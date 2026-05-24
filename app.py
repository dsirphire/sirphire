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

    selected_key = f"{result_key}_selected_model"
    search_key = f"{result_key}_manual"

    if selected_key not in st.session_state:
        st.session_state[selected_key] = ""

    manual_search = st.text_input(
        "Search model",
        placeholder=placeholder,
        key=search_key
    )

    typed_text = manual_search.strip()

    # Filter model suggestions
    filtered_models = []
    if typed_text:
        typed_lower = typed_text.lower()
        filtered_models = [
            model for model in model_list
            if typed_lower in model.lower()
        ][:20]
    else:
        filtered_models = model_list[:20]

    # Suggestion buttons instead of dropdown
    if filtered_models:
        st.markdown(
            '<div class="section-title" style="font-size:1rem;margin-top:10px;margin-bottom:8px;">Select Model</div>',
            unsafe_allow_html=True
        )

        for i in range(0, len(filtered_models), 2):
            cols = st.columns(2)

            for j, col in enumerate(cols):
                if i + j < len(filtered_models):
                    model_name = filtered_models[i + j]

                    with col:
                        button_type = "primary" if st.session_state[selected_key] == model_name else "secondary"

                        if st.button(
                            model_name,
                            key=f"{result_key}_model_btn_{i+j}_{model_name}",
                            use_container_width=True,
                            type=button_type
                        ):
                            st.session_state[selected_key] = model_name
                            st.rerun()

    # If user types exact/custom model, use typed text.
    # If not typing, use selected button model.
    search_model = typed_text if typed_text else st.session_state[selected_key]

    if not search_model:
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
    <span>{safe_search_model}</span>
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
