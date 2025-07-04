import joblib
import json
import numpy as np
import base64
import cv2
from server.wavelet import w2d
import os

__class_name_to_number = {}
__class_number_to_name = {}
__model = None

# Simplifies long dataset folder names to match frontend element IDs
def simplify_class_name(full_name):
    mapping = {
        'bill_gates_face_png___Google_Search': 'bill_gates',
        'elon_musk_face___Google_Search': 'elon_musk',
        'maria_sharapova_face___Google_Search': 'maria_sharapova',
        'mark_zuckerberg_face_png___Google_Search': 'mark_zuckerberg',
        'ms_dhoni_face___Google_Search': 'ms_dhoni'
    }
    return mapping.get(full_name, full_name)

def classify_image(image_base64_data, file_path=None):
    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)
    result = []

    for img in imgs:
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32*32*3, 1), scalled_img_har.reshape(32*32, 1)))

        len_image_array = 32*32*3 + 32*32
        final = combined_img.reshape(1, len_image_array).astype(float)

        predicted_class_number = __model.predict(final)[0]
        predicted_class_name = class_number_to_name(predicted_class_number)
        simplified_class_name = simplify_class_name(predicted_class_name)

        # Create class dictionary with simplified names
        simplified_class_dict = {
            simplify_class_name(original_name): index
            for original_name, index in __class_name_to_number.items()
        }

        result.append({
            'class': simplified_class_name,
            'class_probability': np.around(__model.predict_proba(final) * 100, 2).tolist()[0],
            'class_dictionary': simplified_class_dict
        })

    return result

def class_number_to_name(class_num):
    return __class_number_to_name[class_num]

def load_saved_artifacts():
    print("📦 Loading saved artifacts...")
    global __class_name_to_number
    global __class_number_to_name
    global __model

    model_path = os.path.join(os.path.dirname(__file__), '..', 'model')
    print("📁 Model path resolved to:", model_path)

    try:
        class_dict_path = os.path.join(model_path, "class_dictionary.json")
        model_file_path = os.path.join(model_path, "save_model.pkl")

        print("🔍 Checking file:", class_dict_path, os.path.exists(class_dict_path))
        print("🔍 Checking file:", model_file_path, os.path.exists(model_file_path))

        with open(class_dict_path, "r") as f:
            __class_name_to_number = json.load(f)
            __class_number_to_name = {v: k for k, v in __class_name_to_number.items()}

        with open(model_file_path, 'rb') as f:
            __model = joblib.load(f)

        print("✅ Model loaded successfully")

    except Exception as e:
        print("❌ Exception while loading artifacts:", str(e))


def get_cv2_image_from_base64_string(b64str):
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)
    return cropped_faces

def get_b64_test_image_for_ELON_MUSK():
    with open("server/b64.txt") as f:
        return f.read()

if __name__ == '__main__':
    load_saved_artifacts()
    print(classify_image(get_b64_test_image_for_ELON_MUSK(), None))