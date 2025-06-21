import heapq
import tkinter as tk
from tkinter import ttk, messagebox
import folium
import webbrowser
import math  # Importing math for mathematical functions
import os  # To open the HTML file(file path manipulations)

# City distance data and coordinates (lat, lon)
city_data = {
    'New Delhi': {'lat': 28.6139, 'lon': 77.2090, 'neighbors': {'Agra': 200, 'Jaipur': 280}},
    'Agra': {'lat': 27.1767, 'lon': 78.0081, 'neighbors': {'New Delhi': 200, 'Jaipur': 240, 'Lucknow': 330}},
    'Jaipur': {'lat': 26.9124, 'lon': 75.7873, 'neighbors': {'New Delhi': 280, 'Agra': 240, 'Udaipur': 650, 'Jodhpur': 600}},
    'Lucknow': {'lat': 26.8467, 'lon': 80.9462, 'neighbors': {'Agra': 330, 'Varanasi': 320}},
    'Udaipur': {'lat': 24.5854, 'lon': 73.7125, 'neighbors': {'Jaipur': 650, 'Jodhpur': 250}},
    'Varanasi': {'lat': 25.3176, 'lon': 82.9739, 'neighbors': {'Lucknow': 320, 'Patna': 230}},
    'Jodhpur': {'lat': 26.2389, 'lon': 73.0243, 'neighbors': {'Jaipur': 600, 'Udaipur': 250}},
    'Patna': {'lat': 25.5941, 'lon': 85.1376, 'neighbors': {'Varanasi': 230, 'Kolkata': 600}},
    'Kolkata': {'lat': 22.5726, 'lon': 88.3639, 'neighbors': {'Patna': 600, 'Howrah': 15}},
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'neighbors': {'Pune': 150, 'Nashik': 170}},
    'Pune': {'lat': 18.5204, 'lon': 73.8567, 'neighbors': {'Mumbai': 150, 'Nashik': 210}},
    'Nashik': {'lat': 19.9975, 'lon': 73.7898, 'neighbors': {'Mumbai': 170, 'Pune': 210}},
    'Howrah': {'lat': 22.5958, 'lon': 88.2636, 'neighbors': {'Kolkata': 15}},
}

# Global variable to store the final path
global_path = []

# A* search algorithm to find the optimal route
def astar_search(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}  #cost from starting city to itself as 0(actual cost)
    f_score = {start: haversine_distance(start, goal)}  #total cost to reach the goal city(estimated cost)

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor, distance in city_data[current]['neighbors'].items():
            tentative_g_score = g_score[current] + distance
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + haversine_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

# Haversine distance formula to calculate the straight-line distance between two cities
def haversine_distance(city1, city2):
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = city_data[city1]['lat'], city_data[city1]['lon']
    lat2, lon2 = city_data[city2]['lat'], city_data[city2]['lon']
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Reconstruct the optimal path
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# Display the route on a map using folium
def display_route_on_map(path):
    if not path:
        messagebox.showerror("Error", "No path to display.")
        return

    start_city = path[0]
    m = folium.Map(location=[city_data[start_city]['lat'], city_data[start_city]['lon']], zoom_start=6)

    # Add markers and lines between cities
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        folium.Marker(location=[city_data[start]['lat'], city_data[start]['lon']], popup=start).add_to(m)
        folium.Marker(location=[city_data[end]['lat'], city_data[end]['lon']], popup=end).add_to(m)
        folium.PolyLine(locations=[
            [city_data[start]['lat'], city_data[start]['lon']],
            [city_data[end]['lat'], city_data[end]['lon']]
        ], color="blue").add_to(m)

    # Save the map to a file
    map_file = "route.html"
    m.save(map_file)
    
    # Open the map in a web browser
    webbrowser.open('file://' + os.path.realpath(map_file))

# GUI for user interaction
def start_gui():
    def find_route():
        start_point = start_combo.get()
        end_point = end_combo.get()

        if start_point and end_point:
            global global_path  # Use the global path variable
            global_path = astar_search(start_point, end_point)  # Store the path globally
            if global_path:
                path_str = " -> ".join(global_path)
                messagebox.showinfo("Optimal Path", f"Optimal path: {path_str}")
                show_map_button.config(state="normal")  # Enable the show map button
            else:
                messagebox.showwarning("No Path Found", "Could not find a path between the selected points.")
        else:
            messagebox.showerror("Error", "Invalid start or end point selected.")

    # Create the main window
    root = tk.Tk()
    root.title("Smart Traffic Routing System")
    root.geometry("500x350")
    root.configure(bg="#F0F0F0")

    # Title label
    title_label = tk.Label(root, text="Smart Traffic Routing System", font=("Arial", 16, "bold"), bg="#F0F0F0", fg="#333")
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Labels for start and end points
    start_label = tk.Label(root, text="Select Start Point:", font=("Arial", 12), bg="#F0F0F0")
    start_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    end_label = tk.Label(root, text="Select End Point:", font=("Arial", 12), bg="#F0F0F0")
    end_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    # Combobox for selecting start and end points
    options = list(city_data.keys())
    start_combo = ttk.Combobox(root, values=options, state='readonly', font=("Arial", 12), width=25)
    start_combo.grid(row=1, column=1, padx=10, pady=10)
    start_combo.current(0)

    end_combo = ttk.Combobox(root, values=options, state='readonly', font=("Arial", 12), width=25)
    end_combo.grid(row=2, column=1, padx=10, pady=10)
    end_combo.current(1)

    # Button to find the route
    find_button = tk.Button(root, text="Find Route", command=find_route, font=("Arial", 12), bg="#4CAF50", fg="white", width=20)
    find_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Button to show the map (initially disabled)
    show_map_button = tk.Button(root, text="Show Map", command=lambda: display_route_on_map(global_path) if global_path else None, state="disabled", font=("Arial", 12), bg="#2196F3", fg="white", width=20)
    show_map_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
