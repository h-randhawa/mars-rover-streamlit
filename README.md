![Build](https://github.com/h-randhawa/mars-rover-streamlit/actions/workflows/deploy.yml/badge.svg)
[![Docker](https://img.shields.io/badge/Docker-Image-blue)](https://github.com/h-randhawa/mars-rover-streamlit/pkgs/container/mars-rover-streamlit)

# 🚀 Mars Rover Explorer

A Streamlit web app that lets you explore real imagery sent from NASA’s Curiosity and Perseverance rovers on Mars. Get the latest photos, browse random sols, filter by camera, and learn cool facts about Mars — all from a beautiful interactive interface.

---

## Features

- **Latest Photos**
  - Instantly view the most recent images from both Curiosity and Perseverance.

- **Random Image Viewer**
  - Load random sols with available NAVCAM images and scroll through a photo slideshow.

- **Filter by Camera, Sol, or Earth Date**
  - Fine-tune your photo searches with Martian Sols, Earth dates, or rover cameras.

- **Daily Quote or Mars Fun Fact**
  - Toggle between motivational space quotes and interesting Mars trivia with a single click.

- **Rover Mission Summary**
  - View a stats table comparing launch date, landing date, latest photo info, and total images captured.

---

## Tech Stack

- **Streamlit** – Python framework for interactive dashboards  
- **NASA Mars Rover API** – Live photo and mission data  
- **Requests** – API communication  
- **Pandas** – Data processing  

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mars-rover-streamlit.git
cd mars-rover-streamlit
```
### 2. Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
### 3. Live App
🔗 [Launch Mars Rover Explorer](https://mars-rover-app-beeabctsgqv5seegv3lmba.streamlit.app/)
