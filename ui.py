import tkinter as tk

class UI:
    def __init__(self, app):
        self.app = app
        self.root = tk.Tk()
        self.root.title("Dijkstra simulation")
        
        # Allow resizing of window
        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_columnconfigure(0, weight=1)
        self.root.state("zoomed") # Fills screen

        # Default mode state 
        self.mode = tk.StringVar(value="place")

        # Layout
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Create UI
        self.create_sidebar()
        self.create_canvas()

    # UI creation methods
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, width=150, bg="lightgray")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        tk.Label(self.sidebar, text="Mode", bg="lightgray").grid(row=0, column=0, pady=10, padx=10)
        # Mode radiobuttons
        tk.Radiobutton(self.sidebar, text="Place", variable=self.mode, value="place", bg="lightgray").grid(row=1, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="Connect", variable=self.mode, value="connect", bg="lightgray").grid(row=2, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="Delete", variable=self.mode, value="delete", bg="lightgray").grid(row=3, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="Start", variable=self.mode, value="start", bg="lightgray").grid(row=4, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="End", variable=self.mode, value="end", bg="lightgray").grid(row=5, column=0, sticky="w", padx=10)

        # Run Dijkstra button
        self.run_button = tk.Button(self.sidebar, text="Run", bg="lightgray" , command=self.app.run_dijkstra)
        self.run_button.grid(row=6, column=0, pady=20)

        # Result labels
        self.dist_label = tk.Label(self.sidebar, text="Distance: -", bg="lightgray", justify="left")
        self.dist_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.path_label = tk.Label(self.sidebar, text="Path: -", bg="lightgray", justify="left")
        self.path_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")

    # Canvas creation
    def create_canvas(self):
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nsew")
        self.canvas.bind("<Button-1>", self.app.handle_click) # Binds left mousebutton to handle_click method

    """Colour update methods"""
    # Update colour of individual node 
    def update_city_color(self, city):
        if city == self.app.start_city:
            self.canvas.itemconfig(city.draw_id, fill="green")
        elif city == self.app.end_city:
            self.canvas.itemconfig(city.draw_id, fill="red")
        else:
            self.canvas.itemconfig(city.draw_id, fill="black")

    # Update colour of all nodes
    def update_all_city_colors(self):
        for city in self.app.cities:
            self.update_city_color(city)

    # Update colour of run button
    def update_run_button(self):
        if self.app.start_city and self.app.end_city:
            self.run_button.config(bg="green")
        else:
            self.run_button.config(bg="lightgray")

    # Draw/highlight shortest path
    def draw_path(self, path):
        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]
            for edge in city1.edges:
                if edge.other(city1) == city2:
                    self.canvas.itemconfig(edge.line_id, fill="red", width=5)

    # Reset edge colour
    def reset_edges(self):
        for edge in self.app.edges:
            self.canvas.itemconfig(edge.line_id, fill="black", width=1)

    # Run the window
    def run(self):
        self.root.mainloop()
