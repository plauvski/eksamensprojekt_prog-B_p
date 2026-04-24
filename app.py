from model import Model
from controller import Controller
from ui import UI

class App:
    def __init__(self):
        self.model = Model()
        self.controller = Controller(self.model) # Create controller first
        self.ui = UI(self.controller) # Pass controller directly
        self.controller.set_view(self.ui)  # Link controller to view

    def run(self):
        self.ui.run()

if __name__ == "__main__":
    app = App()
    app.run()