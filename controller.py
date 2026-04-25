class Controller:
    def __init__(self, model):
        self.model = model
        self.view = None  # Gets configured in App later
        
    # Link view to controller
    def set_view(self, view):
        self.view = view

    def handle_click(self, pos, mode):
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

    def place_city(self, pos):
        city = self.model.add_city(pos.x, pos.y) # Creates City object
        self.view.display_city(city) # Displays City object on canvas through UI

    def connect_city(self, pos):
        city = self.model.find_city_at_position(pos.x, pos.y) # Selects city near mouse
        if not city:
            return
        
        if self.model.selected_city is None:
            self.model.select_city(city)
            self.view.highlight_city(city)
        else:
            edge, error = self.model.connect_cities(self.model.selected_city, city)
            
            if error:
                self.view.show_error(error)
            else:
                # Send data to UI
                cities_data = self.get_all_cities_data()
                self.view.display_all_cities(cities_data)
                self.view.display_edge(edge, self.model.selected_city, city)
            
            self.model.deselect_city()

    def delete_city(self, pos):
        city = self.model.find_city_at_position(pos.x, pos.y) # Selects city near mouse
        if not city:
            return
        
        self.view.erase_city(city)
        for edge in self.model.get_edges_of_city(city):
            self.view.erase_edge(edge)
        
        self.model.delete_city(city)
        cities_data = self.get_all_cities_data()
        self.view.display_all_cities(cities_data)

    def select_start(self, pos):
        city = self.model.find_city_at_position(pos.x, pos.y)
        if not city:
            return
        self.model.set_start_city(city)
        cities_data = self.get_all_cities_data()
        self.view.display_all_cities(cities_data)
        self.update_run_button_state()

    def select_end(self, pos):
        city = self.model.find_city_at_position(pos.x, pos.y)
        if not city:
            return
        self.model.set_end_city(city)
        cities_data = self.get_all_cities_data()
        self.view.display_all_cities(cities_data)
        self.update_run_button_state()

    def run_dijkstra(self):
        # Update view
        self.view.reset_edges(self.model.edges)
        # Execute Dijkstra
        path, distance, error = self.model.run_dijkstra()
        # Display error in view
        if error:
            self.view.show_error(error)
            return
        
        # Format path data and send to UI
        path_with_dist = self.format_path(path)
        path_names = "->" + "\n->".join(path_with_dist)
        self.view.show_result(distance, path_names)
        self.view.highlight_path(path)

    # UI helper methods
    # Returns all data about a given city to UI
    def get_all_cities_data(self):
        cities_data = self.model.get_state()
        return cities_data

    # Returns data about all edges to UI
    def get_all_edges_data(self):
        return self.model.edges

    # Helps format the path display properly
    def format_path(self, path):
        path_with_dist = [] # List including formatted cities along with cumulative distance
        current_dist = 0 # Keep track of the total distance from start node 
        # Go through all cities in route
        for i in range(len(path)):
            if i == 0: 
                path_with_dist.append(f"{path[i].name} (0)") # The first city, i.e. start, always has distance 0
            else:
                # Find connection between previous and current city
                for edge in path[i-1].edges:
                    # When the connection is found, add its distance to the total
                    if edge.other(path[i-1]) == path[i]:
                        current_dist += edge.distance
                        break
                path_with_dist.append(f"{path[i].name} ({current_dist:.1f})") # Add city along with respective cumulative distance to the formatted list
        return path_with_dist # Return the formatted list of strings
        
    # Tell view whether to enable run button
    def update_run_button_state(self):
        can_run = self.model.start_city is not None and self.model.end_city is not None
        self.view.set_run_button_enabled(can_run)
    
    # Clear all cities and edges
    def clear_all(self):
        self.model.reset()
        self.update_run_button_state()