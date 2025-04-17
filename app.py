import streamlit as st
import requests
import random
import pandas as pd
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Mars Rover Explorer", layout="wide")
st.title("🚀 Welcome to the Mars Rover Explorer")
st.caption("Explore stunning images, live stats, and facts from NASA’s active Mars rover missions.")

with st.container():
    st.markdown("## Welcome to the Mars Rover Explorer App!")

    st.markdown("""
    This interactive dashboard lets you explore the latest imagery, data, and fun facts from NASA’s active Mars rover missions — **Curiosity** and **Perseverance**.

    Here's what you can do:
    - 🖼️ **View random photos** taken by Mars rovers from the surface of the Red Planet  
    - 📊 **Compare rover stats**, including launch dates, number of sols, and photos taken  
    - 🔁 **Toggle between daily quotes and fun Mars facts** to stay inspired or informed  
    - 🌡️ **Check real weather data** from the InSight lander, including temperature and wind 

    Use the sidebar to navigate through different sections of the app.  
    Whether you're here for science, inspiration, or fun — you're in the right place.
    """)

API_KEY = st.secrets["api"]["nasa_key"]
ROVERS = ["curiosity", "perseverance"]

# ---------------- QUOTE OR FUN FACT W/ SOURCES ----------------
quotes = [
    {
        "text": "“Mars is there, waiting to be reached.”",
        "author": "Buzz Aldrin",
        "desc": "Apollo 11 astronaut and the second human to walk on the Moon.",
        "source": "https://www.nasa.gov/sites/default/files/atoms/files/buzz_aldrin_biography.pdf"
    },
    {
        "text": "“Curiosity is the essence of our existence.”",
        "author": "Gene Cernan",
        "desc": "Commander of Apollo 17, the last person to walk on the Moon.",
        "source": "https://www.nasa.gov/astronautprofiles/cernan/"
    },
    {
        "text": "“Somewhere, something incredible is waiting to be known.”",
        "author": "Carl Sagan",
        "desc": "Astronomer, astrophysicist, and host of the original *Cosmos* series.",
        "source": "https://www.carlsagan.com/"
    }
]

fun_facts = [
    {
        "fact": "🔎 The Curiosity rover has traveled over 18 miles across Gale Crater.",
        "source": "https://mars.nasa.gov/msl/mission/overview/"
    },
    {
        "fact": "🧪 Perseverance is the first rover to collect and cache samples of Martian rock and soil.",
        "source": "https://mars.nasa.gov/mars2020/"
    },
    {
        "fact": "🚁 Ingenuity became the first aircraft to fly on another planet!",
        "source": "https://mars.nasa.gov/technology/helicopter/"
    },
    {
        "fact": "📡 Curiosity and Perseverance communicate with Earth via orbiters like MRO and MAVEN.",
        "source": "https://mars.nasa.gov/faq/#communicating"
    },
    {
        "fact": "⚡ Perseverance uses a nuclear power source called an MMRTG.",
        "source": "https://mars.nasa.gov/mars2020/spacecraft/rover/power/"
    }
]

st.sidebar.markdown("🧠 **Inspire or Inform?**")
display_mode = st.sidebar.radio("Show me a...", ["Quote", "Fun Fact"])

# Reset if switching modes
if "last_display_mode" not in st.session_state:
    st.session_state.last_display_mode = display_mode

if display_mode != st.session_state.last_display_mode:
    st.session_state.quote_or_fact = None
    st.session_state.refresh_quote_fact = True
    st.session_state.last_display_mode = display_mode

# Set up session state
if "quote_or_fact" not in st.session_state:
    st.session_state.quote_or_fact = None
if "refresh_quote_fact" not in st.session_state:
    st.session_state.refresh_quote_fact = True  # Load one on first render

def get_new_entry():
    if display_mode == "Quote":
        st.session_state.quote_or_fact = random.choice(quotes)
    else:
        st.session_state.quote_or_fact = random.choice(fun_facts)
    st.session_state.refresh_quote_fact = False

# Reroll button
if st.button("🔁 Get Another Quote or Fact"):
    st.session_state.refresh_quote_fact = True

# Generate if needed
if st.session_state.quote_or_fact is None or st.session_state.refresh_quote_fact:
    get_new_entry()

# Display result
if display_mode == "Quote":
    selected = st.session_state.quote_or_fact
    st.markdown(f"> 💬 *{selected['text']}*  \n**— {selected['author']}**")
    st.caption(f"**{selected['author']}**: {selected['desc']}  \n🔗 [Source]({selected['source']})")
else:
    selected = st.session_state.quote_or_fact
    st.markdown(f"> 🤓 {selected['fact']}")
    st.caption(f"🔗 [Source]({selected['source']})")


# ---------------- COUNTDOWN TO NEXT OPPOSITION ----------------
#next_opposition = datetime(2026, 12, 19)
#today = datetime.now()
#days_left = (next_opposition - today).days
#st.markdown(f"🪐 **Days until next Mars–Earth opposition:** `{days_left}` days")

# ---------------- MISSION STATS SUMMARY ----------------
@st.cache_data(show_spinner=False)
def get_manifest(rover):
    url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}?api_key={API_KEY}"
    response = requests.get(url)
    return response.json()["photo_manifest"]

st.subheader("📊 Mission Stats Summary")

summary_data = []
for rover in ROVERS:
    manifest = get_manifest(rover)
    summary_data.append({
        "Rover": manifest["name"],
        "Launch Date": manifest["launch_date"],
        "Landing Date": manifest["landing_date"],
        "Status": manifest["status"].capitalize(),
        "Max Sol": manifest["max_sol"],
        "Max Earth Date": manifest["max_date"],
        "Total Photos": manifest["total_photos"]
    })

df_summary = pd.DataFrame(summary_data)
st.dataframe(df_summary, use_container_width=True)
