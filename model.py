import random

classes = ["Cat", "Dog", "Car", "Tree"]

def classify_image(image_path):
    prediction = random.choice(classes)
    confidence = round(random.uniform(70, 99), 2)
    return prediction, confidence

