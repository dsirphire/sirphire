import streamlit as st
import pandas as pd
import re
import html

st.set_page_config(
    page_title="Sirphire Utility",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Force Light Modern UI CSS ----------
st.markdown("""
<style>
:root {
    color-scheme: light !important;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(135deg, #fcf7f7 0%, #ffffff 48%, #f7f8fb 100%) !important;
    color: #111827 !important;
    color-scheme: light !important;
}

* {
    color-scheme: light !important;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1080px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stToolbar {
    display: none !important;
}

html, body, .stApp,
p, li, span, div, label {
    color: #111827 !important;
}

.app-card {
    background: linear-gradient(180deg, #ffffff 0%, #fffdfd 100%) !important;
    border: 1px solid #f0dede;
    border-radius: 7px;
    padding: 30px 32px;
    box-shadow: 0 4px 14px rgba(25, 25, 25, 0.025);
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}

.app-card:before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: linear-gradient(90deg, #ff4b4b 0%, #ff7a7a 100%);
}

.utility-tag {
    display: inline-block;
    background: #fff4f4 !important;
    color: #d92d37 !important;
    border: 1px solid #ffd8d8;
    padding: 8px 14px;
    border-radius: 7px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    margin-bottom: 18px;
}

.app-title {
    font-size: 3rem;
    font-weight: 700;
    color: #1f2937 !important;
    margin-bottom: 10px;
    letter-spacing: -0.04em;
    line-height: 1.08;
}

.app-title span {
    color: #d92d37 !important;
    font-weight: 700;
}

.app-subtitle {
    font-size: 1.12rem;
    color: #4b5563 !important;
    line-height: 1.65;
    margin-bottom: 0;
    font-weight: 400;
    max-width: 760px;
}

/* ---------- Category Cards ---------- */
.category-title-main {
    font-size: 1.35rem;
    font-weight: 600;
    color: #1f2937 !important;
    margin-top: 8px;
    margin-bottom: 14px;
}

.category-card {
    background: #ffffff !important;
    border: 1px solid #eceff3;
    border-radius: 12px;
    padding: 24px 22px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.035);
    min-height: 130px;
    margin-bottom: 12px;
}

.category-card.active {
    border: 2px solid #d92d37;
    background: #fff8f8 !important;
}

.category-title {
    font-size: 1.45rem;
    font-weight: 700;
    color: #1f2937 !important;
    margin-bottom: 8px;
}

.category-subtitle {
    font-size: 0.98rem;
    color: #667085 !important;
    line-height: 1.45;
}

div[data-testid="stButton"] > button {
    width: 100%;
    min-height: 58px;
    border-radius: 14px;
    border: 1.5px solid #d92d37;
    background: #ffffff !important;
    color: #d92d37 !important;
    font-size: 1.05rem;
    font-weight: 700;
}

div[data-testid="stButton"] > button:hover {
    background: #fff4f4 !important;
    color: #b4232c !important;
    border-color: #b4232c;
}

/* ---------- Inputs ---------- */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label {
    font-size: 1.02rem !important;
    font-weight: 500 !important;
    color: #1f2937 !important;
}

div[data-testid="stSelectbox"] div,
div[data-testid="stTextInput"] div {
    font-size: 1.02rem !important;
    color: #111827 !important;
    font-weight: 400 !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 16px !important;
    background-color: #ffffff !important;
    border: 1.5px solid #d6dbe4 !important;
    color: #111827 !important;
    min-height: 54px !important;
    box-shadow: none !important;
}

div[data-baseweb="select"] span {
    color: #111827 !important;
    font-weight: 400 !important;
    background-color: transparent !important;
    -webkit-text-fill-color: #111827 !important;
}

div[data-baseweb="input"] input {
    color: #111827 !important;
    background-color: #ffffff !important;
    font-weight: 400 !important;
    -webkit-text-fill-color: #111827 !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #667085 !important;
    opacity: 1 !important;
    font-weight: 400 !important;
    -webkit-text-fill-color: #667085 !important;
}

div[data-baseweb="popover"] {
    background-color: #ffffff !important;
    color: #111827 !important;
}

div[data-baseweb="popover"] * {
    background-color: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 400 !important;
}

ul[role="listbox"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 14px !important;
}

li[role="option"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    font-weight: 400 !important;
    -webkit-text-fill-color: #111827 !important;
}

li[role="option"] div,
li[role="option"] span {
    background-color: transparent !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 400 !important;
}

li[role="option"]:hover {
    background-color: #f8fafc !important;
    color: #111827 !important;
}

li[role="option"]:hover * {
    background-color: #f8fafc !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

li[aria-selected="true"],
li[aria-selected="true"] * {
    background-color: #fff5f5 !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 500 !important;
}

input, textarea, select, button {
    color-scheme: light !important;
    background-color: #ffffff !important;
    color: #111827 !important;
}

/* ---------- Alerts ---------- */
.stAlert {
    border-radius: 7px;
    border: 1px solid rgba(22, 163, 74, 0.12);
}

.stAlert div {
    color: #166534 !important;
    font-weight: 400 !important;
}

/* ---------- Metric Grid ---------- */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    margin: 18px 0 32px 0;
}

.metric-grid.two-col {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.metric-card {
    background: #ffffff !important;
    border: 1px solid #eceff3;
    border-radius: 7px;
    padding: 20px 22px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.025);
    min-height: 145px;
    overflow: visible !important;
}

.metric-label {
    font-size: 0.98rem !important;
    color: #667085 !important;
    font-weight: 500 !important;
    margin-bottom: 18px;
}

.metric-value {
    font-size: 1.75rem !important;
    font-weight: 600 !important;
    color: #1f2937 !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
    word-break: break-word !important;
}

.location-card .metric-value {
    font-size: 1.45rem !important;
}

/* ---------- Result Sections ---------- */
.section-title {
    font-size: 1.35rem;
    font-weight: 600;
    color: #1f2937 !important;
    margin-top: 8px;
    margin-bottom: 14px;
}

.selected-model {
    background: #ffffff !important;
    border: 1px solid #eceff3;
    border-radius: 7px;
    padding: 15px 18px;
    margin: 18px 0 16px 0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.02);
    font-size: 1.02rem;
    color: #1f2937 !important;
    font-weight: 400 !important;
}

.selected-model .label {
    color: #667085 !important;
    font-weight: 500 !important;
    margin-right: 8px;
}

.selected-model .value {
    color: #1f2937 !important;
    font-weight: 400 !important;
}

.model-item {
    background: #ffffff !important;
    border: 1px solid #eceff3;
    border-radius: 7px;
    padding: 13px 15px;
    margin-bottom: 9px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.018);
    color: #1f2937 !important;
    font-weight: 400 !important;
    font-size: 1rem !important;
    line-height: 1.45;
}

details {
    background: #ffffff !important;
    border-radius: 16px !important;
    color: #111827 !important;
    border: 1px solid #eceff3;
}

details * {
    color: #111827 !important;
}

/* ---------- Mobile ---------- */
@media screen and (max-width: 768px) {
    .block-container {
        padding-top: 1.1rem;
        padding-left: 0.95rem;
        padding-right: 0.95rem;
    }

    .app-card {
        padding: 22px 20px;
        border-radius: 7px;
        margin-bottom: 20px;
    }

    .utility-tag {
        font-size: 0.74rem;
        padding: 7px 11px;
    }

    .app-title {
        font-size: 2.25rem;
        line-height: 1.12;
    }

    .app-subtitle {
        font-size: 1.04rem;
        color: #475467 !important;
        font-weight: 400;
    }

    .category-card {
        min-height: auto;
        padding: 18px 16px;
    }

    .category-title {
        font-size: 1.25rem;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        font-size: 1.04rem !important;
        font-weight: 500 !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="input"] input {
        font-size: 1rem !important;
        color: #111827 !important;
        font-weight: 400 !important;
        -webkit-text-fill-color: #111827 !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #667085 !important;
        font-weight: 400 !important;
        -webkit-text-fill-color: #667085 !important;
    }

    .metric-grid,
    .metric-grid.two-col {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
        margin: 16px 0 28px 0;
    }

    .metric-card {
        min-height: 118px;
        padding: 16px 15px;
        border-radius: 7px;
    }

    .location-card {
        grid-column: 1 / -1;
        min-height: auto;
    }

    .metric-label {
        font-size: 0.86rem !important;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 1.35rem !important;
        line-height: 1.28 !important;
    }

    .location-card .metric-value {
        font-size: 1.18rem !important;
        line-height: 1.35 !important;
    }

    .model-item {
        font-size: 0.98rem !important;
        font-weight: 400 !important;
    }

    .selected-model {
        font-size: 1rem !important;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="app-card">
    <div class="utility-tag">SIRPHIRE UTILITY</div>
    <div class="app-title">Compatibility <span>Dashboard</span></div>
    <p class="app-subtitle">
        Select Tempered Glass or Mobile Cover and instantly view location and compatible model list.
    </p>
</div>
""", unsafe_allow_html=True)

SHEET_URL = st.secrets.get("SHEET_URL", "")


# ---------- Google Sheet Helpers ----------
def get_sheet_id(url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if match:
        return match.group(1)
    return None


def excel_export_url(sheet_url):
    sheet_id = get_sheet_id(sheet_url)
    if not sheet_id:
        return sheet_url
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"


def clean_text(value):
    return str(value).strip() if value is not None else ""


def make_compatible_df(raw_df, location_col_index=1, compatible_col_index=2):
    raw_df = raw_df.fillna("")

    compatible_df = raw_df.iloc[:, [location_col_index, compatible_col_index]].copy()
    compatible_df.columns = ["location", "compatible"]

    compatible_df["location"] = compatible_df["location"].astype(str).str.strip()
    compatible_df["compatible"] = compatible_df["compatible"].astype(str).str.strip()

    compatible_df = compatible_df[
        (compatible_df["location"] != "") &
        (compatible_df["compatible"] != "")
    ]

    compatible_df = compatible_df[
        ~compatible_df["location"].str.lower().str.contains("s.no|location|nan", na=False)
    ]

    compatible_df = compatible_df[
        ~compatible_df["compatible"].str.lower().str.contains("compatible model names|nan", na=False)
    ]

    return compatible_df.drop_duplicates().reset_index(drop=True)


def make_model_list(raw_df, model_col_index):
    raw_df = raw_df.fillna("")

    if raw_df.shape[1] <= model_col_index:
        return []

    models = raw_df.iloc[:, model_col_index].astype(str).str.strip()

    models = models[
        (models != "") &
        (~models.str.lower().str.contains("all modals|all models|nan", na=False))
    ]

    return sorted(models.drop_duplicates().tolist())


def make_display_type_map(raw_df):
    raw_df = raw_df.fillna("")

    if raw_df.shape[1] < 4:
        return {}

    models_df = raw_df.iloc[:, [2, 3]].copy()
    models_df.columns = ["model", "display_type"]

    models_df["model"] = models_df["model"].astype(str).str.strip()
    models_df["display_type"] = models_df["display_type"].astype(str).str.strip()

    models_df = models_df[
        (models_df["model"] != "") &
        (~models_df["model"].str.lower().str.contains("all modals|all models|nan", na=False))
    ]

    return {
        row["model"].lower(): row["display_type"]
        for _, row in models_df.drop_duplicates(subset=["model"], keep="first").iterrows()
        if row["display_type"] and row["display_type"].lower() != "nan"
    }


@st.cache_data(ttl=60)
def load_data(sheet_url):
    url = excel_export_url(sheet_url)

    compatible_raw = pd.read_excel(
        url,
        sheet_name="compatible modal",
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    mobile_cover_raw = pd.read_excel(
        url,
        sheet_name="Mobile Cover",
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    models_raw = pd.read_excel(
        url,
        sheet_name="All Modals",
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    # Tempered:
    # compatible modal sheet:
    # Column B = location
    # Column C = compatible model list
    tempered_df = make_compatible_df(
        compatible_raw,
        location_col_index=1,
        compatible_col_index=2
    )

    # Mobile Cover:
    # Mobile Cover sheet:
    # Column B = location
    # Column C = compatible back cover model list
    back_cover_df = make_compatible_df(
        mobile_cover_raw,
        location_col_index=1,
        compatible_col_index=2
    )

    # All Modals sheet:
    # Column C = tempered model list
    # Column G = mobile cover model list
    tempered_model_list = make_model_list(models_raw, model_col_index=2)
    back_cover_model_list = make_model_list(models_raw, model_col_index=6)

    display_type_map = make_display_type_map(models_raw)

    return tempered_df, back_cover_df, tempered_model_list, back_cover_model_list, display_type_map


def find_matches(df, search_model):
    search_model = clean_text(search_model)

    if not search_model:
        return df.iloc[0:0]

    return df[
        df["compatible"].astype(str).str.contains(
            search_model,
            case=False,
            na=False,
            regex=False
        )
    ]


def render_search_section(
    section_title,
    df,
    model_list,
    placeholder,
    result_key,
    show_display_type=False,
    display_type_map=None
):
    st.markdown(
        f'<div class="section-title">{html.escape(section_title)}</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_model = st.selectbox(
            "Select or search a model",
            options=[""] + model_list,
            index=0,
            key=f"{result_key}_select"
        )

    with col2:
        manual_search = st.text_input(
            "Or type manually",
            placeholder=placeholder,
            key=f"{result_key}_manual"
        )

    search_model = manual_search.strip() if manual_search.strip() else selected_model.strip()

    if not search_model:
        st.info("Select a model from the dropdown or type it manually.")
        return

    result = find_matches(df, search_model)

    if result.empty:
        st.warning("No compatible result found.")
        return

    locations = sorted(result["location"].astype(str).str.strip().unique())

    all_compatible = []
    for value in result["compatible"].astype(str):
        parts = [x.strip() for x in value.split(",") if x.strip()]
        all_compatible.extend(parts)

    all_compatible = sorted(set(all_compatible))
    location_text = " & ".join(locations)

    safe_search_model = html.escape(search_model)
    safe_location_text = html.escape(location_text)
    safe_count = html.escape(str(len(all_compatible)))

    st.success("Result found")

    st.markdown(
        f"""
<div class="selected-model">
    <span class="label">Selected model:</span>
    <span class="value">{safe_search_model}</span>
</div>
""",
        unsafe_allow_html=True
    )

    if show_display_type:
        display_type = "Not found"

        if display_type_map:
            display_type = display_type_map.get(search_model.lower(), "Not found")

        safe_display_type = html.escape(str(display_type))

        metric_html = f"""
<div class="metric-grid">
    <div class="metric-card location-card">
        <div class="metric-label">Location</div>
        <div class="metric-value">{safe_location_text}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Compatible Count</div>
        <div class="metric-value">{safe_count}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Display Type</div>
        <div class="metric-value">{safe_display_type}</div>
    </div>
</div>
"""
    else:
        metric_html = f"""
<div class="metric-grid two-col">
    <div class="metric-card location-card">
        <div class="metric-label">Location</div>
        <div class="metric-value">{safe_location_text}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Compatible Count</div>
        <div class="metric-value">{safe_count}</div>
    </div>
</div>
"""

    st.markdown(metric_html, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Compatible Model List</div>',
        unsafe_allow_html=True
    )

    for model in all_compatible:
        safe_model = html.escape(model)
        st.markdown(
            f'<div class="model-item">{safe_model}</div>',
            unsafe_allow_html=True
        )

    with st.expander("Matched Rows"):
        st.dataframe(result, use_container_width=True)


# ---------- Load Data ----------
if not SHEET_URL:
    st.error("SHEET_URL is missing. Please add your Google Sheet link in Streamlit secrets.")
    st.stop()

try:
    (
        tempered_df,
        back_cover_df,
        tempered_model_list,
        back_cover_model_list,
        display_type_map
    ) = load_data(SHEET_URL)
except Exception as e:
    st.error("Unable to load Google Sheet data.")
    st.caption(str(e))
    st.stop()


# ---------- Category Selector ----------
if "selected_category" not in st.session_state:
    st.session_state.selected_category = ""

st.markdown(
    '<div class="category-title-main">Select Category</div>',
    unsafe_allow_html=True
)

col_a, col_b = st.columns(2)

with col_a:
    active_class = "active" if st.session_state.selected_category == "tempered" else ""
    st.markdown(f"""
    <div class="category-card {active_class}">
        <div class="category-title">Tempered Glass</div>
        <div class="category-subtitle">
            Search tempered glass compatibility, location and display type.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Tempered Glass", key="open_tempered"):
        st.session_state.selected_category = "tempered"
        st.rerun()

with col_b:
    active_class = "active" if st.session_state.selected_category == "mobile_cover" else ""
    st.markdown(f"""
    <div class="category-card {active_class}">
        <div class="category-title">Mobile Cover</div>
        <div class="category-subtitle">
            Search mobile/back cover compatibility and location.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Mobile Cover", key="open_mobile_cover"):
        st.session_state.selected_category = "mobile_cover"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)


# ---------- Conditional Search Section ----------
if st.session_state.selected_category == "tempered":
    render_search_section(
        section_title="Tempered Glass Compatibility",
        df=tempered_df,
        model_list=tempered_model_list,
        placeholder="Example: Redmi Note 7 Tempered",
        result_key="tempered",
        show_display_type=True,
        display_type_map=display_type_map
    )

elif st.session_state.selected_category == "mobile_cover":
    render_search_section(
        section_title="Mobile Cover Compatibility",
        df=back_cover_df,
        model_list=back_cover_model_list,
        placeholder="Example: Redmi Note 7 Back Cover",
        result_key="back_cover",
        show_display_type=False
    )

else:
    st.info("Please select Tempered Glass or Mobile Cover to start searching.")
