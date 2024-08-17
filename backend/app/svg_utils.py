import svgwrite
import numpy as np
import cv2 as cv
from svgpathtools import svg2paths2

def image_to_svg(img, contours_to_draw, circle_info, bounding_box, lines_to_draw, filename="output.svg"):
    dwg = svgwrite.Drawing(filename, profile='tiny')
    height, width, _ = img.shape
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='white'))

    for contour, color in contours_to_draw:
        contour = np.array(contour)
        for i in range(len(contour)):
            pt1 = (contour[i][0][0], contour[i][0][1])
            pt2 = (contour[(i + 1) % len(contour)][0][0], contour[(i + 1) % len(contour)][0][1])
            dwg.add(dwg.line(start=pt1, end=pt2, stroke=color))

    for center, radius in circle_info:
        dwg.add(dwg.circle(center=center, r=radius, stroke='black', fill='none'))

    for box in bounding_box:
        box = np.array(box)
        points = [tuple(point) for point in box]
        dwg.add(dwg.polygon(points=points, stroke='black', fill='none'))

    dwg.save()

def svg2polylines(svg_path):
    paths, attributes = svg2paths2(svg_path)
    # Convert SVG paths to polylines
    polylines = []
    for path in paths:
        for segment in path:
            if segment.start != segment.end:
                polylines.append((segment.start.real, segment.start.imag, segment.end.real, segment.end.imag))
    return polylines
