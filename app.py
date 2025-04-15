import streamlit as st

st.set_page_config(page_title="Mars Rover Explorer", layout="wide")

st.image("https://mars.nasa.gov/layout/mars2020/images/PIA25681-FigureA-web.jpg", use_container_width=True)

st.title("🚀 Mars Rover Photo Explorer")
st.markdown("""
Welcome to the Mars Rover Explorer!

Select a rover from the sidebar to browse images taken on Mars.
You can explore photos by:
- Martian Sol (Martian day)
- Earth Date
- Camera type
""")
