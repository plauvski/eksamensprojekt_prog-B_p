import math

# Distance between two points, used for weight calculation  
def calculate_distance(city1, city2):
    return math.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2)

# Dijkstras algorithm
def dijkstra(start, end, cities):
    distances = {city: float('inf') for city in cities} # Sets distance values of all cities to infinity
    previous = {} # Used for reconstruction of route

    distances[start] = 0 # Set value of start node
    unvisited = cities.copy() # List of unvisited cities

    # Main loop
    while unvisited: # Loops until all cities have been visited
        current = min(unvisited, key=lambda city: distances[city]) # Find node with shortest distance
        unvisited.remove(current) # Mark city as visited

        if current == end: # Break out of the loop if end node is reached
            break
        for edge in current.edges: # Evaluate connected edges
            neighbor = edge.other(current) # Find neighbouring node
            new_distance = distances[current] + edge.distance # Calculate new distance

            # Compare and update shortest distance
            if new_distance < distances[neighbor]: # Check if new distance to neighbour is shorter than previous 
                distances[neighbor] = new_distance # Update neighbour distance
                previous[neighbor] = current # Update which node we came from. Allows for path reconstruction
    
    # Edge case handling (no path)
    if distances[end] == float('inf'):
        return [], float('inf')
    # Reconstruct path from end node
    path = []
    current = end

    # Loops in reverse over route  
    while current in previous:
        path.insert(0, current)
        current = previous[current]
    # Add start last
    path.insert(0, start)
    return path, distances[end] # Return path list and total distance

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

    # Format for print of City-object
    def __repr__(self):
        return f"{self.name} ({self.x}, {self.y})"

class Edge:
    def __init__(self, city1, city2, distance):
        self.city1 = city1
        self.city2 = city2
        self.distance = distance
        self.line_id = None
        self.text_id = None

    # Connect two
    def connects(self, city):
        return self.city1 == city or self.city2 == city

    # Find neighbour
    def other(self, city):
        if city == self.city1:
            return self.city2
        elif city == self.city2:
            return self.city1
        return None
