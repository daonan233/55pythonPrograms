import tkinter as tk
from itertools import permutations
import math


class GridGraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("鸭鸭连线")

        self.row_entry = tk.Entry(master)
        self.row_entry.grid(row=0, column=0, padx=5, pady=5)
        self.row_label = tk.Label(master, text="行")
        self.row_label.grid(row=0, column=1, padx=5, pady=5)

        self.column_entry = tk.Entry(master)
        self.column_entry.grid(row=0, column=2, padx=5, pady=5)
        self.column_label = tk.Label(master, text="列")
        self.column_label.grid(row=0, column=3, padx=5, pady=5)

        self.generate_button = tk.Button(master, text="生成网格图", command=self.generate_grid)
        self.generate_button.grid(row=0, column=4, padx=5, pady=5)

        self.line_type_var = tk.StringVar()
        self.line_type_var.set("只能直线")
        self.line_type_menu = tk.OptionMenu(master, self.line_type_var, "只能直线", "可以斜线")
        self.line_type_menu.grid(row=0, column=5, padx=5, pady=5)

        self.clear_button = tk.Button(master, text="清除", command=self.clear_all)
        self.clear_button.grid(row=0, column=6, padx=5, pady=5)

        self.canvas = tk.Canvas(master, bg="white", width=500, height=500)
        self.canvas.grid(row=1, columnspan=7)

        self.grid_points = []
        self.marked_points = []
        self.canvas.bind("<Button-1>", self.mark_point)

    def generate_grid(self):
        self.canvas.delete("all")  # Clear canvas
        rows = int(self.row_entry.get())
        columns = int(self.column_entry.get())

        cell_width = 500 // columns
        cell_height = 500 // rows

        for i in range(0, 501, cell_width):
            self.canvas.create_line(i, 0, i, 500, fill="gray")
        for j in range(0, 501, cell_height):
            self.canvas.create_line(0, j, 500, j, fill="gray")

        self.grid_points = [(i * cell_width, j * cell_height) for i in range(columns) for j in range(rows)]

    def mark_point(self, event):
        x, y = event.x, event.y
        closest_point = min(self.grid_points, key=lambda p: math.sqrt((p[0] - x) ** 2 + (p[1] - y) ** 2))

        if closest_point in self.marked_points:
            return

        if self.marked_points:
            prev_point = self.marked_points[-1]
            if prev_point[0] == closest_point[0]:
                # Draw vertical line
                self.canvas.create_line(prev_point[0], min(prev_point[1], closest_point[1]),
                                        prev_point[0], max(prev_point[1], closest_point[1]),
                                        fill="red", tags="path")
            elif prev_point[1] == closest_point[1]:
                # Draw horizontal line
                self.canvas.create_line(min(prev_point[0], closest_point[0]), prev_point[1],
                                        max(prev_point[0], closest_point[0]), prev_point[1],
                                        fill="red", tags="path")

        self.marked_points.append(closest_point)
        self.canvas.create_oval(closest_point[0] - 3, closest_point[1] - 3, closest_point[0] + 3, closest_point[1] + 3,
                                fill="red", tags="point")
        self.calculate_shortest_path()

    def clear_all(self):
        self.canvas.delete("point")
        self.canvas.delete("path")
        self.marked_points.clear()

    def calculate_shortest_path(self):
        if len(self.marked_points) < 2:
            return

        shortest_paths = self.shortest_paths(self.marked_points)

        self.canvas.delete("path")  # Clear existing path
        for path_color, path in shortest_paths:
            for i in range(len(path) - 1):
                self.canvas.create_line(path[i], path[i + 1], fill=path_color, tags="path")

    def shortest_paths(self, points):
        shortest_distance = math.inf
        shortest_paths = []

        for perm in permutations(points):
            distance = 0
            for i in range(len(perm) - 1):
                if self.line_type_var.get() == "只能直线":
                    if self.is_straight_line(perm[i], perm[i + 1]):
                        # Only add distance if points are in the same row or column
                        if perm[i][0] == perm[i + 1][0] or perm[i][1] == perm[i + 1][1]:
                            distance += math.sqrt((perm[i][0] - perm[i + 1][0]) ** 2 + (perm[i][1] - perm[i + 1][1]) ** 2)
                        else:
                            distance = math.inf
                            break
                    else:
                        distance = math.inf
                        break
                elif self.line_type_var.get() == "可以斜线":
                    distance += math.sqrt((perm[i][0] - perm[i + 1][0]) ** 2 + (perm[i][1] - perm[i + 1][1]) ** 2)
                else:
                    distance = math.inf
                    break
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_paths = [(self.get_color(i), perm) for i in range(len(points))]
            elif distance == shortest_distance:
                shortest_paths.append((self.get_color(len(shortest_paths)), perm))

        return shortest_paths

    def is_straight_line(self, point1, point2):
        return point1[0] == point2[0] or point1[1] == point2[1]

    def get_color(self, index):
        colors = ["blue", "green", "red", "orange", "purple", "yellow", "cyan", "magenta"]
        return colors[index % len(colors)]


root = tk.Tk()
app = GridGraphApp(root)
root.mainloop()
