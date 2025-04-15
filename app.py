import streamlit as st

# Set page config FIRST
st.set_page_config(
    page_title="Mars Rover Explorer",
    layout="wide",
    page_icon="🚀"
)

# Banner image
st.image("https://mars.nasa.gov/layout/mars2020/images/PIA25681-FigureA-web.jpg", use_container_width=True)

# Title & Intro
st.title("🚀 Mars Rover Photo Explorer")
st.markdown("""
Welcome to the **Mars Rover Explorer**, a web app that lets you explore high-resolution photos taken by NASA's rovers on the surface of Mars.

Use the sidebar to explore images from:
- 🛸 **Curiosity**
- 🛠️ **Opportunity**
- 🔧 **Spirit**
- 🧪 **Perseverance**

Each page allows you to:
- Search by **Martian Sol** or **Earth Date**
- Filter by **Rover Camera**
- View full-resolution images
- Learn about each rover's **mission status** and stats

This project uses real-time data from the official NASA Mars Rover Photos API.
""")

# Spacer
st.markdown("---")

# Optional: Link to NASA API
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://www.nasa.gov/sites/default/files/thumbnails/image/nasa-logo-web-rgb.png", width=60)
with col2:
    st.markdown("""
**Powered by [NASA's Open APIs](https://api.nasa.gov/)**  
Built with ❤️ using [Streamlit](https://streamlit.io)
""")
