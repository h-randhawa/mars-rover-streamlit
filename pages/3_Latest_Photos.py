import streamlit as st
import requests
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Latest Mars Photos", layout="wide")
st.title("🛰️ Latest Photos from Mars Rovers")
st.caption("See the most recent images sent back by NASA's Perseverance and Curiosity rovers.")

API_KEY = st.secrets["api"]["nasa_key"]
ROVERS = ["curiosity", "perseverance"]

# Correct camera by rover
CAMERA_BY_ROVER = {
    "curiosity": "NAVCAM",
    "perseverance": "NAVCAM_LEFT"
}
# ---------------- HELPERS ----------------
@st.cache_data(show_spinner=False)
def get_latest_photos(rover):
    # Get manifest to find the most recent Earth date
    manifest_url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}?api_key={API_KEY}"
    manifest_response = requests.get(manifest_url).json()
    max_date = manifest_response["photo_manifest"]["max_date"]

    # Get latest photos for that Earth date
    photos_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        "api_key": API_KEY,
        "earth_date": max_date
    }
    photos_response = requests.get(photos_url, params=params).json()
    return photos_response.get("photos", []), max_date

# ---------------- DISPLAY ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛠️ Perseverance")
    perseverance_photos, date_perseverance = get_latest_photos("perseverance")
    st.markdown(f"**Latest Earth Date:** `{date_perseverance}`")
    if perseverance_photos:
        for photo in perseverance_photos[:5]:
            st.image(photo["img_src"], caption=f"{photo['camera']['full_name']} — Sol {photo['sol']}", use_container_width=True)
    else:
        st.warning("No photos found for Perseverance.")

with col2:
    st.subheader("🧪 Curiosity")
    curiosity_photos, date_curiosity = get_latest_photos("curiosity")
    st.markdown(f"**Latest Earth Date:** `{date_curiosity}`")
    if curiosity_photos:
        for photo in curiosity_photos[:5]:
            st.image(photo["img_src"], caption=f"{photo['camera']['full_name']} — Sol {photo['sol']}", use_container_width=True)
    else:
        st.warning("No photos found for Curiosity.")

# ---------------- IMAGE VIEWER ----------------
st.subheader("🖼️ Rover Photo Viewer")

# Session state setup
if "img_index" not in st.session_state:
    st.session_state.img_index = 0
if "photos" not in st.session_state:
    st.session_state.photos = []
if "current_rover" not in st.session_state:
    st.session_state.current_rover = "curiosity"
if "load_new_images" not in st.session_state:
    st.session_state.load_new_images = True
if "nav_command" not in st.session_state:
    st.session_state.nav_command = None

selected_rover = st.selectbox("Choose a Rover for Random Photo", ["Curiosity", "Perseverance"])
selected_rover_key = selected_rover.lower()
camera = CAMERA_BY_ROVER[selected_rover_key]

@st.cache_data(show_spinner=False)
def get_valid_sols(rover, camera):
    url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}?api_key={API_KEY}"
    response = requests.get(url)
    manifest = response.json()["photo_manifest"]["photos"]
    return [entry["sol"] for entry in manifest if camera in entry["cameras"]]

@st.cache_data(show_spinner=True)
def get_rover_photos(rover, sol, camera):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        "api_key": API_KEY,
        "sol": sol,
        "camera": camera
    }
    response = requests.get(url, params=params)
    return response.json().get("photos", [])

# Handle button logic
if st.button("🔄 Load New Random Sol"):
    st.session_state.load_new_images = True
    st.session_state.nav_command = None

# Nav buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Previous"):
        st.session_state.nav_command = "prev"
with col2:
    if st.button("Next ➡️"):
        st.session_state.nav_command = "next"

# Load new images if needed
if st.session_state.load_new_images:
    valid_sols = get_valid_sols(selected_rover_key, camera)
    if valid_sols:
        sol = random.choice(valid_sols)
        photos = get_rover_photos(selected_rover_key, sol, camera)
        if photos:
            st.session_state.photos = photos
            st.session_state.img_index = 0
            st.session_state.current_rover = selected_rover
            st.success(f"Loaded {len(photos)} {camera} photos from Sol {sol}")
        else:
            st.warning(f"No {camera} photos found on Sol {sol}. Try again!")
    else:
        st.error(f"No valid sols found for {selected_rover} using {camera}.")
    st.session_state.load_new_images = False

# Navigate images
if st.session_state.nav_command == "prev" and st.session_state.img_index > 0:
    st.session_state.img_index -= 1
if st.session_state.nav_command == "next" and st.session_state.img_index < len(st.session_state.photos) - 1:
    st.session_state.img_index += 1
st.session_state.nav_command = None

# Display current image
if st.session_state.photos:
    photo = st.session_state.photos[st.session_state.img_index]
    st.image(
        photo["img_src"],
        caption=f"📷 {camera} — {st.session_state.current_rover} — Sol {photo['sol']}",
        use_container_width=True
    )
else:
    st.info("Click **'Load New Random Sol'** to start exploring photos.")
