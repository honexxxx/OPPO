import math
import re
from typing import List


class PointValidator:
    VALID_COLORS = {"red", "green", "blue"}

    @staticmethod
    def is_valid_color(color: str) -> bool:
        return color in PointValidator.VALID_COLORS


class Point2D:
    def __init__(self, x: float, y: float, color: str):
        if not PointValidator.is_valid_color(color):
            raise ValueError(f"Недопустимый цвет: {color}")
        self.x = x
        self.y = y
        self.color = color

    def distance_from_origin(self) -> float:
        return math.hypot(self.x, self.y)

    def distance_to(self, other: "Point2D") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


class PointParser:
    NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")
    COLOR_PATTERN = re.compile(r"\b(red|green|blue)\b")

    @staticmethod
    def parse(line: str) -> Point2D:
        numbers = PointParser._extract_numbers(line)
        color = PointParser._extract_color(line)
        return Point2D(numbers[0], numbers[1], color)

    @staticmethod
    def _extract_numbers(line: str) -> List[float]:
        values = PointParser.NUMBER_PATTERN.findall(line)
        if len(values) != 2:
            raise ValueError("Ожидается ровно две координаты")
        return list(map(float, values))

    @staticmethod
    def _extract_color(line: str) -> str:
        match = PointParser.COLOR_PATTERN.search(line)
        if not match:
            raise ValueError("Цвет не найден")
        return match.group(1)


class FileReader:
    @staticmethod
    def read_points(filename: str) -> List[Point2D]:
        points = []
        for index, line in enumerate(FileReader._read_lines(filename), 1):
            FileReader._parse_line(points, line, index)
        return points

    @staticmethod
    def _read_lines(filename: str):
        with open(filename, encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    yield line

    @staticmethod
    def _parse_line(points: list, line: str, index: int):
        try:
            points.append(PointParser.parse(line))
        except ValueError as error:
            print(f"Ошибка в строке {index}: {error}")


class PointService:
    @staticmethod
    def sort_by_distance(points: List[Point2D]) -> List[Point2D]:
        return sorted(points, key=lambda p: p.distance_from_origin())

    @staticmethod
    def filter_by_radius(
        points: List[Point2D],
        center: Point2D,
        radius: float,
    ) -> List[Point2D]:
        return [p for p in points if p.distance_to(center) <= radius]


class TablePrinter:
    @staticmethod
    def print(points: List[Point2D]):
        if not points:
            print("Нет данных.")
            return
        TablePrinter._print_header()
        TablePrinter._print_rows(points)
        TablePrinter._print_footer(points)

    @staticmethod
    def _print_header():
        print("-" * 72)
        print("| №  | X        | Y        | Цвет       | Расстояние     |")
        print("-" * 72)

    @staticmethod
    def _print_rows(points: List[Point2D]):
        for i, point in enumerate(points, 1):
            TablePrinter._print_row(i, point)

    @staticmethod
    def _print_row(index: int, point: Point2D):
        print(
            f"| {index:<2} | {point.x:<8.2f} | {point.y:<8.2f} | "
            f"{point.color:<10} | {point.distance_from_origin():<14.2f} |"
        )

    @staticmethod
    def _print_footer(points: List[Point2D]):
        print("-" * 72)
        print(f"Всего точек: {len(points)}")


def read_float(prompt: str) -> float:
    return float(input(prompt))


def main():
    points = FileReader.read_points("points.txt")

    print("\n=== Исходные данные ===")
    TablePrinter.print(points)

    print("\n=== Сортировка по расстоянию от (0,0) ===")
    sorted_points = PointService.sort_by_distance(points)
    TablePrinter.print(sorted_points)

    center = Point2D(read_float("X центра: "), read_float("Y центра: "), "red")
    radius = read_float("Радиус: ")

    print("\n=== Точки в радиусе ===")
    result = PointService.filter_by_radius(points, center, radius)
    TablePrinter.print(result)


if __name__ == "__main__":
    main()
