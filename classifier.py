import tensorflow as tf
import numpy as np
from policy import get_bin_rule
from e_waste_locator import find_nearest_e_waste_centre

CLASS_NAMES = ["dry_waste", "e_waste", "sanitary_waste", "wet_waste"]
IMAGE_SIZE  = (224, 224)

def load_model():
    model = tf.keras.models.load_model('saved_model/waste_classifier.keras')
    return model

def preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_image(image, channels=3)
    image = tf.image.resize(image, IMAGE_SIZE)
    image = image / 255.0
    image = tf.expand_dims(image, axis=0)
    return image

def predict(model, image_path):
    image        = preprocess_image(image_path)
    predictions  = model.predict(image)
    class_index  = np.argmax(predictions[0])
    confidence   = float(predictions[0][class_index]) * 100
    class_name   = CLASS_NAMES[class_index]
    return class_name, confidence

def classify(image_path, lat=28.6139, lon=77.2090):
    model               = load_model()
    class_name, confidence = predict(model, image_path)
    bin_rule            = get_bin_rule(class_name)

    if class_name == "e_waste":
        centre = find_nearest_ewaste_centre(lat, lon)
        return {
            "class"     : class_name,
            "confidence": f"{confidence:.1f}%",
            "bin"       : bin_rule["bin"],
            "tip"       : bin_rule["tip"],
            "law"       : bin_rule["law"],
            "centre"    : centre
        }

    return {
        "class"     : class_name,
        "confidence": f"{confidence:.1f}%",
        "bin"       : bin_rule["bin"],
        "color"    : bin_rule["color"],
        "tip"       : bin_rule["tip"],
        "law"       : bin_rule["law"]
    }

# TEST — remove after testing
if __name__ == "__main__":
    result = classify("data/test/dry_waste/cardboard_5.jpg")
    print(result)
