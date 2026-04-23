import tkinter as tk

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    # format for print af City-objekt 
    def __repr__(self):
        return f"{self.name} ({self.x}, {self.y})"


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dijkstra city simulation")

        self.canvas = tk.Canvas(self.root, width=700, height=700, bg="white")
        self.canvas.pack()

        self.cities = []
        self.city_count = 0

        self.canvas.bind("<Button-1>", self.add_city)

    # tilføj by på canvas
    def add_city(self, pos):
        name = f"C{self.city_count}"
        city = City(name, pos.x, pos.y)
        self.cities.append(city)

        self.canvas.create_oval(
            pos.x - 5, pos.y - 5,
            pos.x + 5, pos.y + 5,
            fill="black"
        )

        self.canvas.create_text(pos.x, pos.y - 10, text=name)
        print(city)

        self.city_count += 1

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()