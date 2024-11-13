import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
import triangle as tr

A = None
initial_thickness = 0.1
initial_angle = 20
selected_vertices = []

def rotate_90_left(vector):
    x, y = vector
    return [-y, x]

def normalize(vector):
    return vector / np.linalg.norm(vector)

def line_distance(line_point, line_normal, point):
    return np.dot(line_normal, point - line_point)

def compare_vertices(vertex1, vertex2):
    return vertex1[0] == vertex2[0] and vertex1[1] == vertex2[1]

def create_triangulation():
    global B
    B = tr.triangulate(A, f'q{initial_angle}a{initial_thickness}')
    print(B.items())

def update_plot():
    ax.clear()
    tr.plot(ax, **B)
    
    for vertex in selected_vertices:
        ax.scatter(vertex[0], vertex[1], color='red', s=100)
    
    plt.draw()


def submit_vertices(text):
    global A
    try:
        vertices = [tuple(map(float, v.split(','))) for v in text.split(';')]
        vertices = np.array(vertices)
        
        if vertices.shape[0] < 3:
            print("Будь ласка, введіть принаймні 3 вершини.")
            return
        
        A = dict(vertices=vertices)
        clear_vertices()
        create_triangulation()
        update_plot()
    except ValueError:
        print("Неправильний формат введення. Використовуйте формат 'x1,y1;x2,y2;...'")

A = dict(vertices=np.array(((0, 0), (0, 2), (1, 2), (1, 0))))
create_triangulation()

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)

tri_plot = tr.plot(ax, **B)

ax_slider_thickness = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_slider_angle = plt.axes([0.2, 0.2, 0.65, 0.03], facecolor='lightgoldenrodyellow')

slider_thickness = Slider(ax_slider_thickness, 'Thickness', 0.001, 1.0, valinit=initial_thickness)
slider_angle = Slider(ax_slider_angle, 'Angle', 1, 30, valinit=initial_angle)


def clear_vertices():
    selected_vertices.clear()
    update_plot()

def update(val):
    global initial_thickness, initial_angle
    initial_thickness = slider_thickness.val
    initial_angle = slider_angle.val
    clear_vertices()
    create_triangulation()
    update_plot()

slider_thickness.on_changed(update)
slider_angle.on_changed(update)

ax_textbox = plt.axes([0.5, 0.9, 0.35, 0.05])
text_box = TextBox(ax_textbox, 'Enter vertices (x1,y1;x2,y2;...):', initial='0,0;1,0;1,1;0,1')
text_box.on_submit(submit_vertices)

plt.show()
