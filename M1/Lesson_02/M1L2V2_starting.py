import streamlit as st
import pandas as pd
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="StylePulse | AI Wardrobe Coordinator",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE SESSION STATE (PERSISTENT DATA) ---
if "wardrobe" not in st.session_state:
    st.session_state.wardrobe = pd.DataFrame([
        {"item_name": "White Linen Shirt", "category": "Top", "weather_match": "Sunny & Warm", "occasion_match": "Casual"},
        {"item_name": "Silk Button-Down", "category": "Top", "weather_match": "Sunny & Warm", "occasion_match": "Business"},
        {"item_name": "Graphic Tee", "category": "Top", "weather_match": "Sunny & Warm", "occasion_match": "Casual"},
        {"item_name": "Blue Denim Jeans", "category": "Bottom", "weather_match": "Sunny & Warm", "occasion_match": "Casual"},
        {"item_name": "Tailored Chinos", "category": "Bottom", "weather_match": "Sunny & Warm", "occasion_match": "Business"},
        {"item_name": "Athletic Shorts", "category": "Bottom", "weather_match": "Sunny & Warm", "occasion_match": "Workout"},
        {"item_name": "Black Blazer", "category": "Outerwear", "weather_match": "Cold & Snowy", "occasion_match": "Business"},
        {"item_name": "Waterproof Raincoat", "category": "Outerwear", "weather_match": "Rainy & Cool", "occasion_match": "Casual"},
        {"item_name": "White Leather Sneakers", "category": "Shoes", "weather_match": "Sunny & Warm", "occasion_match": "Casual"},
        {"item_name": "Running Shoes", "category": "Shoes", "weather_match": "Sunny & Warm", "occasion_match": "Workout"},
        {"item_name": "Leather Dress Shoes", "category": "Shoes", "weather_match": "Cold & Snowy", "occasion_match": "Business"},
    ])

# --- HEADER SECTION ---
st.title("👗 StylePulse")
st.caption("AI-Powered Daily Outfit Coordinator • Beat Morning Decision Fatigue")
st.divider()

# --- SIDEBAR: CONTEXT & CLOSET MANAGEMENT ---
with st.sidebar:
    st.header("🎯 Today's Context")
    weather = st.selectbox(
        "Current Weather",
        ["Sunny & Warm", "Rainy & Cool", "Cold & Snowy"],
        help="Select local weather conditions"
    )
    occasion = st.selectbox(
        "Today's Occasion",
        ["Casual", "Business", "Workout"],
        help="What type of event are you attending?"
    )
    
    st.divider()
    
    st.header("📸 Digital Closet Upload")
    with st.form("upload_form", clear_on_submit=True):
        item_name = st.text_input("Item Name", placeholder="e.g., Wool Sweater")
        category = st.selectbox("Category", ["Top", "Bottom", "Outerwear", "Shoes"])
        w_match = st.selectbox("Best Weather", ["Sunny & Warm", "Rainy & Cool", "Cold & Snowy"])
        o_match = st.selectbox("Best Occasion", ["Casual", "Business", "Workout"])
        uploaded_file = st.file_uploader("Upload Photo (Optional)", type=["jpg", "png", "jpeg"])
        
        submit_button = st.form_submit_button("Add to Wardrobe", use_container_width=True)
        
        if submit_button:
            if item_name.strip() != "":
                new_item = pd.DataFrame([{
                    "item_name": item_name,
                    "category": category,
                    "weather_match": w_match,
                    "occasion_match": o_match
                }])
                st.session_state.wardrobe = pd.concat([st.session_state.wardrobe, new_item], ignore_index=True)
                st.success(f"Added '{item_name}' to your wardrobe!")
            else:
                st.error("Please enter an item name.")

# --- MAIN CONTENT AREA ---
col_main, col_stats = st.columns([2, 1], gap="large")

with col_main:
    st.subheader("💡 Today's Recommendation")
    
    # Filter matching items
    df = st.session_state.wardrobe
    exact_matches = df[
        (df["weather_match"] == weather) & 
        (df["occasion_match"] == occasion)
    ]
    
    # Assembly logic: ensure we attempt to pick 1 Top, 1 Bottom, 1 Shoe, and Outerwear if cold/rainy
    categories_needed = ["Top", "Bottom", "Shoes"]
    if weather in ["Rainy & Cool", "Cold & Snowy"]:
        categories_needed.append("Outerwear")
        
    outfit_recommendation = []
    
    for cat in categories_needed:
        # Try exact category match
        cat_matches = exact_matches[exact_matches["category"] == cat]
        if not cat_matches.empty:
            chosen = cat_matches.sample(1).iloc[0]
            outfit_recommendation.append(chosen)
        else:
            # Fallback to category-only match
            fallback = df[df["category"] == cat]
            if not fallback.empty:
                chosen = fallback.sample(1).iloc[0]
                outfit_recommendation.append(chosen)

    # Display Outcome
    if outfit_recommendation:
        st.info(f"Targeting **{weather}** weather for a **{occasion}** setting:")
        
        for item in outfit_recommendation:
            with st.container(border=True):
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.markdown(f"**{item['category']}**")
                with c2:
                    st.markdown(f"### {item['item_name']}")
                    st.caption(f"Tags: {item['weather_match']} • {item['occasion_match']}")
    else:
        st.warning("No items found in your closet! Use the sidebar to add clothing items.")

    # Feedback Loop Controls
    st.divider()
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        if st.button("👍 Wear This Outfit", type="primary", use_container_width=True):
            st.balloons()
            st.success("Outfit logged to your style history!")
    with f_col2:
        if st.button("🔀 Shuffle Options", use_container_width=True):
            st.rerun()

with col_stats:
    st.subheader("📊 Closet Overview")
    
    # Metrics
    total_items = len(st.session_state.wardrobe)
    st.metric("Total Items Cataloged", total_items)
    
    # Category Breakdown
    st.markdown("**Category Breakdown**")
    cat_counts = st.session_state.wardrobe["category"].value_counts()
    st.bar_chart(cat_counts, height=200)
    
    # Raw Data Expander
    with st.expander("View Full Wardrobe Inventory"):
        st.dataframe(st.session_state.wardrobe, use_container_width=True, hide_index=True)