# Smart-Traffic-Routing-System
# 🚦 Smart Traffic Routing System

This project is a **GUI-based Smart Traffic Routing System** developed using Python. It helps users find the optimal path between two Indian cities using the **A* (A-star) search algorithm**, and visualizes the route using **Folium** maps.

---

## ✨ Features

- 🔍 Calculates shortest route using A* search algorithm
- 🗺️ Visual route visualization on an interactive map
- 📍 Includes major cities with real geolocation coordinates
- 🖥️ User-friendly GUI built with Tkinter
- 📦 Lightweight and easy to use

---

## 🧠 Algorithm Used

The project uses the **A* search algorithm** for pathfinding. It combines the actual travel distance (g-cost) with a heuristic (Haversine distance) to efficiently find the shortest path.

---

## 🛠️ Tech Stack

- **Python**
- **Tkinter** – for GUI
- **Folium** – for interactive maps
- **heapq** – for priority queue in A*
- **math** – for Haversine formula

---

## 🏙️ Cities Covered

Includes major Indian cities like:
- New Delhi
- Agra
- Jaipur
- Mumbai
- Pune
- Varanasi
- Kolkata
- And more...

---

## 🚀 How to Run


   git clone https://github.com/your-username/smart-traffic-routing.git
   cd smart-traffic-routing
   pip install folium
   python main.py
