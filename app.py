from model import Model
from controller import Controller
from ui import UI

class App:
    def __init__(self):
        self.model = Model()
        self.controller = Controller(self.model, None)  # Create controller first
        self.ui = UI(self.controller, self.model)  # Pass controller directly
        self.controller.view = self.ui  # Update controller's view reference

    def run(self):
        self.ui.run()

if __name__ == "__main__":
    app = App()
    app.run()