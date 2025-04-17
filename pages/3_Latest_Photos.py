import streamlit as st
import requests

st.set_page_config(page_title="Latest Mars Photos", layout="wide")
st.title("📅 Latest Mars Photos")
st.caption("These are the most recent images sent from Perseverance Rover.")

API_KEY = st.secrets["api"]["nasa_key"]
ROVER = "perseverance"

@st.cache_data
def get_latest_photos():
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ROVER}/latest_photos?api_key={API_KEY}"
    response = requests.get(url)
    return response.json().get("latest_photos", [])

photos = get_latest_photos()

st.subheader(f"🔄 {len(photos)} Latest Photos from Perseverance")

if photos:
    cols = st.columns(3)
    for i, photo in enumerate(photos):
        with cols[i % 3]:
            st.image(
                photo["img_src"],
                caption=f"{photo['camera']['full_name']} — {photo['earth_date']}",
                use_container_width=True
            )
else:
    st.info("No recent photos available. Check back later.")
