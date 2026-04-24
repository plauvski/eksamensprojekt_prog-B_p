import tkinter as tk 

class UI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Transport Network Simulator")
        self.root.state("zoomed")
        
        # Configure root to expand
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main frame with left panel and canvas
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Left control panel
        self.left_panel = tk.Frame(self.main_frame, bg="lightgray", width=200)
        self.left_panel.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        self.left_panel.grid_propagate(False)
        
        # Title
        title = tk.Label(self.left_panel, text="Controls", font=("Arial", 14, "bold"), bg="lightgray")
        title.pack(pady=10)
        
        # Mode selection
        tk.Label(self.left_panel, text="Mode:", bg="lightgray").pack(pady=(10, 0))
        self.mode = tk.StringVar(value="place")
        
        modes = [("Place City", "place"), ("Connect", "connect"), ("Delete", "delete"), ("Start", "start"), ("End", "end")]
        
        for label, value in modes:
            tk.Radiobutton(self.left_panel, text=label, variable=self.mode, value=value, bg="lightgray").pack(anchor="w", padx=10)
        
        # Buttons
        tk.Label(self.left_panel, text="\nActions:", bg="lightgray").pack(pady=(20, 10))
        
        self.run_button = tk.Button(self.left_panel, text="Run Dijkstra", bg="lightgray", command=self.on_run_dijkstra)
        self.run_button.pack(pady=5, padx=10, fill="x")
        self.set_run_button_enabled(False)
        
        clear_btn = tk.Button(self.left_panel, text="Clear All", command=self.on_clear_all)
        clear_btn.pack(pady=5, padx=10, fill="x")
        
        # Results display
        tk.Label(self.left_panel, text="\nResults:", bg="lightgray").pack(pady=(20, 10))
        
        self.dist_label = tk.Label(self.left_panel, text="Distance: -", bg="white", wraplength=180, justify="left")
        self.dist_label.pack(pady=5, padx=10, fill="x")
        
        self.path_label = tk.Label(self.left_panel, text="Path: -", bg="white", wraplength=180, justify="left", height=4)
        self.path_label.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Create canvas
        self.create_canvas()

    def create_canvas(self):
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nsew")
        
        def on_click(event):
            # Kalder controller, IKKE model
            self.controller.handle_click(event, self.mode.get())
        
        self.canvas.bind("<Button-1>", on_click)

    # Display methods
    def display_city(self, city):
        city.draw_id = self.canvas.create_oval(city.x - 5, city.y - 5,  city.x + 5, city.y + 5, fill="black")
        city.text_id = self.canvas.create_text(city.x, city.y - 10, text=city.name)

    # Update all cities based on data from controller
    def display_all_cities(self, cities_data):
        for city in cities_data['cities']:
            self.update_city_color(city, cities_data['start_city'], cities_data['end_city'])

    def update_city_color(self, city, start_city, end_city):
        if city == start_city:
            self.canvas.itemconfig(city.draw_id, fill="green")
        elif city == end_city:
            self.canvas.itemconfig(city.draw_id, fill="red")
        else:
            self.canvas.itemconfig(city.draw_id, fill="black")

    def display_edge(self, edge, city1, city2):
        edge.line_id = self.canvas.create_line(city1.x, city1.y, city2.x, city2.y)
        mid_x = (city1.x + city2.x) / 2
        mid_y = (city1.y + city2.y) / 2
        edge.text_id = self.canvas.create_text(mid_x, mid_y, text=f"{edge.distance:.1f}", fill="blue")

    def erase_city(self, city):
        self.canvas.delete(city.draw_id)
        self.canvas.delete(city.text_id)

    def erase_edge(self, edge):
        self.canvas.delete(edge.line_id)
        self.canvas.delete(edge.text_id)

    def highlight_city(self, city):
        self.canvas.itemconfig(city.draw_id, fill="blue")

    def highlight_path(self, path):
        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]
            for edge in city1.edges:
                if edge.other(city1) == city2:
                    self.canvas.itemconfig(edge.line_id, fill="red", width=5)

    def reset_edges(self, edges):
        for edge in edges:
            self.canvas.itemconfig(edge.line_id, fill="black", width=1)

    def show_error(self, error):
        self.dist_label.config(text=error)
        self.path_label.config(text="")

    def show_result(self, distance, path_names):
        self.dist_label.config(text=f"Distance: {distance:.1f}")
        self.path_label.config(text=f"Path: \n{path_names}")

    def set_run_button_enabled(self, enabled):
        self.run_button.config(bg="green" if enabled else "lightgray", state="normal" if enabled else "disabled")

    # Called when "Run Dijkstra"-button is pressed
    def on_run_dijkstra(self):
        self.controller.run_dijkstra()
    
    # Clear all cities and edges from canvas
    def on_clear_all(self):
        self.canvas.delete("all")
        self.dist_label.config(text="Distance: -")
        self.path_label.config(text="Path: -")
        self.controller.clear_all()

    def run(self):
        self.root.mainloop()