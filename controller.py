from model import City, Edge, calculate_distance, dijkstra

class Controller:
    def __init__(self, app):
        self.app = app

    # Click handling
    def handle_click(self, pos):
        mode = self.app.ui.mode.get()
        if mode == "place":
            self.place_city(pos)
        elif mode == "connect":
            self.connect_city(pos)
        elif mode == "delete":
            self.delete_city(pos)
        elif mode == "start":
            self.select_start(pos)
        elif mode == "end":
            self.select_end(pos)

    # Place city node
    def place_city(self, pos):
        name = f"C{self.app.city_count}"
        city = City(name, pos.x, pos.y)
        self.app.cities.append(city)
        # Draw city
        city.draw_id = self.app.ui.canvas.create_oval(pos.x - 5, pos.y - 5, pos.x + 5, pos.y + 5, fill="black")
        city.text_id = self.app.ui.canvas.create_text(pos.x, pos.y - 10, text=name)

        print(city)
        self.app.city_count += 1

    # Find & select city method
    def find_city_at_position(self, x, y):
        for city in self.app.cities:
            if abs(city.x - x) < 10 and abs(city.y - y) < 10:
                return city
        return None

    # Connect two cities
    def connect_city(self, pos):
        city = self.find_city_at_position(pos.x, pos.y)
        # Check for attempt to connect city to self
        if city == self.app.selected_city:
            print("Cannot connect a city to itself.")
            self.app.selected_city = None
            self.app.ui.update_all_city_colors()
            return
        # No city selected
        if not city:
            return
        # Select and highlight first selected city with blue
        if self.app.selected_city is None:
            self.app.selected_city = city
            self.app.ui.canvas.itemconfig(city.draw_id, fill="blue")
        # Upon selection of second city
        else:
            # Create weighted edge
            distance = calculate_distance(self.app.selected_city, city)
            # Check for existing edge
            if any(edge.other(self.app.selected_city) == city for edge in self.app.selected_city.edges):
                print("Connection already exists")
                self.app.selected_city = None
                self.app.ui.update_all_city_colors()
                return
            edge = Edge(self.app.selected_city, city, distance)
            # Draw connection
            edge.line_id = self.app.ui.canvas.create_line(self.app.selected_city.x, self.app.selected_city.y, city.x, city.y)
            # Add edge to both cities' edge lists
            self.app.selected_city.add_edge(edge)
            city.add_edge(edge)
            # Add to "global" edge list
            self.app.edges.append(edge)
            # Display weight next to edge
            mid_x = (self.app.selected_city.x + city.x) / 2
            mid_y = (self.app.selected_city.y + city.y) / 2
            edge.text_id = self.app.ui.canvas.create_text(
                mid_x, mid_y, text=f"{distance:.1f}", fill="blue") # .1f = 1 decimal point

            # Reset colour
            self.app.ui.update_city_color(self.app.selected_city)
            self.app.selected_city = None

    # Delete a city
    def delete_city(self, pos):
        city = self.find_city_at_position(pos.x, pos.y)
        if not city: # Check if city is selected
            return
        if city == self.app.start_city: # Check if city is a start node
            self.app.start_city = None
        if city == self.app.end_city: # Check if city is an end node
            self.app.end_city = None
        # Delete all edges connected to city 
        for edge in city.edges[:]:  # Copy of list to avoid side effects
            self.delete_edge(edge)
        # Delete city from list
        self.app.cities.remove(city)
        # Remove from canvas
        self.app.ui.canvas.delete(city.draw_id)
        self.app.ui.canvas.delete(city.text_id)

        self.app.selected_city = None
        # Update colours
        self.app.ui.update_all_city_colors()
        self.app.ui.update_run_button()

        print(f"Deleted {city.name}")
    
    def delete_edge(self, edge):
        # Remove from canvas
        self.app.ui.canvas.delete(edge.line_id)
        # Remove edge from both cities' edge lists
        edge.city1.edges.remove(edge)
        edge.city2.edges.remove(edge)
        # Remove from "global" edge list
        self.app.edges.remove(edge)
        self.app.ui.canvas.delete(edge.text_id)

    def select_start(self, pos):
        city = self.find_city_at_position(pos.x, pos.y)
        if not city: # Check if city is selected
            return
        # Reset previous start
        self.app.start_city = city
        # Update colours
        self.app.ui.update_all_city_colors()
        self.app.ui.update_run_button()
        print(f"Start: {city.name}")

    def select_end(self, pos):
        city = self.find_city_at_position(pos.x, pos.y)
        if not city: # Check if city is selected
            return
        # Reset previous end
        self.app.end_city = city
        # Update colours
        self.app.ui.update_all_city_colors()
        self.app.ui.update_run_button()
        print(f"End: {city.name}")

    def run_dijkstra(self):
        # Clear previous path
        self.app.ui.reset_edges()
        # Update colours
        self.app.ui.update_all_city_colors()
        # Missing start/end node handling
        if not self.app.start_city or not self.app.end_city:
            self.app.ui.dist_label.config(text="Missing start/end")
            self.app.ui.path_label.config(text="")
            print("Select a start and end destination.")
            return
        # Reset previous path data
        path, distance = dijkstra(self.app.start_city, self.app.end_city, self.app.cities)
        # Used for display of cumulative distance in path_label
        path_with_dist = []
        current_dist = 0
        for i in range(len(path)):
            if i == 0:
                path_with_dist.append(f"{path[i].name} (0)")
            else:
                for edge in path[i-1].edges:
                    if edge.other(path[i-1]) == path[i]:
                        current_dist += edge.distance
                        break
                path_with_dist.append(f"{path[i].name} ({current_dist:.1f})")
        path_names = "->" + "\n->".join(path_with_dist)
        # Edge case handling (no possible route)
        if distance == float('inf') or not path:
            self.app.ui.dist_label.config(text="No route found")
            self.app.ui.path_label.config(text="")
            return
        # Update result labels
        self.app.ui.dist_label.config(text=f"Distance: {distance:.1f}")
        self.app.ui.path_label.config(text=f"Path: \n{path_names}")
        print(f"Shortest path: {path_names}")
        print("Distance:", distance)
        self.app.ui.draw_path(path)
