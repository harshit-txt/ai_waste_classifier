import cv2
import tensorflow as tf
import numpy as np

CLASS_NAMES = ["dry_waste", "e_waste", "sanitary_waste", "wet_waste"]
IMAGE_SIZE  = (224, 224)

# load model
print("Loading model...")
model = tf.keras.models.load_model('saved_model/best_model.h5')
print("Model loaded! Opening camera...")

# open camera
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    # read frame from camera
    ret, frame = cap.read()
    if not ret:
        break

    # preprocess frame for model
    image = cv2.resize(frame, IMAGE_SIZE)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    # predict
    predictions = model.predict(image, verbose=0)
    class_index = np.argmax(predictions[0])
    confidence  = float(predictions[0][class_index]) * 100
    class_name  = CLASS_NAMES[class_index]

    # choose colour based on class
    colours = {
        "dry_waste"     : (255, 0, 0),    # blue
        "wet_waste"     : (0, 255, 0),    # green
        "e_waste"       : (0, 0, 255),    # red
        "sanitary_waste": (0, 165, 255)   # orange
    }
    colour = colours.get(class_name, (255, 255, 255))

    # draw prediction on screen
    cv2.putText(
        frame,
        f"{class_name} — {confidence:.1f}%",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1, colour, 2
    )

    # show the frame
    cv2.imshow("AI Waste Classifier", frame)

    # press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()