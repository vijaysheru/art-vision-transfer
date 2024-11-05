# **Artistic Vision Transfer**

## **Overview**
Artistic Vision Transfer is a web application that allows users to upload their own images and transform them into stylized artworks using neural style transfer. The project leverages deep learning models such as MobileNetV2 or EfficientNet for efficient, real-time style application.

## **Features**
- Upload a content image and a style image to transform the content into the chosen artistic style.
- Real-time style transfer with a user-friendly interface.
- Download the stylized image once processing is complete.
- Optimized for fast performance without sacrificing quality.

---

## **Installation and Setup**

### **1. Clone the Repository**
First, clone the repository to your local machine using the following command:
```bash
git clone https://github.com/yourusername/art-vision-transfer.git
cd art-vision-transfer
```

### **2. Create and Activate a Virtual Environment**
Create a virtual environment to isolate your project dependencies:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### **3. Install Dependencies**
Install the required Python packages by running:
```bash
pip install -r requirements.txt
```

### **4. Install TensorFlow**
Ensure you have TensorFlow installed. If it's not listed in `requirements.txt`, you can install it separately:
```bash
pip install tensorflow==2.14.0
```

### **5. Verify the Installation**
Check if all dependencies are installed correctly:
```bash
python -m flask --version
python -c "import tensorflow as tf; print(tf.__version__)"
```

---

## **Running the Application Locally**

### **1. Start the Flask Application**
To run the web application on your local machine, execute:
```bash
python app.py
```
This will start the server, and you should see output indicating that the application is running on `http://127.0.0.1:5000/`.

### **2. Access the Application**
Open your web browser and navigate to `http://127.0.0.1:5000/` to access the application.

### **3. Upload an Image and Apply a Style**
- Upload a **content image** from your device.
- Select or upload a **style image**.
- Click "Submit" to transform your content image with the selected artistic style.
- Once the process is complete, you can preview and download the stylized image.

---

## **Project Structure**
```plaintext
art-vision-transfer/
│
├── app.py                  # Main application script
├── models/
│   ├── style_transfer.py    # Neural style transfer model logic
│   └── recommendation.py    # (Optional) Style recommendation logic
├── static/
│   └── css/                 # Stylesheets for the frontend
├── templates/
│   └── index.html           # Frontend HTML template
├── requirements.txt         # Project dependencies
├── README.md                # Project README file
└── utils/
    └── __init__.py          # Utility functions
```

---

## **System Requirements**
- Python 3.8 or higher
- TensorFlow 2.14.0
- Flask 2.0.1
- Additional packages listed in `requirements.txt`

---

## **Usage Notes**
- The model can process images of up to **2MB** in size for optimal performance.
- The application processes each request in real-time, so larger images may take longer to stylize.
- Feel free to modify the backend to suit different neural network architectures or enhance frontend design.

---

## **FAQ**

### **1. How can I change the style transfer model?**
You can modify the `models/style_transfer.py` file to swap MobileNetV2 with other pre-trained models like EfficientNet, VGG19, etc. Be sure to install any necessary dependencies if you switch models.

### **2. How do I deploy this application?**
The app is set up for local testing, but you can deploy it to cloud platforms such as AWS or Heroku. A `Procfile` is included to help with deployment on Heroku.

### **3. What if TensorFlow doesn't work on my machine?**
Make sure you're using a compatible Python version (3.8+) and check your system’s compatibility with TensorFlow. Refer to [TensorFlow installation guide](https://www.tensorflow.org/install) for system-specific instructions.

---

## **Contributing**
Contributions are welcome! Please fork the repository and submit pull requests for any improvements or features you'd like to add.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---
