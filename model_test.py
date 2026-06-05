import cv2
import tensorflow as tf
import numpy as np

CLASS_NAMES = ["dry_waste", "e_waste", "sanitary_waste", "wet_waste"]
IMAGE_SIZE  = (224, 224)

BIN_COLOURS = {
    "dry_waste"     : (255, 0,   0  ),
    "wet_waste"     : (0,   255, 0  ),
    "e_waste"       : (0,   0,   255),
    "sanitary_waste": (0,   165, 255)
}

BIN_NAMES = {
    "dry_waste"     : "Blue Bin",
    "wet_waste"     : "Green Bin",
    "e_waste"       : "DO NOT BIN - E-Waste!",
    "sanitary_waste": "Black Bin"
}

print("Loading model...")
model = tf.keras.models.load_model('saved_model/best_model.h5')
print("Model loaded! Opening camera...")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]

    # calculate square position — centre of screen
    square_size = 300
    x1 = (width  // 2) - (square_size // 2)
    y1 = (height // 2) - (square_size // 2)
    x2 = x1 + square_size
    y2 = y1 + square_size

    # crop only the area inside the square
    roi = frame[y1:y2, x1:x2]

    # preprocess only the ROI
    image = cv2.resize(roi, IMAGE_SIZE)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    # predict
    predictions = model.predict(image, verbose=0)
    class_index = np.argmax(predictions[0])
    confidence  = float(predictions[0][class_index]) * 100
    class_name  = CLASS_NAMES[class_index]
    colour      = BIN_COLOURS[class_name]
    bin_name    = BIN_NAMES[class_name]

    # draw square on screen
    # colour of square changes based on prediction
    cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 3)

    # small label above square
    cv2.putText(
        frame, "Place waste inside box",
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6, (255, 255, 255), 2
    )

    # result panel at bottom
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, height - 100), (width, height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # class name
    cv2.putText(
        frame, f"{class_name.replace('_', ' ').upper()}",
        (20, height - 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8, colour, 2
    )

    # bin name
    cv2.putText(
        frame, f"Bin: {bin_name}",
        (20, height - 38),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (255, 255, 255), 2
    )

    # confidence bar background
    cv2.rectangle(frame, (20, height - 20), (300, height - 8), (100, 100, 100), -1)

    # confidence bar fill
    bar_width = int((confidence / 100) * 280)
    cv2.rectangle(frame, (20, height - 20), (20 + bar_width, height - 8), colour, -1)

    # confidence percentage
    cv2.putText(
        frame, f"{confidence:.1f}%",
        (310, height - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 1
    )

    cv2.imshow("AI Waste Classifier", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()