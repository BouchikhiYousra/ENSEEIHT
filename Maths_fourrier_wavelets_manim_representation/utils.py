import numpy as np
from manim import *
from drawingInterface import DrawingInterface
from scipy import interpolate
import matplotlib.pyplot as plt
import PIL


def getTexComponents(tex = "$\Sigma$"):
    path = VMobject()
    shape = Tex(tex)
    for sp in shape.family_members_with_points():
        path.append_points(sp.get_points())
    path = path[0]

    x = path.get_all_points()[:, 0]
    y = path.get_all_points()[:, 1]

    points = x + 1j * y
    components = [points]
    return components

def getDrawingComponents(size = 780):
    drawingInterface = DrawingInterface((size, size))
    shapes = drawingInterface.get_shapes()

    all_points = [] # all components combined
    for shape in shapes:
        x_values, y_values = decompose_points(shape)
        all_points = x_values + 1j * (780-y_values)
    
    all_points = np.array(all_points)
    moy = np.mean(all_points)
    max = np.amax(np.abs(all_points))

    components = []
    for shape in shapes:
        x_values, y_values = decompose_points(shape)
        points = (x_values + 1j * (780-y_values) - moy)/max
        components.append(points)

    return components

def getImageComponents(image_path):
    im = PIL.Image.open(image_path).convert('L')
    im = im.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    im = im.resize((200,200))
    
    points = []
    cs = plt.contour(im, levels = [245,255])
    paths = cs.collections[0].get_paths()
    for p in paths:
        pathsegs = p.iter_segments()
        for (x_pt, y_pt), _ in pathsegs:
            points.append(x_pt + 1j * y_pt)

    points = np.array(points)
    moy = np.mean(points)
    max = np.amax(np.abs(points))
    
    components = []
    comp = [points[0]]
    for idx in range(len(points) - 1):
        pt0 = points[idx]
        pt1 = points[idx+1]
        d = np.linalg.norm(pt0 - pt1)
        if d < 5: # distance max entre deux points voisins.
            comp.append(pt1)
        else:
            components.append((np.array(comp) - moy)/150) # pour l'affichage met 1, sinon fait max
            comp = [pt1]

    lengths = [len(c) for c in components]
    indices = np.flip(np.argsort(lengths))
    components = np.array(components)
    components = components[indices] # prioritize big components
    return components

def decompose_points(points):
    x_values, y_values = [], []
    for pt in points:
        x, y = pt
        x_values.append(x)
        y_values.append(y)
    return np.array(x_values), np.array(y_values)

def compose_points(x_values, y_values):
    assert len(x_values) == len(y_values)

    points = []
    for x, y in zip(x_values, y_values):
        points.append((x,y))
    return np.array(points)