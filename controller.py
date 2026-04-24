# controller.py (refactored)
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    # Click handler
    def handle_click(self, pos, mode):
        """Route clicks based on mode"""
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
        self.view.draw_city(city) # Displays City object on canvas
        print(city)

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
                print(error)
            else:
                self.view.draw_edge(edge, self.model.selected_city, city)
            
            self.model.deselect_city()
            self.view.update_all_city_colors(self.model)

    def delete_city(self, pos):
        city = self.model.find_city_at_position(pos.x, pos.y) # Selects city near mouse
        if not city:
            return
        
        # Erase from view first
        self.view.erase_city(city)
        for edge in city.edges[:]:
            self.view.erase_edge(edge)
        
        # Remove from model
        self.model.delete_city(city)
        
        self.view.update_all_city_colors(self.model)
        self.view.update_run_button(self.model)
        print(f"Deleted {city.name}")

    def select_start(self, pos):
        city = self.model.find_city_at_position(pos.x, pos.y)
        if not city:
            return
        
        self.model.set_start_city(city)
        self.view.update_all_city_colors(self.model)
        self.view.update_run_button(self.model)
        print(f"Start: {city.name}")

    def select_end(self, pos):
        city = self.model.find_city_at_position(pos.x, pos.y)
        if not city:
            return
        
        self.model.set_end_city(city)
        self.view.update_all_city_colors(self.model)
        self.view.update_run_button(self.model)
        print(f"End: {city.name}")

    def run_dijkstra(self):
        # Update view
        self.view.reset_edges(self.model)
        self.view.update_all_city_colors(self.model)
        
        # Execute Dijkstra
        path, distance, error = self.model.run_dijkstra()
        
        # Display error in view
        if error:
            self.view.show_error(error)
            return
        
        # Format path display
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
        # Update view display
        self.view.show_result(distance, path_names)
        self.view.draw_path(path)