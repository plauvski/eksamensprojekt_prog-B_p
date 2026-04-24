import math

# Distance between two points, used for weight calculation  
def calculate_distance(city1, city2):
    return math.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2)

# Dijkstras algorithm
def dijkstra(start, end, cities):
    distances = {city: float('inf') for city in cities} # Note: Implicit hashing
    previous = {}

    distances[start] = 0
    unvisited = cities.copy()

    while unvisited:
        # Find node with smallest distance
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
        # Edge case handling (no path)
    if distances[end] == float('inf'):
        return [], float('inf')
    # Reconstruct path
    path = []
    current = end

    while current in previous:
        path.insert(0, current)
        current = previous[current]

    path.insert(0, start)
    return path, distances[end]

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
