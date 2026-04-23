import tkinter as tk
import math

def calculate_distance(city1, city2):
    return math.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2)

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.edges = []
        self.draw_id = None
        self.text_id = None

    def add_edge(self, edge):
        self.edges.append(edge)

    # format for print of City-object
    def __repr__(self):
        return f"{self.name} ({self.x}, {self.y})"

class Edge:
    def __init__(self, city1, city2, distance):
        self.city1 = city1
        self.city2 = city2
        self.distance = distance
        self.line_id = None
        self.text_id = None

    def connects(self, city):
        return self.city1 == city or self.city2 == city

    def other(self, city):
        if city == self.city1:
            return self.city2
        elif city == self.city2:
            return self.city1
        return None

class App:
    def __init__(self):
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

        self.create_sidebar()
        self.create_canvas()

        # Data
        self.cities = []
        self.city_count = 0
        self.selected_city = None  # used for connections
        self.edges = []

    # UI creation methods
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, width=150, bg="lightgray")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        tk.Label(self.sidebar, text="Mode", bg="lightgray").grid(row=0, column=0, pady=10, padx=10)
        
        # Mode radiobuttons
        tk.Radiobutton(self.sidebar, text="Place", variable=self.mode, value="place", bg="lightgray").grid(row=1, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="Connect", variable=self.mode, value="connect", bg="lightgray").grid(row=2, column=0, sticky="w", padx=10)
        tk.Radiobutton(self.sidebar, text="Delete", variable=self.mode, value="delete", bg="lightgray").grid(row=3, column=0, sticky="w", padx=10)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nsew")
        self.canvas.bind("<Button-1>", self.handle_click) # Binds left mousebutton to handle_click method

    # Click handling
    def handle_click(self, pos):
        mode = self.mode.get()
        if mode == "place":
            self.place_city(pos)
        elif mode == "connect":
            self.connect_city(pos)
        elif mode == "delete":
            self.delete_city(pos)

    # Other features
    def place_city(self, pos):
        name = f"C{self.city_count}"
        city = City(name, pos.x, pos.y)
        self.cities.append(city)
        # Draw city
        city.draw_id = self.canvas.create_oval(pos.x - 5, pos.y - 5, pos.x + 5, pos.y + 5, fill="black")
        city.text_id = self.canvas.create_text(pos.x, pos.y - 10, text=name)

        print(city)
        self.city_count += 1

    # Find/select city method
    def find_city_at_position(self, x, y):
        for city in self.cities:
            if abs(city.x - x) < 10 and abs(city.y - y) < 10:
                return city
        return None

    # Connect two cities
    def connect_city(self, pos):
        city = self.find_city_at_position(pos.x, pos.y)
        if not city:
            return
        if self.selected_city is None:
            self.selected_city = city
            # Highlight selected city with blue
            self.canvas.itemconfig(city.draw_id, fill="blue")
        else:
            # Create weighted edge
            distance = calculate_distance(self.selected_city, city)
            edge = Edge(self.selected_city, city, distance)
            # Draw connection
            edge.line_id = self.canvas.create_line(self.selected_city.x, self.selected_city.y, city.x, city.y)
            # Add edge to both cities' edge lists
            self.selected_city.add_edge(edge)
            city.add_edge(edge)
            # Add to "global" edge list
            self.edges.append(edge)
            # Display weight next to edge
            mid_x = (self.selected_city.x + city.x) / 2
            mid_y = (self.selected_city.y + city.y) / 2
            edge.text_id = self.canvas.create_text(
                mid_x, mid_y, text=f"{distance:.1f}", fill="blue") # .1f = 1 decimal point

            # Reset colour
            self.canvas.itemconfig(self.selected_city.draw_id, fill="black")
            self.selected_city = None

    # Delete a city
    def delete_city(self, pos):
        city = self.find_city_at_position(pos.x, pos.y)
        if not city:
            return
        # Delete all edges connected to city 
        for edge in city.edges[:]:  # Copy of list
            self.delete_edge(edge)
        # Delete city from list
        self.cities.remove(city)
        # Remove from canvas
        self.canvas.delete(city.draw_id)
        self.canvas.delete(city.text_id)

        print(f"Deleted {city.name}")
    
    def delete_edge(self, edge):
        # Remove from canvas
        self.canvas.delete(edge.line_id)
        # Remove edge from both cities' edge lists
        edge.city1.edges.remove(edge)
        edge.city2.edges.remove(edge)
        # Remove from "global" edge list
        self.edges.remove(edge)
        self.canvas.delete(edge.text_id)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()