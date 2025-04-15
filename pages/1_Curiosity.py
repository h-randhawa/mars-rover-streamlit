import streamlit as st
import requests
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Curiosity Rover", layout="wide")
st.title("Curiosity Rover - Mars Photo Explorer")

API_KEY = st.secrets["api"]["nasa_key"]
ROVER = "curiosity"

# ---------------- HELPERS ----------------
@st.cache_data(show_spinner=False)
def get_manifest(rover):
    url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}?api_key={API_KEY}"
    response = requests.get(url)
    return response.json()["photo_manifest"]

@st.cache_data(show_spinner=False)
def get_photos(rover, sol=None, earth_date=None, camera=None, page=1):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        "api_key": API_KEY,
        "page": page
    }
    if sol is not None:
        params["sol"] = sol
    if earth_date is not None:
        params["earth_date"] = earth_date
    if camera != "ALL":
        params["camera"] = camera
    response = requests.get(url, params=params)
    return response.json()["photos"]

# ---------------- FETCH MANIFEST ----------------
manifest = get_manifest(ROVER)
landing_date = manifest['landing_date']
launch_date = manifest['launch_date']
status = manifest['status']
max_sol = manifest['max_sol']
max_date = manifest['max_date']
total_photos = manifest['total_photos']

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filter Options")

query_type = st.sidebar.radio("Search by:", ["Martian Sol", "Earth Date"])
camera = st.sidebar.selectbox("Camera", ["ALL", "FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM"])
# Initialize page number in session state
if "curiosity_page" not in st.session_state:
    st.session_state.curiosity_page = 1

# Page controls
with st.sidebar:
    st.markdown("### 📖 Pagination")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Previous") and st.session_state.curiosity_page > 1:
            st.session_state.curiosity_page -= 1
    with col2:
        if st.button("Next ➡️"):
            st.session_state.curiosity_page += 1

    st.markdown(f"**Current Page:** {st.session_state.curiosity_page}")

sol = None
earth_date = None

if query_type == "Martian Sol":
    sol = st.sidebar.slider("Martian Sol", 0, max_sol, 1000)
else:
    min_date = datetime.strptime(landing_date, "%Y-%m-%d").date()
    max_dt = datetime.strptime(max_date, "%Y-%m-%d").date()
    earth_date = st.sidebar.date_input("Earth Date", value=min_date, min_value=min_date, max_value=max_dt)

# ---------------- FETCH & DISPLAY PHOTOS ----------------
photos = get_photos(
    ROVER,
    sol=sol,
    earth_date=str(earth_date) if earth_date else None,
    camera=camera,
    page=st.session_state.curiosity_page
)

st.subheader(f"Results ({len(photos)} photos found on page {st.session_state.curiosity_page})")

if photos:
    cols = st.columns(3)
    for i, photo in enumerate(photos):
        with cols[i % 3]:
            st.image(photo["img_src"], caption=f"{photo['camera']['full_name']} - Sol {photo['sol']}", use_container_width=True)
else:
    st.info("No photos found. Try a different date, sol, or camera.")

# ---------------- MISSION INFO ----------------
with st.expander("ℹ️ Mission Details"):
    st.markdown(f"""
    **Rover Name:** Curiosity  
    **Launch Date:** {launch_date}  
    **Landing Date:** {landing_date}  
    **Mission Status:** {status.capitalize()}  
    **Total Photos Taken:** {total_photos:,}  
    **Latest Sol Available:** {max_sol}  
    **Latest Earth Date with Photos:** {max_date}
    """)
