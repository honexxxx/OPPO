import re
import math


class Point2D:
    def __init__(self, x, y, color):
        if color not in ("red", "green", "blue"):
            raise ValueError(f"Недопустимый цвет: {color}")
        self.x = x
        self.y = y
        self.color = color

    def distance_from_origin(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class PointParser:
    # регулярки для поиска элементов по ТИПУ, а не по порядку
    number_pattern = re.compile(r"-?\d+(?:\.\d+)?")
    color_pattern = re.compile(r"\b(red|green|blue)\b")

    @staticmethod
    def parse(line):
        numbers = PointParser.number_pattern.findall(line)
        color_match = PointParser.color_pattern.search(line)

        if len(numbers) != 2:
            raise ValueError("Должно быть ровно две координаты")

        if not color_match:
            raise ValueError("Цвет не найден или недопустим")

        x, y = map(float, numbers)
        color = color_match.group(1)

        return Point2D(x, y, color)


def read_points_from_file(filename):
    points = []

    with open(filename, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, 1):
            if not line.strip():
                continue
            try:
                point = PointParser.parse(line)
                points.append(point)
            except Exception as e:
                print(f"Ошибка в строке {line_num}: {e}")

    return points


def print_table(points):
    if not points:
        print("Нет данных для отображения.")
        return

    print("-" * 72)
    print(f"| {'№':<3} | {'X':<10} | {'Y':<10} | {'Цвет':<10} | {'Расстояние':<15} |")
    print("-" * 72)

    for i, p in enumerate(points, 1):
        print(
            f"| {i:<3} | {p.x:<10.2f} | {p.y:<10.2f} | {p.color:<10} | {p.distance_from_origin():<15.2f} |"
        )

    print("-" * 72)
    print(f"Всего точек: {len(points)}")


def sort_by_distance(points):
    return sorted(points, key=lambda p: p.distance_from_origin())


def points_in_radius(points, center, radius):
    return [p for p in points if p.distance_to(center) <= radius]


def main():
    filename = "points.txt"
    points = read_points_from_file(filename)

    print("\n=== Исходные точки ===")
    print_table(points)

    print("\n=== Отсортировано по расстоянию от (0,0) ===")
    sorted_points = sort_by_distance(points)
    print_table(sorted_points)

    try:
        cx = float(input("\nВведите X центра: "))
        cy = float(input("Введите Y центра: "))
        radius = float(input("Введите радиус: "))

        center = Point2D(cx, cy, "red")  # цвет не важен
        result = points_in_radius(points, center, radius)

        print(f"\n=== Точки в радиусе {radius} от ({cx}, {cy}) ===")
        print_table(result)

    except ValueError:
        print("Ошибка ввода координат или радиуса.")


if __name__ == "__main__":
    main()
