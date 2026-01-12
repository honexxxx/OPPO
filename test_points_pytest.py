import pytest
from Points_Table_Vasilev_R2 import Point2D, PointParser, PointService, PointValidator


# =======================
# Тесты PointParser
# =======================
def test_valid_input_numbers_first():
    point = PointParser.parse("3 4 red")
    assert point.x == 3.0
    assert point.y == 4.0
    assert point.color == "red"


def test_valid_input_color_first():
    point = PointParser.parse("blue -1.5 2.5")
    assert point.x == -1.5
    assert point.y == 2.5
    assert point.color == "blue"


def test_invalid_color():
    with pytest.raises(ValueError):
        PointParser.parse("3 4 yellow")


def test_missing_color():
    with pytest.raises(ValueError):
        PointParser.parse("3 4")


def test_extra_numbers():
    with pytest.raises(ValueError):
        PointParser.parse("1 2 3 red")


def test_negative_numbers():
    point = PointParser.parse("-1.5 -2.5 blue")
    assert point.x == -1.5
    assert point.y == -2.5


def test_missing_numbers():
    with pytest.raises(ValueError):
        PointParser.parse("red")


def test_numbers_with_signs():
    point = PointParser.parse("+3 -4 green")
    assert point.x == 3.0
    assert point.y == -4.0
    assert point.color == "green"

# =======================
# Тесты Point2D
# =======================
def test_distance_from_origin():
    point = Point2D(3, 4, "red")
    assert point.distance_from_origin() == 5.0


def test_distance_to_another_point():
    p1 = Point2D(0, 0, "red")
    p2 = Point2D(3, 4, "blue")
    assert p1.distance_to(p2) == 5.0


def test_invalid_color_creation():
    with pytest.raises(ValueError):
        Point2D(1, 1, "yellow")


def test_distance_negative_coords():
    p1 = Point2D(-1, -1, "green")
    p2 = Point2D(-4, -5, "red")
    assert p1.distance_to(p2) == 5.0


# =======================
# Тесты PointService
# =======================
def test_sort_by_distance():
    p1 = Point2D(3, 4, "red")
    p2 = Point2D(0, 0, "blue")
    p3 = Point2D(1, 1, "green")
    points = [p1, p2, p3]
    sorted_points = PointService.sort_by_distance(points)
    distances = [p.distance_from_origin() for p in sorted_points]
    assert distances == sorted(distances)


def test_filter_by_radius_include_all():
    center = Point2D(0, 0, "red")
    points = [Point2D(1, 1, "blue"), Point2D(2, 2, "green")]
    filtered = PointService.filter_by_radius(points, center, 5)
    assert len(filtered) == 2


def test_filter_by_radius_include_none():
    center = Point2D(0, 0, "red")
    points = [Point2D(10, 10, "blue"), Point2D(6, 6, "green")]
    filtered = PointService.filter_by_radius(points, center, 5)
    assert len(filtered) == 0


def test_filter_by_radius_partial():
    center = Point2D(0, 0, "red")
    points = [Point2D(1, 1, "blue"), Point2D(10, 10, "green")]
    filtered = PointService.filter_by_radius(points, center, 5)
    assert len(filtered) == 1
    assert filtered[0].x == 1
    assert filtered[0].y == 1


def test_sort_same_distance():
    p1 = Point2D(3, 4, "red")
    p2 = Point2D(4, 3, "blue")
    points = [p2, p1]
    sorted_points = PointService.sort_by_distance(points)
    assert sorted_points[0].distance_from_origin() == 5.0
    assert sorted_points[1].distance_from_origin() == 5.0


# =======================
# Тесты PointValidator
# =======================
def test_valid_colors():
    for color in ["red", "green", "blue"]:
        assert PointValidator.is_valid_color(color)


def test_invalid_colors():
    for color in ["yellow", "", "purple"]:
        assert not PointValidator.is_valid_color(color)

