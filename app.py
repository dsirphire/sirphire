import re
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sirphire Inventory",
    page_icon="📦",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}
.app-title {
    font-size: 34px;
    font-weight: 800;
    color: #111827;
}
.app-title span {
    color: #ef4444;
}
.sub-title {
    color: #6b7280;
    font-size: 15px;
}
.result-box {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 14px;
    margin-top: 14px;
}
.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #fee2e2;
    color: #991b1b;
    font-size: 13px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


PRODUCT_CONFIG = {
    "Tempered Glass": {
        "secret_key": "TEMPERED_SHEET_URL",
        "fallback_secret_key": "SHEET_URL",
        "type_label": "Display Type",
        "search_placeholder": "Search model for tempered glass..."
    },
    "Mobile Cover": {
        "secret_key": "COVER_SHEET_URL",
        "fallback_secret_key": None,
        "type_label": "Cover Type",
        "search_placeholder": "Search model for mobile cover..."
    }
}


def get_sheet_url(config):
    url = st.secrets.get(config["secret_key"], "")
    if not url and config.get("fallback_secret_key"):
        url = st.secrets.get(config["fallback_secret_key"], "")
    return url


def convert_to_xlsx_export_url(url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if not match:
        return None
    sheet_id = match.group(1)
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"


@st.cache_data(ttl=300)
def load_data(sheet_url):
    export_url = convert_to_xlsx_export_url(sheet_url)
    if not export_url:
        raise ValueError("Invalid Google Sheet URL")

    compatible_df = pd.read_excel(
        export_url,
        sheet_name="compatible modal",
        header=None
    )

    all_models_df = pd.read_excel(
        export_url,
        sheet_name="All Modals",
        header=None
    )

    compatible_df = compatible_df.iloc[:, [1, 2]].copy()
    compatible_df.columns = ["location", "compatible"]

    all_models_df = all_models_df.iloc[:, [2, 3]].copy()
    all_models_df.columns = ["model", "type"]

    compatible_df = compatible_df.dropna(subset=["compatible"])
    all_models_df = all_models_df.dropna(subset=["model"])

    compatible_df["location"] = compatible_df["location"].astype(str).str.strip()
    compatible_df["compatible"] = compatible_df["compatible"].astype(str).str.strip()

    all_models_df["model"] = all_models_df["model"].astype(str).str.strip()
    all_models_df["type"] = all_models_df["type"].astype(str).str.strip()

    return compatible_df, all_models_df


def find_matches(search_text, compatible_df):
    search_text = search_text.strip().lower()

    if not search_text:
        return pd.DataFrame()

    mask = compatible_df["compatible"].str.lower().str.contains(
        re.escape(search_text),
        na=False
    )

    return compatible_df[mask].copy()


def get_model_type(search_text, all_models_df):
    search_text = search_text.strip().lower()

    exact_match = all_models_df[
        all_models_df["model"].str.lower() == search_text
    ]

    if not exact_match.empty:
        return exact_match.iloc[0]["type"]

    partial_match = all_models_df[
        all_models_df["model"].str.lower().str.contains(
            re.escape(search_text),
            na=False
        )
    ]

    if not partial_match.empty:
        return partial_match.iloc[0]["type"]

    return "Not found"


st.markdown(
    """
    <div class="app-title">Sirphire <span>Inventory</span></div>
    <div class="sub-title">Tempered Glass & Mobile Cover Compatibility Search</div>
    """,
    unsafe_allow_html=True
)

st.divider()

product = st.radio(
    "Select Product",
    ["Tempered Glass", "Mobile Cover"],
    horizontal=True
)

config = PRODUCT_CONFIG[product]
sheet_url = get_sheet_url(config)

if not sheet_url:
    st.warning(f"{product} sheet link not found. Please add it in Streamlit Secrets.")
    st.stop()

try:
    compatible_df, all_models_df = load_data(sheet_url)
except Exception as e:
    st.error("Sheet data load nahi ho pa raha. Sheet link, sharing permission, ya tab names check karo.")
    st.exception(e)
    st.stop()

model_options = sorted(all_models_df["model"].dropna().unique().tolist())

col1, col2 = st.columns([2, 1])

with col1:
    selected_model = st.selectbox(
        "Select Model",
        [""] + model_options
    )

with col2:
    manual_search = st.text_input(
        "Manual Search",
        placeholder=config["search_placeholder"]
    )

search_text = manual_search.strip() if manual_search.strip() else selected_model.strip()

if search_text:
    matches = find_matches(search_text, compatible_df)
    model_type = get_model_type(search_text, all_models_df)

    st.markdown(f'<span class="badge">{product}</span>', unsafe_allow_html=True)

    if matches.empty:
        st.error("No compatible location found.")
    else:
        locations = matches["location"].dropna().unique().tolist()
        compatible_count = len(matches)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        st.subheader(search_text)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Location", ", ".join(locations))

        with c2:
            st.metric("Compatible Count", compatible_count)

        with c3:
            st.metric(config["type_label"], model_type)

        st.markdown("### Compatible Model List")

        for _, row in matches.iterrows():
            st.write(f"**Location:** {row['location']}")
            st.write(row["compatible"])
            st.divider()

        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("Matched Rows"):
            st.dataframe(matches, use_container_width=True)
else:
    st.info("Model select karo ya manual search me model name type karo.")
