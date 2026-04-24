import math

# Distance calculation
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

    # Print format
    def __repr__(self):
        return f"{self.name} ({self.x}, {self.y})"

class Edge:
    def __init__(self, city1, city2, distance):
        self.city1 = city1
        self.city2 = city2
        self.distance = distance
        self.line_id = None
        self.text_id = None

    def other(self, city):
        if city == self.city1:
            return self.city2
        elif city == self.city2:
            return self.city1
        return None

class Model:
    def __init__(self):
        # Data
        self.cities = []
        self.city_count = 0
        self.selected_city = None
        self.edges = []
        self.start_city = None
        self.end_city = None

    # Add new city
    def add_city(self, x, y):
        name = f"C{self.city_count}"
        city = City(name, x, y)
        self.cities.append(city)
        self.city_count += 1
        return city

    def find_city_at_position(self, x, y):
        for city in self.cities:
            if abs(city.x - x) < 10 and abs(city.y - y) < 10:
                return city
        return None

    def select_city(self, city):
        self.selected_city = city

    def deselect_city(self):
        self.selected_city = None

    def connect_cities(self, city1, city2):
        # Avoid creating connection to self
        if city1 == city2:
            return None, "Cannot connect a city to itself."
        # Avoid creating duplicate connections
        if any(edge.other(city1) == city2 for edge in city1.edges):
            return None, "Connection already exists"
        
        distance = calculate_distance(city1, city2)
        edge = Edge(city1, city2, distance)
        city1.add_edge(edge)
        city2.add_edge(edge)
        self.edges.append(edge)
        return edge, None

    def delete_city(self, city):
        if not city:
            return
        # Start/end update
        if city == self.start_city:
            self.start_city = None
        if city == self.end_city:
            self.end_city = None
        # Remove edges
        for edge in city.edges[:]:
            self.delete_edge(edge)
        # Remove city
        self.cities.remove(city)
        if self.selected_city == city:
            self.selected_city = None

    def delete_edge(self, edge):
        edge.city1.edges.remove(edge)
        edge.city2.edges.remove(edge)
        self.edges.remove(edge)

    def set_start_city(self, city):
        self.start_city = city

    def set_end_city(self, city):
        self.end_city = city

    # Dijkstras algorithm
    def dijkstra(self, start, end, cities):
        distances = {city: float('inf') for city in cities}
        previous = {}
        distances[start] = 0
        unvisited = cities.copy()
        
        while unvisited:
            current = min(unvisited, key=lambda city: distances[city])
            unvisited.remove(current)
            
            if current == end:
                break
            for edge in current.edges:
                neighbor = edge.other(current)
                new_distance = distances[current] + edge.distance
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
        
        if distances[end] == float('inf'):
            return [], float('inf')
        
        path = []
        current = end
        while current in previous:
            path.insert(0, current)
            current = previous[current]
        path.insert(0, start)
        return path, distances[end]

    def run_dijkstra(self):
        if not self.start_city or not self.end_city:
            return None, None, "Missing start/end nodes"
        
        path, distance = self.dijkstra(self.start_city, self.end_city, self.cities)
        
        if distance == float('inf') or not path:
            return None, None, "No route found"
        
        return path, distance, None