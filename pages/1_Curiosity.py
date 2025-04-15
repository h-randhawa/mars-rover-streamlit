import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Curiosity Rover", layout="wide")
st.title("🛸 Curiosity Rover Photos")

API_KEY = "DEMO_KEY"
ROVER = "curiosity"

def get_manifest(rover):
    url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}?api_key={API_KEY}"
    return requests.get(url).json()["photo_manifest"]

def get_photos(rover, sol=None, earth_date=None, camera=None, page=1):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {"api_key": API_KEY, "page": page}
    if sol:
        params["sol"] = sol
    if earth_date:
        params["earth_date"] = earth_date
    if camera and camera != "ALL":
        params["camera"] = camera
    response = requests.get(url, params=params)
    return response.json()["photos"]

manifest = get_manifest(ROVER)

st.sidebar.subheader("Search Options")
query_type = st.sidebar.radio("Search by", ["Martian Sol", "Earth Date"])
camera = st.sidebar.selectbox("Camera", ["ALL"] + list({photo["camera"]["name"] for photo in get_photos(ROVER, sol=100)}))
page = st.sidebar.number_input("Page #", min_value=1, value=1)

if query_type == "Martian Sol":
    sol = st.sidebar.slider("Sol", 0, manifest["max_sol"])
    photos = get_photos(ROVER, sol=sol, camera=camera, page=page)
else:
    min_date = datetime.strptime(manifest["landing_date"], "%Y-%m-%d").date()
    max_date = datetime.strptime(manifest["max_date"], "%Y-%m-%d").date()
    earth_date = st.sidebar.date_input("Earth Date", min_value=min_date, max_value=max_date)
    photos = get_photos(ROVER, earth_date=earth_date, camera=camera, page=page)

st.subheader("Photos")

if photos:
    cols = st.columns(3)
    for i, photo in enumerate(photos):
        with cols[i % 3]:
            st.image(photo["img_src"], caption=f'{photo["camera"]["full_name"]} - Sol {photo["sol"]}', use_column_width=True)
else:
    st.warning("No photos found for this selection.")

st.markdown(f"""
**Launch Date**: {manifest['launch_date']}  
**Landing Date**: {manifest['landing_date']}  
**Status**: {manifest['status'].capitalize()}  
**Total Photos**: {manifest['total_photos']}  
""")
