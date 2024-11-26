# prompt: shape detection using web cam streamlit 

import cv2
import numpy as np
import streamlit as st

def detect_shapes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

        x, y, w, h = cv2.boundingRect(approx)
        
        if len(approx) == 3:
            shape = "Triangle"
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
        elif len(approx) == 4:
            aspect_ratio = float(w) / h
            if 0.95 <= aspect_ratio <= 1.05:
                shape = "Square"
                cv2.drawContours(image, [approx], -1, (0, 0, 255), 2)
            else:
                shape = "Rectangle"
                cv2.drawContours(image, [approx], -1, (0, 255, 255), 2)
        elif len(approx) == 5:
            shape = "Pentagon"
            cv2.drawContours(image, [approx], -1, (255, 0, 0), 2)
        elif len(approx) == 10:
            shape = "Star"
            cv2.drawContours(image, [approx], -1, (255, 255, 0), 2)
        
        else:
            shape="circle"
            cv2.drawContours(image, [approx], -1, (255, 255, 0), 2)

        cv2.putText(image, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    return image


st.title("Shape Detection using Webcam")
run = st.checkbox('Run')
FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

while run:
    _, frame = camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = detect_shapes(frame)
    FRAME_WINDOW.image(frame)
else:
    st.write('Stopped')