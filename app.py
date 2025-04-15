import streamlit as st
import requests
import random

# ----------------------------------
# SET PAGE CONFIG FIRST
# ----------------------------------
st.set_page_config(
    page_title="Mars Rover Explorer",
    layout="wide",
    page_icon="🚀"
)

# ----------------------------------
# API KEY FROM SECRETS
# ----------------------------------
API_KEY = st.secrets["api"]["nasa_key"] if "api" in st.secrets else "DEMO_KEY"
ROVER = "curiosity"

# ----------------------------------
# API CALLS
# ----------------------------------
@st.cache_data
def get_manifest(rover):
    url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}?api_key={API_KEY}"
    response = requests.get(url)
    return response.json()["photo_manifest"]

@st.cache_data
def get_random_banner_photo():
    manifest = get_manifest(ROVER)
    max_sol = manifest["max_sol"]
    attempts = 0
    while attempts < 5:
        random_sol = random.randint(0, max_sol)
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ROVER}/photos"
        params = {"sol": random_sol, "api_key": API_KEY}
        response = requests.get(url, params=params)
        photos = response.json().get("photos", [])
        if photos:
            return random.choice(photos)["img_src"]
        attempts += 1
    return None

# ----------------------------------
# DISPLAY RANDOM BANNER IMAGE
# ----------------------------------
banner_url = get_random_banner_photo()
if banner_url:
    st.image(banner_url, caption="📸 Random Image from Curiosity Rover", use_container_width=True)
else:
    st.warning("No banner image could be loaded. Try refreshing or check API limits.")

# ----------------------------------
# TITLE & INTRO
# ----------------------------------
st.title("🚀 Mars Rover Photo Explorer")

st.markdown("""
Welcome to the **Mars Rover Explorer**, where you can view real images taken by NASA's rovers on the surface of Mars.  
The app is powered by [NASA's Mars Rover API](https://api.nasa.gov/) and displays live data with interactive filtering.

### 🔍 What You Can Do:
- Select one of NASA’s four Mars rovers from the sidebar
- Search photos by **Martian Sol** or **Earth Date**
- Filter by **camera**
- View **full-resolution images**
- Learn about each rover’s **mission status** and stats

> Use the navigation in the sidebar to get started!
""")

st.markdown("---")

# Optional: NASA + Streamlit attribution
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://www.nasa.gov/sites/default/files/thumbnails/image/nasa-logo-web-rgb.png", width=70)
with col2:
    st.markdown("""
**Powered by NASA Open APIs**  
Made with ❤️ using [Streamlit](https://streamlit.io)
""")
