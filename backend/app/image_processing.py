import cv2 as cv
import numpy as np

def process_image_and_shapes(img):
    # Initialize mask and shape info lists
    mask = np.ones(img.shape[:2], dtype=np.uint8) * 255
    contoursToDraw = []
    circleInfo = []
    boundingBox = []
    linesToDraw = []

    # Convert to grayscale and apply thresholding
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Find contours
    contours, _ = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    shape_info = []

    for contour in contours:
        if cv.contourArea(contour) < 3:
            shape_info.append(("unidentified", contour))
            continue

        eps = 0.01 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, eps, True)

        shape = "unidentified"
        peri = cv.arcLength(contour, True)
        area = cv.contourArea(contour)
        vertices = len(approx)

        # Shape detection logic
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

    # Process detected shapes and draw contours
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

    # Combine mask with original image
    img = cv.bitwise_and(img, img, mask=mask)

    # Draw circles and bounding boxes
    for center, radius in circleInfo:
        cv.circle(img, center, radius - 5, (0, 0, 255), 1)
        cv.line(img, (center[0] - radius, center[1]), (center[0] + radius, center[1]), (0, 255, 0), 1)
        cv.line(img, (center[0], center[1] - radius), (center[0], center[1] + radius), (0, 255, 0), 1)
        linesToDraw.append([(int(center[0] - radius), int(center[1])), (int(center[0] + radius), int(center[1]))])
        linesToDraw.append([(int(center[0]), int(center[1] - radius)), (int(center[0]), int(center[1] + radius))])

    for box in boundingBox:
        cv.drawContours(img, [box], 0, (255, 0, 0), 1)
        p1_h = tuple(box[1])
        p2_h = tuple(box[3])
        cv.line(img, p1_h, p2_h, (0, 255, 0), 1)
        linesToDraw.append([p1_h, p2_h])
        mid1 = tuple(((box[0] + box[1]) // 2).astype(int))
        mid2 = tuple(((box[1] + box[2]) // 2).astype(int))
        mid3 = tuple(((box[2] + box[3]) // 2).astype(int))
        mid4 = tuple(((box[3] + box[0]) // 2).astype(int))
        cv.line(img, mid1, mid3, (0, 255, 0), 1)
        cv.line(img, mid2, mid4, (0, 255, 0), 1)
        linesToDraw.append([mid1, mid3])
        linesToDraw.append([mid2, mid4])

    return img, contoursToDraw, circleInfo, boundingBox, linesToDraw
