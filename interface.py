import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt
from data import communes, hospitals
from maincode import Problem, bfs, dfs, astar, steepest_ascent_hill_climbing, stochastic_hill_climbing

def get_unique_departments(hospitals):
    departments = set()
    for hospital in hospitals.values():
        departments.update(hospital["departments"])
    return list(departments)

def update_communes(*args):
    selected_region = region_dropdown.get().lower()
    filtered_communes = [commune for commune, details in communes.items() if details['region'] == selected_region]
    commune_dropdown['values'] = filtered_communes
    if filtered_communes:
        commune_dropdown.current(0)

root = tk.Tk()
root.title("Path Visualization")
root.configure(bg="lightblue")  # Set the background color for the entire window

# Create frames
menu_frame = tk.Frame(root, bg="lightgray", padx=20, pady=20)
menu_frame.pack(side=tk.LEFT, fill=tk.Y)

graph_frame = tk.Frame(root, bg="lightblue")  # Set the background color for the graph frame
graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
graph_frame.grid_rowconfigure(0, weight=1)
graph_frame.grid_columnconfigure(0, weight=1)

# Create frames for the dropdown menus
region_frame = tk.Frame(menu_frame, bg="lightgray")
region_frame.pack(pady=5)
commune_frame = tk.Frame(menu_frame, bg="lightgray")
commune_frame.pack(pady=5)
speciality_frame = tk.Frame(menu_frame, bg="lightgray")
speciality_frame.pack(pady=5)
search_frame = tk.Frame(menu_frame, bg="lightgray")
search_frame.pack(pady=5)

# Create the dropdown menus with larger fonts
region_options = ["East", "Centre", "West"]  # Region options
commune_options = list(communes.keys())
speciality_options = get_unique_departments(hospitals)
search_options = ["BFS", "DFS", "A*", "Steepest Ascent Hill Climbing", "Stochastic Hill Climbing"]

selected_region = tk.StringVar()
region_label = tk.Label(region_frame, text="Select Region:", font=("Arial", 20, "bold"), fg="blue", bg="lightgray")
region_label.pack(side=tk.LEFT)
region_dropdown = ttk.Combobox(region_frame, textvariable=selected_region, values=region_options, font=("Arial", 20))
region_dropdown.pack(side=tk.LEFT, padx=5)

selected_commune = tk.StringVar()
commune_label = tk.Label(commune_frame, text="Select Commune:", font=("Arial", 20, "bold"), fg="green", bg="lightgray")
commune_label.pack(side=tk.LEFT)
commune_dropdown = ttk.Combobox(commune_frame, textvariable=selected_commune, values=[], font=("Arial", 20))
commune_dropdown.pack(side=tk.LEFT, padx=5)

selected_speciality = tk.StringVar()
speciality_label = tk.Label(speciality_frame, text="Select Speciality:", font=("Arial", 20, "bold"), fg="red", bg="lightgray")
speciality_label.pack(side=tk.LEFT)
speciality_dropdown = ttk.Combobox(speciality_frame, textvariable=selected_speciality, values=speciality_options, font=("Arial", 20))
speciality_dropdown.pack(side=tk.LEFT, padx=5)

selected_search = tk.StringVar()
search_label = tk.Label(search_frame, text="Select Search:", font=("Arial", 20, "bold"), fg="purple", bg="lightgray")
search_label.pack(side=tk.LEFT)
search_dropdown = ttk.Combobox(search_frame, textvariable=selected_search, values=search_options, font=("Arial", 20))
search_dropdown.pack(side=tk.LEFT, padx=5)

# Create a matplotlib figure
fig = plt.figure(figsize=(6, 4))

# Add the canvas for the graph to the graph_frame
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# Hide the graph frame initially
graph_frame.grid_remove()

def draw_graph(path, goal_state):
    global canvas

    # Convert tuples to strings in the path list
    path = [str(node) for node in path]

    # Clear the previous graph and canvas
    plt.clf()
    if canvas:
        canvas.get_tk_widget().pack_forget()

    # Create a NetworkX graph from the path
    G = nx.Graph()
    G.add_edges_from(zip(path, path[1:]))

    # Assign colors to the nodes
    node_colors = ['green' if node == goal_state else 'skyblue' for node in G.nodes]

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=200, font_size=18)

    # Create a new canvas for the graph
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")


def calculate_path_distance(path, problem):
    total_distance = 0
    for i in range(len(path) - 1):
        state = path[i]
        next_state = path[i + 1]
        if state in problem.communes and next_state in problem.communes[state]["neighbors"]:
            total_distance += problem.communes[state]["neighbors"][next_state]
    return total_distance

# Create a label to display the distance
distance_label = tk.Label(menu_frame, text="", font=("Arial", 20, "bold"), bg="skyblue")
distance_label.pack(pady=10)

def find_path():
    commune = selected_commune.get()
    speciality = selected_speciality.get()
    search = selected_search.get()

    initial_state = commune
    specialty_needed = speciality
    problem = Problem(initial_state, specialty_needed, communes, hospitals)

    if search == "BFS":
        path, distance = bfs(problem)
    elif search == "DFS":
        path, distance = dfs(problem)
    elif search == "A*":
        path, distance = astar(problem)
    elif search == "Steepest Ascent Hill Climbing":
        path, distance = steepest_ascent_hill_climbing(problem)
    elif search == "Stochastic Hill Climbing":
        path, distance = stochastic_hill_climbing(problem, 20)
    else:
        path, distance = [], 0

    # Update the distance label
    distance_label.config(text=f"Total Distance: {distance}")

    # Assume the last node in the path is the goal state
    goal_state = path[-1] if path else None

    # Draw the graph with the resulting path and the goal state
    draw_graph(path, goal_state)


# Bind the find_path function to a button
find_path_button = tk.Button(menu_frame, text="Find Path", font=("Arial", 20, "bold"), command=find_path)
find_path_button.pack(pady=10)

# Bind the region selection change to update the commune options
selected_region.trace('w', update_communes)

# Run the Tkinter event loop
root.mainloop()
