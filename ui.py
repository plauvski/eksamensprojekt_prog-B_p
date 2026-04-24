# ui.py (refactored)
import tkinter as tk

class UI:
    def __init__(self, controller, model):
        self.controller = controller
        self.model = model
        self.root = tk.Tk()
        self.root.title("Dijkstra simulation")
        
        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_columnconfigure(0, weight=1)
        self.root.state("zoomed")

        self.mode = tk.StringVar(value="place")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_canvas()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, width=150, bg="lightgray")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        tk.Label(self.sidebar, text="Mode", bg="lightgray").grid(row=0, column=0, pady=10, padx=10)
        
        tk.Radiobutton(self.sidebar, text="Place", variable=self.mode, value="place", bg="lightgray").grid(row=1, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="Connect", variable=self.mode, value="connect", bg="lightgray").grid(row=2, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="Delete", variable=self.mode, value="delete", bg="lightgray").grid(row=3, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="Start", variable=self.mode, value="start", bg="lightgray").grid(row=4, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="End", variable=self.mode, value="end", bg="lightgray").grid(row=5, column=0, sticky="w", padx=10)

        self.run_button = tk.Button(self.sidebar, text="Run", bg="lightgray", command=self.controller.run_dijkstra)
        self.run_button.grid(row=6, column=0, pady=20)

        self.dist_label = tk.Label(self.sidebar, text="Distance: -", bg="lightgray", justify="left")
        self.dist_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        
        self.path_label = tk.Label(self.sidebar, text="Path: -", bg="lightgray", justify="left")
        self.path_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")

    def create_canvas(self):
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nsew")
        self.canvas.bind("<Button-1>", lambda pos: self.controller.handle_click(pos, self.mode.get()))

    # Drawing methods
    def draw_city(self, city):
        city.draw_id = self.canvas.create_oval(city.x - 5, city.y - 5, city.x + 5, city.y + 5, fill="black")
        city.text_id = self.canvas.create_text(city.x, city.y - 10, text=city.name)

    def draw_edge(self, edge, city1, city2):
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

    def update_city_color(self, city):
        if city == self.model.start_city:
            self.canvas.itemconfig(city.draw_id, fill="green")
        elif city == self.model.end_city:
            self.canvas.itemconfig(city.draw_id, fill="red")
        else:
            self.canvas.itemconfig(city.draw_id, fill="black")

    def update_all_city_colors(self, model):
        for city in model.cities:
            self.update_city_color(city)

    def update_run_button(self, model):
        if model.start_city and model.end_city:
            self.run_button.config(bg="green")
        else:
            self.run_button.config(bg="lightgray")

    def draw_path(self, path):
        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]
            for edge in city1.edges:
                if edge.other(city1) == city2:
                    self.canvas.itemconfig(edge.line_id, fill="red", width=5)

    def reset_edges(self, model):
        for edge in model.edges:
            self.canvas.itemconfig(edge.line_id, fill="black", width=1)

    def show_result(self, distance, path_names):
        self.dist_label.config(text=f"Distance: {distance:.1f}")
        self.path_label.config(text=f"Path: \n{path_names}")

    def show_error(self, error):
        self.dist_label.config(text=error)
        self.path_label.config(text="")

    def run(self):
        self.root.mainloop()