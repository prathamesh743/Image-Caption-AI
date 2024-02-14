# Image-Caption-AI
Building an automated image captioning system involves combining computer vision and natural language processing techniques

For Reff -https://www.kaggle.com/code/zohaib123/image-caption-generator-using-cnn-and-lstm/notebook 

Project Overview
**Image-Caption-AI** is an exciting project inspired by the Kaggle competition on Image Caption Generation using CNN and LSTM. The goal is to automatically generate descriptive captions for images, combining the power of computer vision and natural language processing. The project utilizes the TensorFlow library, with a focus on the VGG16 model for image feature extraction and LSTM for sequence generation.

## Tech Stack

- TensorFlow
- Flask
- PIL (Python Imaging Library)

## Directory Structure
Image-Caption-AI/
│   app.py
│   generate_caption.py
│   README.md
│   requirements.txt
├── input/
│   └── flickr8k/
│       ├── images/
│       └── captions.txt
├── working/
│   ├── Trained model
│   └── features.pkl
├── templates/
│   └── index.html
└── static/
    ├── uploads/
    └── style/



## Setup Instructions
1. Clone the repository:
   git clone https://github.com/your-username/Image-Caption-AI.git
   cd Image-Caption-AI
2. Create and activate a virtual environment (recommended):
    conda create --name image-caption-env python=3.8 (u can use any py version.)
    conda activate image-caption-env

3. Install the required dependencies:
    pip install -r requirements.txt

4. Run the Flask app:
    python app.py
5. Open your web browser and navigate to http://localhost:5000 to use the Image Captioner app.

**Usage**
Visit the web application at http://localhost:5000.
Upload an image using the provided form.
Click "Generate Caption" to see the AI-generated caption for the uploaded image.

**Notes**
The input/flickr8k directory contains the dataset, including an images folder and a captions.txt file.
The working directory stores the trained model and features.pkl file.
The static directory includes subfolders for uploaded images and styles.