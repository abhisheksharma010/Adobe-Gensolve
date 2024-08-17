import pandas as pd
import numpy as np
import cv2 as cv
from io import BytesIO
from .svg_utils import image_to_svg, svg2polylines

def process_csv_and_generate_image(polylines):
    # Initialize a black image
    img = np.zeros((512, 512), dtype=np.uint8)
    current_polyline = None

    # Draw lines based on polylines
    for i in range(len(polylines)):
        if [polylines.iloc[i, 0], polylines.iloc[i, 1]] != current_polyline:
            current_polyline = [polylines.iloc[i, 0], polylines.iloc[i, 1]]
        else:
            pt1 = (int(round(polylines.iloc[i-1, 2])), int(round(polylines.iloc[i-1, 3])))
            pt2 = (int(round(polylines.iloc[i, 2])), int(round(polylines.iloc[i, 3])))
            cv.line(img, pt1, pt2, color=255, thickness=1)

    # Save CSV to a buffer
    input_csv_df = pd.DataFrame(polylines)
    input_csv_buffer = BytesIO()
    input_csv_df.to_csv(input_csv_buffer, index=False, header=False)
    input_csv_buffer.seek(0)

    # Process image
    input_image = img.copy()
    input_image_path = 'backend/input_image.png'
    cv.imwrite(input_image_path, input_image)

    _, input_img_encoded = cv.imencode('.png', input_image)
    input_img_bytes = input_img_encoded.tobytes()

    # Apply blurring and thresholding
    blur = cv.blur(img, (1, 1))
    _, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Convert to RGB
    img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    shape_info = []

    # Analyze contours and classify shapes
    for i, contour in enumerate(contours):
        if cv.contourArea(contour) < 3:
            shape_info.append(("unidentified", contour))
            continue

        eps = 0.01 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, eps, True)

        shape = "unidentified"
        peri = cv.arcLength(contour, True)
        area = cv.contourArea(contour)
        vertices = len(approx)

        if vertices >= 7:
            (x, y), radius = cv.minEnclosingCircle(contour)
            circle_area = np.pi * (radius ** 2)
            if abs(area - circle_area) < 0.2 * circle_area:
                center = (int(x), int(y))
                shape = "circle"
                shape_info.append((shape, (center, int(radius), contour)))
                continue
            circularity = 4 * np.pi * area / (peri ** 2)
            if 0.43 < circularity < 0.79:
                shape_info.append(("unidentified", contour))
                continue
        else:
            eps = 0.02 * cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, eps, True)
            shape = "unidentified"
            peri = cv.arcLength(contour, True)
            area = cv.contourArea(contour)
            vertices = len(approx)
            if vertices == 3:
                shape = "triangle"
            elif vertices == 4:
                shape = "rectangle"
            elif vertices == 5:
                shape = "pentagon"
            elif vertices == 6:
                shape = "hexagon"
            elif vertices == 7:
                if peri / area > 0.05:
                    shape_info.append(("unidentified", contour))
                    continue
                shape = "heptagon"
            elif vertices == 8:
                shape = "octagon"
            elif vertices == 9:
                shape = "nonagon"
            elif vertices == 10:
                if peri / area > 0.105:
                    shape_info.append(("unidentified", contour))
                    continue
                shape = "circle"

        if shape != "unidentified":
            shape_info.append((shape, (contour, approx)))
        else:
            shape_info.append((shape, contour))

    mask = np.ones((512, 512), dtype=np.uint8) * 255
    circleInfo = []
    boundingBox = []
    contoursToDraw = []
    finalContours = []
    linesToDraw = []

    # Draw shapes on mask and image
    for shape, contour in shape_info:
        if shape == "triangle":
            cv.drawContours(mask, [contour[0]], -1, 0, 1)
            contoursToDraw.append((contour[1], (0, 128, 0)))
        elif shape == "rectangle":
            rect = cv.minAreaRect(contour[0])
            box = cv.boxPoints(rect)
            box = box.astype(int)
            boundingBox.append(box)
            cv.drawContours(mask, [contour[0]], -1, 0, 1)
        elif shape == "pentagon":
            cv.drawContours(mask, [contour[0]], -1, 0, 1)
            contoursToDraw.append((contour[1], (128, 0, 128)))
        elif shape == "hexagon":
            cv.drawContours(mask, [contour[0]], -1, 0, 1)
            contoursToDraw.append((contour[1], (0, 128, 128)))
        elif shape == "heptagon":
            cv.drawContours(mask, [contour[0]], -1, 0, 1)
            contoursToDraw.append((contour[1], (255, 165, 0)))
        elif shape == "octagon":
            cv.drawContours(mask, [contour[0]], -1, 0, 1)
            contoursToDraw.append((contour[1], (0, 165, 255)))
        elif shape == "nonagon":
            cv.drawContours(mask, [contour[0]], -1, 0, 1)
            contoursToDraw.append((contour[1], (75, 0, 130)))
        elif shape == "circle":
            center, radius = contour[0], contour[1]
            circleInfo.append((center, radius))
            cv.drawContours(mask, [contour[2]], -1, 0, 1)
        else:
            cv.drawContours(img, [contour], -1, (255, 255, 0), 1)
            finalContours.append((contour, (255, 255, 0)))

    img = cv.bitwise_and(img, img, mask=mask)

    # Draw circles on image
    for info in circleInfo:
        center, radius = info
        cv.circle(img, center, radius, (0, 255, 0), 1)
        cv.circle(img, center, 1, (0, 0, 255), 2)

    # Save processed image
    cv.imwrite(input_image_path, img)

    # Encode processed image to bytes
    output_img_bytes = BytesIO()
    _, encoded_img = cv.imencode('.png', img)
    output_img_bytes.write(encoded_img)
    output_img_bytes.seek(0)

    # Convert image to SVG
    svg_img = image_to_svg(img, contoursToDraw, circleInfo, boundingBox, linesToDraw)

    return output_img_bytes.getvalue(), input_csv_buffer.getvalue(), svg_img, img
