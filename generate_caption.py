# CaptionGenerator.py

import os
import pickle
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.vgg16 import VGG16 , preprocess_input
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical, plot_model
from tensorflow.keras.layers import Input , Dense , LSTM , Embedding , Dropout , add

import numpy as np

BASE_DIR = 'input/flickr8k/'
WORKING_DIR = 'working/'
features ={}

def clean(mapping):
    for key, captions in mapping.items():
        for i in range(len(captions)):
            caption = captions[i]
            caption = caption.lower()
            caption = caption.replace('[^A-Za-z]', '')
            caption = caption.replace('\s+', ' ')
            caption = 'startseq ' + " ".join([word for word in caption.split() if len(word) > 1]) + ' endseq'
            captions[i] = caption


def load_tokenizer(captions_path):
    with open(captions_path, 'r') as f:
        captions_doc = f.read()

    mapping = {}

    for line in captions_doc.split('\n'):
        tokens = line.split(',')
        if len(line) < 2:
            continue
        image_id, caption = tokens[0], tokens[1:]
        image_id = image_id.split('.')[0]
        caption = " ".join(caption)
        if image_id not in mapping:
            mapping[image_id] = []
        mapping[image_id].append(caption)

    clean(mapping)

    all_captions = []
    for key in mapping:
        for caption in mapping[key]:
            all_captions.append(caption)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(all_captions)

    return tokenizer


def load_trained_model(model_path):
    model = load_model(model_path)
    return model


def predict_caption(model, image, tokenizer, max_length):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], max_length)
        yhat = model.predict([image, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = idx_to_word(yhat, tokenizer)
        if word is None:
            break
        in_text += " " + word
        if word == 'endseq':
            break
    caption = in_text.replace('startseq', '').replace('endseq', '').strip()
    return caption



def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def generate_caption(image_name):
    model = VGG16()

    # restructure model
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)

    #dont use this load - instead generate feature fn to
    #load the image from file
    img_path = os.path.join('static', 'uploads', image_name)
    image = load_img(img_path, target_size=(224, 224))
    #     # convert image pixels to numpy array
    image = img_to_array(image)
    # reshape data for model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    #     # preprocess image for vgg
    image = preprocess_input(image)
    #     # extract features
    feature = model.predict(image, verbose=0)
    #     # get image ID
    image_id = image_name.split('.')[0]
    #     # store feature
    features[image_id] = feature



    with open(os.path.join(BASE_DIR, 'captions.txt'), 'r') as f:
        next(f)
        captions_doc = f.read()

    mapping = {}

    for line in captions_doc.split('\n'):
        tokens = line.split(',')
        if len(line) < 2:
            continue
        L_image_id, caption = tokens[0], tokens[1:]
        L_image_id = L_image_id.split('.')[0]



        caption = " ".join(caption)
        if L_image_id not in mapping:
            mapping[L_image_id] = []
        mapping[L_image_id].append(caption)

    clean(mapping)

    all_captions = []
    for key in mapping:
        for caption in mapping[key]:
            all_captions.append(caption)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(all_captions)
    vocab_size = len(tokenizer.word_index) + 1
    max_length = max(len(caption.split()) for caption in all_captions)

    model = load_trained_model(os.path.join(WORKING_DIR, "best_model.h5"))
    predicted_caption = predict_caption(model, features[image_id], tokenizer, max_length)

    return predicted_caption
