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