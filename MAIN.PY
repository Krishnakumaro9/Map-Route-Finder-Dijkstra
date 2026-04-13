from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import heapq

# ---------------- GRAPH ----------------
graph = {
    'Delhi': {'Jaipur': 280, 'Lucknow': 550, 'Chandigarh': 250},
    'Jaipur': {'Delhi': 280, 'Mumbai': 1150},
    'Lucknow': {'Delhi': 550, 'Varanasi': 320},
    'Chandigarh': {'Delhi': 250},
    'Mumbai': {'Jaipur': 1150, 'Pune': 150},
    'Pune': {'Mumbai': 150, 'Goa': 450},
    'Goa': {'Pune': 450},
    'Varanasi': {'Lucknow': 320}
}

# ---------------- POSITIONS ----------------
positions = {
    'Delhi': (500, 250),
    'Jaipur': (400, 300),
    'Lucknow': (600, 270),
    'Chandigarh': (500, 150),
    'Mumbai': (400, 450),
    'Pune': (450, 520),
    'Goa': (450, 600),
    'Varanasi': (700, 320)
}

# ---------------- DIJKSTRA ----------------
def dijkstra(start, end):
    pq = [(0, start)]
    dist = {n: float('inf') for n in graph}
    dist[start] = 0
    parent = {}

    while pq:
        cost, node = heapq.heappop(pq)

        for nbr in graph[node]:
            new_cost = cost + graph[node][nbr]
            if new_cost < dist[nbr]:
                dist[nbr] = new_cost
                parent[nbr] = node
                heapq.heappush(pq, (new_cost, nbr))

    path = []
    node = end
    while node != start:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()

    return path, dist[end]

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Map Route Finder")
root.geometry("1000x650")
root.configure(bg="#0f172a")

# ---------------- TOP FRAME ----------------
frame = tk.Frame(root, bg="#0f172a")
frame.pack(pady=5)

cities = list(graph.keys())

tk.Label(frame, text="Start City", bg="#0f172a", fg="#38bdf8",
         font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10)

start_var = tk.StringVar()
start_dropdown = ttk.Combobox(frame, textvariable=start_var,
                              values=cities, state="readonly")
start_dropdown.grid(row=1, column=0, padx=10)

tk.Label(frame, text="End City", bg="#0f172a", fg="#38bdf8",
         font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10)

end_var = tk.StringVar()
end_dropdown = ttk.Combobox(frame, textvariable=end_var,
                            values=cities, state="readonly")
end_dropdown.grid(row=1, column=1, padx=10)

# ---------------- CANVAS ----------------
canvas = tk.Canvas(root, width=1000, height=650, highlightthickness=0)
canvas.pack()

# Load and resize image
img = Image.open("map.png")
img = img.resize((1000, 650))
map_img = ImageTk.PhotoImage(img)

# ---------------- DRAW MAP ----------------
def draw_map(start=None, end=None):
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=map_img)

    for city, (x, y) in positions.items():

        if city == start:
            color = "#22c55e"
        elif city == end:
            color = "#ef4444"
        else:
            color = "#facc15"

        canvas.create_oval(x-6, y-6, x+6, y+6,
                           fill=color, outline="white", width=2)

        canvas.create_text(x, y-12,
                           text=city,
                           fill="black",
                           font=("Arial", 9, "bold"))

draw_map()

# ---------------- FIND ROUTE ----------------
def find_route():
    start = start_var.get()
    end = end_var.get()

    if start == "" or end == "":
        result.set("⚠️ Please select both cities")
        return

    if start == end:
        result.set("⚠️ Start and End cannot be same")
        return

    path, cost = dijkstra(start, end)

    draw_map(start, end)

    for i in range(len(path)-1):
        x1, y1 = positions[path[i]]
        x2, y2 = positions[path[i+1]]

        canvas.create_line(x1, y1, x2, y2,
                           fill="#60a5fa", width=10, smooth=True)

        canvas.create_line(x1, y1, x2, y2,
                           fill="#2563eb", width=5, smooth=True)

    result.set(f"{' → '.join(path)} | Distance: {cost} km")

# ---------------- BUTTON ----------------
tk.Button(frame, text="Find Route",
          bg="#22c55e", fg="black",
          font=("Arial", 10, "bold"),
          command=find_route).grid(row=1, column=2, padx=15)

# ---------------- RESULT ----------------
result = tk.StringVar()
tk.Label(root, textvariable=result,
         bg="#0f172a", fg="#22c55e",
         font=("Arial", 12, "bold")).pack(pady=5)

root.mainloop()