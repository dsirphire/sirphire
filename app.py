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
    max-width: 1100px;
}
.app-title {
    font-size: 42px;
    font-weight: 900;
    color: #111827;
    line-height: 1.1;
}
.app-title span {
    color: #ef4444;
}
.sub-title {
    color: #6b7280;
    font-size: 17px;
    margin-top: 8px;
}
.search-box {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    padding: 22px;
    border-radius: 18px;
    margin-top: 24px;
}
.card {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 20px;
    border-radius: 18px;
    margin-top: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
}
.card-title {
    font-size: 22px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 8px;
}
.found {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 999px;
    background: #dcfce7;
    color: #166534;
    font-weight: 800;
    font-size: 13px;
}
.not-found {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 999px;
    background: #fee2e2;
    color: #991b1b;
    font-weight: 800;
    font-size: 13px;
}
.location {
    font-size: 28px;
    font-weight: 900;
    color: #ef4444;
    margin: 12px 0;
}
.small-text {
    color: #6b7280;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


PRODUCT_CONFIG = {
    "Tempered Glass": {
        "secret_key": "TEMPERED_SHEET_URL",
        "fallback_secret_key": "SHEET_URL",
        "type_label": "Display Type",
        "icon": "🛡️"
    },
    "Mobile Cover": {
        "secret_key": "COVER_SHEET_URL",
        "fallback_secret_key": None,
        "type_label": "Cover Type",
        "icon": "📱"
    },
    "Camera Lens Protector": {
        "secret_key": "LENS_SHEET_URL",
        "fallback_secret_key": None,
        "type_label": "Lens Type",
        "icon": "📷"
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


def get_all_model_options():
    models = []

    for product_name, config in PRODUCT_CONFIG.items():
        sheet_url = get_sheet_url(config)

        if not sheet_url:
            continue

        try:
            _, all_models_df = load_data(sheet_url)
            models.extend(all_models_df["model"].dropna().tolist())
        except Exception:
            pass

    clean_models = sorted(list(set([str(m).strip() for m in models if str(m).strip()])))
    return clean_models


def render_product_result(product_name, config, search_text):
    sheet_url = get_sheet_url(config)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="card-title">{config["icon"]} {product_name}</div>',
        unsafe_allow_html=True
    )

    if not sheet_url:
        st.markdown('<span class="not-found">Sheet link missing</span>', unsafe_allow_html=True)
        st.warning(f"{product_name} ka sheet link Streamlit Secrets me add nahi hai.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    try:
        compatible_df, all_models_df = load_data(sheet_url)
    except Exception as e:
        st.markdown('<span class="not-found">Sheet error</span>', unsafe_allow_html=True)
        st.error(f"{product_name} sheet load nahi ho rahi. Tab name ya permission check karo.")
        st.caption(str(e))
        st.markdown("</div>", unsafe_allow_html=True)
        return

    matches = find_matches(search_text, compatible_df)
    model_type = get_model_type(search_text, all_models_df)

    if matches.empty:
        st.markdown('<span class="not-found">Not Found</span>', unsafe_allow_html=True)
        st.write("Is model ke liye location nahi mili.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    locations = matches["location"].dropna().unique().tolist()

    st.markdown('<span class="found">Available</span>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="location">{", ".join(locations)}</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Compatible Count", len(matches))

    with c2:
        st.metric(config["type_label"], model_type)

    with st.expander("Compatible Model List"):
        for _, row in matches.iterrows():
            st.write(f"**Location:** {row['location']}")
            st.write(row["compatible"])
            st.divider()

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="app-title">Sirphire <span>Inventory</span></div>
    <div class="sub-title">Ek model search karo aur tempered glass, mobile cover, camera lens protector ki location ek saath dekho.</div>
    """,
    unsafe_allow_html=True
)

model_options = get_all_model_options()

st.markdown('<div class="search-box">', unsafe_allow_html=True)

selected_model = st.selectbox(
    "Model select karo",
    [""] + model_options
)

manual_search = st.text_input(
    "Ya model name manually type karo",
    placeholder="Example: iPhone 13, Vivo Y20, Redmi Note 10..."
)

st.markdown("</div>", unsafe_allow_html=True)

search_text = manual_search.strip() if manual_search.strip() else selected_model.strip()

if not search_text:
    st.info("Model select karo ya search box me model name type karo.")
else:
    st.subheader(f"Search Result: {search_text}")

    for product_name, config in PRODUCT_CONFIG.items():
        render_product_result(product_name, config, search_text)
