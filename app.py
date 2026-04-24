
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# =====================
# 标题 + 说明
# =====================
st.title("🗺️ AI Spatial Intelligence Map")

st.markdown("""
This system collects participatory spatial perception data.  
Users can click on the map to record emotions and urban experiences.  
Data is visualized through color-coded markers and analytical charts.
""")

# =====================
# 数据初始化
# =====================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["lat","lon","emotion","text"])

# =====================
# sidebar
# =====================
with st.sidebar:
    st.header("Emotion Lexicon")

    st.markdown("""
🟢 Positive: safe / calm / green  
🟡 Neutral: normal / mixed  
🔴 Negative: noisy / unsafe / polluted  
""")

# =====================
# layout
# =====================
col1, col2 = st.columns([2,1])

# =====================
# map
# =====================
with col1:

    m = folium.Map(location=[1.35,103.82], zoom_start=13)

    for _, r in st.session_state.data.iterrows():

        color = "green" if r["emotion"]=="positive" else "red" if r["emotion"]=="negative" else "orange"

        folium.CircleMarker(
            [r["lat"], r["lon"]],
            radius=6,
            color=color,
            fill=True
        ).add_to(m)

    map_data = st_folium(m, height=550)

# =====================
# click
# =====================
lat, lon = None, None

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.success(f"Selected: {lat:.4f}, {lon:.4f}")

# =====================
# input
# =====================
emotion = st.selectbox("Emotion", ["positive","neutral","negative"])
text = st.text_area("Description")

img = st.file_uploader("Image", type=["png","jpg","jpeg"])
audio = st.file_uploader("Audio", type=["mp3","wav"])

if st.button("Submit"):

    if lat is not None:

        new = pd.DataFrame([{
            "lat":lat,
            "lon":lon,
            "emotion":emotion,
            "text":text
        }])

        st.session_state.data = pd.concat([st.session_state.data, new], ignore_index=True)

        st.success("Saved!")
    else:
        st.warning("Click map first")

# =====================
# stats
# =====================
with col2:

    st.subheader("Stats")

    if len(st.session_state.data)>0:

        fig, ax = plt.subplots()

        st.session_state.data["emotion"].value_counts().plot(kind="bar", ax=ax)

        st.pyplot(fig)
