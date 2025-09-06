# pookalam design with turtle graphics
import turtle
from math import sin, cos, radians, pi
W, H = 800, 800
BG_COLOR = "#fff5e0"       
COLOR_YELLOW = "#FFD700"
COLOR_ORANGE = "#FFA500"
COLOR_DARK_ORANGE = "#FF8C00"
COLOR_LIGHT_ORANGE = "#FFB347"
COLOR_WHITE = "#8B0000"    
COLOR_DARK_BROWN = "#8B4513"
COLOR_PURPLE = "#800080"
COLOR_GREEN = "#228B22"    
R_OUTER = 300
R_RING_INNER = 250
R_RING_OUTER = 290
R_MIDDLE_RING_INNER = 240
R_MIDDLE_RING_OUTER = 250
R_OUTER_PETAL_OFFSET = 160
R_OUTER_PETAL_ARC = 80
R_OUTER_PETAL_EXT = 60
R_INNER_PETAL_OFFSET = 90
R_INNER_PETAL_ARC = 50
R_INNER_PETAL_EXT = 40
R_EXTRA_PETAL_OFFSET = 60
R_EXTRA_PETAL_ARC = 40
R_EXTRA_PETAL_EXT = 30

# ---------- Setup ----------
screen = turtle.Screen()
screen.setup(W, H)
screen.bgcolor(BG_COLOR)
screen.title("Exact Pookalam Design - Polished with Ambient Fill")
screen.tracer(0, 0)

t = turtle.Turtle(visible=False)
t.speed(0)
t.hideturtle()


def go_home():
    t.up()
    t.home()
    t.setheading(0)

def filled_circle(radius, color, outline=None, outline_width=2):
    go_home()
    t.goto(0, -radius)
    t.setheading(0)
    t.fillcolor(color)
    t.pencolor(outline if outline else color)
    t.pensize(outline_width)
    t.down()
    t.begin_fill()
    t.circle(radius)
    t.end_fill()
    t.up()

def annulus(r_in, r_out, color, outline=None, outline_width=2):
    filled_circle(r_out, color, outline, outline_width)
    filled_circle(r_in, BG_COLOR)

def draw_segment(start_angle, extent, r_inner, r_outer, color, outline=True):
    angle_step = 2
    angles = [start_angle + i for i in range(0, int(extent)+1, angle_step)]
    points = []
    for angle in angles:
        rad = radians(angle)
        x = r_outer * cos(rad)
        y = r_outer * sin(rad)
        points.append((x, y))
    for angle in reversed(angles):
        rad = radians(angle)
        x = r_inner * cos(rad)
        y = r_inner * sin(rad)
        points.append((x, y))
    go_home()
    t.fillcolor(color)
    t.pencolor(COLOR_DARK_BROWN if outline else color)
    t.pensize(2 if outline else 1)
    t.goto(points[0])
    t.down()
    t.begin_fill()
    for x, y in points[1:]:
        t.goto(x, y)
    t.goto(points[0])
    t.end_fill()
    t.up()

def draw_checker_ring():
    num_segments = 12
    colors = [COLOR_YELLOW, COLOR_ORANGE, COLOR_WHITE, COLOR_DARK_BROWN]
    extent = 360 / num_segments
    for i in range(num_segments):
        color = colors[i % len(colors)]
        draw_segment(i * extent, extent, R_RING_INNER, R_RING_OUTER, color)

def draw_middle_ring():
    annulus(R_MIDDLE_RING_INNER, R_MIDDLE_RING_OUTER, COLOR_PURPLE)

def sample_petal_points(angle_deg, offset, arc_r, extent_deg, n=40):
    ang = radians(angle_deg)
    sx = offset * cos(ang)
    sy = offset * sin(ang)
    theta0 = ang + pi/2
    ext_rad = radians(extent_deg)
    pts = []
    for i in range(n+1):
        th = theta0 + ext_rad * (i / n)
        x = sx + arc_r * cos(th)
        y = sy + arc_r * sin(th)
        pts.append((x, y))
    theta1 = theta0 + pi
    for i in range(n+1):
        th = theta1 + ext_rad * (i / n)
        x = sx + arc_r * cos(th)
        y = sy + arc_r * sin(th)
        pts.append((x, y))
    return pts

def draw_petal(angle_deg, offset, arc_r, extent_deg, colors):
    num_layers = len(colors)
    band_step = 8
    arc_step = 4
    for i, color in enumerate(colors):
        cur_offset = offset - i * band_step
        cur_arc = arc_r - i * arc_step
        cur_extent = extent_deg - i * 0.5
        pts = sample_petal_points(angle_deg, cur_offset, cur_arc, cur_extent)
        go_home()
        t.fillcolor(color)
        t.pencolor(COLOR_DARK_BROWN)
        t.pensize(1)
        t.goto(pts[0])
        t.down()
        t.begin_fill()
        for x, y in pts[1:]:
            t.goto(x, y)
        t.goto(pts[0])
        t.end_fill()
        t.up()

def draw_outer_petals():
    for i in range(8):
        angle = i * 45
        draw_petal(angle, R_OUTER_PETAL_OFFSET, R_OUTER_PETAL_ARC, R_OUTER_PETAL_EXT,
                   [COLOR_DARK_ORANGE, COLOR_LIGHT_ORANGE, COLOR_ORANGE, COLOR_YELLOW])

def draw_inner_petals():
    for i in range(4):
        angle = i * 90 + 45
        draw_petal(angle, R_INNER_PETAL_OFFSET, R_INNER_PETAL_ARC, R_INNER_PETAL_EXT,
                   [COLOR_DARK_ORANGE, COLOR_ORANGE, COLOR_LIGHT_ORANGE, COLOR_YELLOW, COLOR_WHITE])

def draw_extra_inner_petals():
    for i in range(12):
        angle = i * (360 / 12)
        draw_petal(angle, R_EXTRA_PETAL_OFFSET, R_EXTRA_PETAL_ARC, R_EXTRA_PETAL_EXT,
                   [COLOR_GREEN, COLOR_LIGHT_ORANGE, COLOR_ORANGE])

def draw_outer_outline():
    annulus(R_RING_OUTER, R_RING_OUTER + 4, COLOR_DARK_BROWN)

def draw_inner_outline():
    annulus(R_RING_INNER - 4, R_RING_INNER, COLOR_DARK_BROWN)


def fill_outer_gap_ambient():
    """
    Fill the blank space between outer ring and inner petals with ambient concentric circles.
    """
    colors = ["#C0BE85", "#FFE4B5", "#FFDEAD", "#FFEFD5"]  
    steps = len(colors)
    r_start = R_RING_INNER + 2   
    r_end = R_MIDDLE_RING_OUTER - 2  

    for i, color in enumerate(colors):
        r = r_start + (r_end - r_start) * (i / steps)
        filled_circle(r, color)

def build_pookalam():
    draw_outer_outline()
    draw_inner_outline()
    draw_checker_ring()
    fill_outer_gap_ambient()   
    draw_middle_ring()
    draw_outer_petals()
    draw_inner_petals()
    draw_extra_inner_petals()

if __name__ == "__main__":
    build_pookalam()
    screen.update()
    turtle.done()