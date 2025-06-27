# 🧠📸 Famous Face Classifier

This project is a **machine learning-powered web application** that classifies images of globally recognized personalities using face detection and feature extraction techniques. It utilizes **OpenCV** for face detection with **Haar cascades**, applies **Wavelet Transforms** for rich feature extraction, and finally uses a trained **ML model** for prediction.

---

## 👤 Recognizable Personalities

The model is trained to recognize and classify the following personalities:

- **Bill Gates**
- **Elon Musk**
- **Mark Zuckerberg**
- **Maria Sharapova**
- **MS Dhoni**

---

## 🔍 Features

- 📂 Drag-and-drop image upload (via Dropzone.js)
- 🧠 Detects and crops faces with at least **two eyes** using OpenCV
- 🌊 Applies **Wavelet Transform** for texture-based feature extraction
- 🔍 Classifies using a trained **scikit-learn model**
- 📊 Displays predicted **name** and **confidence scores**

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, JavaScript (Dropzone.js, jQuery)
- **Backend:** Python (Flask)
- **Libraries:** OpenCV, NumPy, scikit-learn, joblib
- **ML Model:** Support Vector Machine (SVM) or similar (custom trained)
- **Face Detection:** Haar Cascades (frontal face + eyes)
- **Image Format:** Base64-encoded or direct file upload

---

## 🧠 How It Works

1. **Face Detection**: Haar Cascade Classifier detects face + 2 eyes.
2. **Cropping**: Extracts only valid face regions.
3. **Feature Extraction**:
   - Raw pixel values
   - Wavelet-transformed values
4. **Classification**: Feature vector passed to a trained ML model (e.g., SVM).
5. **Output**: Class label and per-class probability scores shown.

---

## 📸 Screenshots

<img width="920" alt="image" src="https://github.com/user-attachments/assets/055cfe13-c85b-4bfa-a251-bfb857182b35" />
<img width="922" alt="image" src="https://github.com/user-attachments/assets/4483bbdf-7984-42e9-81a3-31c4933516a5" />

---

## 🌐 Future Enhancements

- Add more celebrities
- Upgrade to **deep learning (CNN)**-based face recognition
- Deploy online using platforms like:
  - [Render](https://render.com/)

---

## 👨‍💻 Author

**Aashutosh Yadav**  
B.Tech CSSE | KIIT | ML Enthusiast

- 📫 [LinkedIn](http://www.linkedin.com/in/aashutosh-yadav-1a07352a5)

---

