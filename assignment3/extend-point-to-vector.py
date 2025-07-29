import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Vector(Point):
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    
if __name__ == "__main__":

    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 4)

    print("Points:")
    print(p1)
    print(p2)
    print(f"Are p1 and p2 equal? {p1 == p2}")
    print(f"Distance from p1 to p3: {p1.distance_to(p3):.2f}")

    v1 = Vector(2, 3)
    v2 = Vector(4, 1)
    v3 = v1 + v2

    print("\nVectors:")
    print(v1)
    print(v2)
    print(f"v1 + v2 = {v3}")
