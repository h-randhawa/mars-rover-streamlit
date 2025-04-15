import streamlit as st
import requests
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Perseverance Rover", layout="wide")
st.title("🧪 Perseverance Rover - Mars Photo Explorer")
st.caption("Browse real images taken by NASA's Perseverance rover on the surface of Mars.")

API_KEY = st.secrets["api"]["nasa_key"]
ROVER = "perseverance"

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

# ✅ Updated camera list for Perseverance
camera = st.sidebar.selectbox("Camera", [
    "ALL", "EDL_RUCAM", "EDL_DDCAM", "EDL_PUCAM1", "EDL_PUCAM2", "NAVCAM_LEFT", "NAVCAM_RIGHT",
    "MCZ_RIGHT", "MCZ_LEFT", "FRONT_HAZCAM_LEFT", "FRONT_HAZCAM_RIGHT",
    "REAR_HAZCAM_LEFT", "REAR_HAZCAM_RIGHT", "SKYCAM", "SHERLOC_WATSON", "SUPERCAM_RMI"
])

# Initialize page number in session state
if "perseverance_page" not in st.session_state:
    st.session_state.perseverance_page = 1

# Page controls
with st.sidebar:
    st.markdown("### 📖 Pagination")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Previous") and st.session_state.perseverance_page > 1:
            st.session_state.perseverance_page -= 1
    with col2:
        if st.button("Next ➡️"):
            st.session_state.perseverance_page += 1
    st.markdown(f"**Current Page:** {st.session_state.perseverance_page}")
    if st.sidebar.button("🔄 Reset to Page 1"):
        st.session_state.perseverance_page = 1

sol = None
earth_date = None

if query_type == "Martian Sol":
    sol = st.sidebar.slider("Martian Sol", 0, max_sol, 100)
else:
    min_date = datetime.strptime(landing_date, "%Y-%m-%d").date()
    max_dt = datetime.strptime(max_date, "%Y-%m-%d").date()
    earth_date = st.sidebar.date_input("Earth Date", value=min_date, min_value=min_date, max_value=max_dt)

# Debug: Show API call info
st.sidebar.code(f"Sol: {sol} | Earth Date: {earth_date} | Camera: {camera} | Page: {st.session_state.perseverance_page}")

# ---------------- FETCH & DISPLAY PHOTOS ----------------
photos = get_photos(
    ROVER,
    sol=sol,
    earth_date=str(earth_date) if earth_date else None,
    camera=camera,
    page=st.session_state.perseverance_page
)

st.subheader(f"Results ({len(photos)} photos found on page {st.session_state.perseverance_page})")

if photos:
    cols = st.columns(3)
    for i, photo in enumerate(photos):
        with cols[i % 3]:
            st.image(
                photo["img_src"],
                caption=f"📷 {photo['camera
