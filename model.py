import random

classes = ["Cat", "Dog", "Car", "Tree"]

def classify_image(image_path):
    prediction = random.choice(classes)
    return prediction