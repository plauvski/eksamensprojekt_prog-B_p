from ui import UI
from controller import Controller

class App:
    def __init__(self):
        # Data
        self.cities = []
        self.city_count = 0
        self.selected_city = None
        self.edges = []
        self.start_city = None
        self.end_city = None
        # UI
        self.ui = UI(self)
        # Controller
        self.controller = Controller(self)

    # Click handling
    def handle_click(self, pos):
        self.controller.handle_click(pos)

    def run_dijkstra(self):
        self.controller.run_dijkstra()

    def run(self):
        self.ui.run()

if __name__ == "__main__":
    app = App()
    app.run()
