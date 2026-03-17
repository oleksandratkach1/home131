import math

# ─────────────────────────── Base class ───────────────────────────

class Figure:
    def perimeter(self) -> float:
        raise NotImplementedError

    def area(self) -> float:
        raise NotImplementedError

    def __str__(self) -> str:
        return (f"{self.__class__.__name__}: "
                f"area={self.area():.4f}, perimeter={self.perimeter():.4f}")

# ─────────────────────────── Figures ───────────────────────────────


class Triangle(Figure):

    def __init__(self, a: float, b: float, c: float):
        self.a, self.b, self.c = a, b, c

    def is_valid(self) -> bool:
        a, b, c = self.a, self.b, self.c
        return a > 0 and b > 0 and 0 < c < a + b and a + c > b and b + c > a

    def perimeter(self) -> float:
        return self.a + self.b + self.c

    def area(self) -> float:
        s = self.perimeter() / 2  # формула Герона
        val = s * (s - self.a) * (s - self.b) * (s - self.c)
        return math.sqrt(max(val, 0))


class Rectangle(Figure):
    """Визначається двома сторонами a, b."""

    def __init__(self, a: float, b: float):
        self.a, self.b = a, b

    def is_valid(self) -> bool:
        return self.a > 0 and self.b > 0

    def perimeter(self) -> float:
        return 2 * (self.a + self.b)

    def area(self) -> float:
        return self.a * self.b


class Trapeze(Figure):
    """Визначається двома основами a, b та двома бічними сторонами c, d."""

    def __init__(self, a: float, b: float, c: float, d: float):
        self.a, self.b, self.c, self.d = a, b, c, d

    def is_valid(self) -> bool:
        a, b, c, d = self.a, self.b, self.c, self.d
        if a <= 0 and b <= 0: return False
        if c <= 0 or d <= 0: return False
        return True

    def perimeter(self) -> float:
        return self.a + self.b + self.c + self.d

    def area(self) -> float:
        a, b, c, d = self.a, self.b, self.c, self.d
        if abs(a - b) < 1e-12:
            h = c
        else:
            x = (a - b + (c ** 2 - d ** 2) / (a - b)) / 2
            h_sq = c ** 2 - x ** 2
            h = math.sqrt(max(h_sq, 0))
        return (a + b) / 2 * h


class Parallelogram(Figure):
    """Визначається двома сторонами a, b та висотою h."""

    def __init__(self, a: float, b: float, h: float):
        self.a, self.b, self.h = a, b, h

    def is_valid(self) -> bool:
        return self.a > 0 and self.b > 0 and self.h > 0

    def perimeter(self) -> float:
        return 2 * (self.a + self.b)

    def area(self) -> float:
        return self.a * self.h


class Circle(Figure):
    """Визначається радіусом r."""

    def __init__(self, r: float):
        self.r = r

    def is_valid(self) -> bool:
        return self.r > 0

    def perimeter(self) -> float:  # довжина кола
        return 2 * math.pi * self.r

    def area(self) -> float:
        return math.pi * self.r ** 2


# ─────────────────────────── Parser ────────────────────────────────

FIGURE_MAP = {
    "triangle": (Triangle, 3),
    "rectangle": (Rectangle, 2),
    "trapeze": (Trapeze, 4),
    "parallelogram": (Parallelogram, 3),
    "circle": (Circle, 1),
}


def parse_file(filename: str) -> list[Figure]:
    shapes = []
    with open(filename, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            name = parts[0].lower()
            if name not in FIGURE_MAP:
                print(f"  [!] Рядок {lineno}: невідома фігура '{parts[0]}' — пропускаємо")
                continue
            cls, n_params = FIGURE_MAP[name]
            params_raw = parts[1:]
            if len(params_raw) < n_params:
                print(f"  [!] Рядок {lineno}: замало параметрів для {parts[0]} "
                      f"(потрібно {n_params}, є {len(params_raw)}) — пропускаємо")
                continue
            try:
                params = [float(p) for p in params_raw[:n_params]]
            except ValueError:
                print(f"  [!] Рядок {lineno}: нечислові параметри — пропускаємо")
                continue
            shape = cls(*params)
            if hasattr(shape, "is_valid") and not shape.is_valid():
                print(f"  [!] Рядок {lineno}: некоректні параметри — пропускаємо")
                continue
            shapes.append(shape)
    return shapes

# ─────────────────────────── Main ──────────────────────────────────

def test(input_file_path, output_file_path):
    with open(output_file_path, "w", encoding='utf-8') as f_out:
        figures = parse_file(input_file_path)  # передаємо правильний шлях

        if figures:
            max_area = max(figures, key=lambda f: f.area())
            max_perimeter = max(figures, key=lambda f: f.perimeter())

            print(f"Maximal area: {max_area.area():.4f}", file=f_out)
            print(f"Maximal perimeter: {max_perimeter.perimeter():.4f}", file=f_out)
        else:
            print("None are found", file=f_out)


test("input01.txt", "output01.txt")
test("input02.txt", "output02.txt")
test("input03.txt", "output03.txt")