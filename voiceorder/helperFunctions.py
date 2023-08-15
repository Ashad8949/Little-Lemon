import os
import glob
import json
import requests
import pandas as pd
from zipfile import ZipFile
from difflib import SequenceMatcher
from nltk.corpus import stopwords
import nltk
from ibm_watson import SpeechToTextV1
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


def clean_text(text):
    stop_words = stopwords.words("english")
    stop_words.extend(["gimme", "lemme", "cause", "cuz", "imma", "gonna", "wanna", "please", "the", "and",
                       "gotta", "hafta", "woulda", "coulda", "shoulda", "howdy", "day", "can", "could",
                       "my", "mine", "I" "hey", "yoo", "deliver", "delivery", "delivered", "piece", "want",
                       "send", "sent", "order", "address", "addrez", "to", "too"])
    clean_texts = " ".join(
        [word.replace("X", "").replace("/", "") for word in text.split() if word.lower() not in stop_words])
    return clean_texts

def clean_text_order(text):
    stop_words = stopwords.words("english")
    stop_words.extend(["gimme", "lemme", "cause", "cuz", "imma", "gonna", "wanna", "please", "the", "and",
                       "gotta", "hafta", "woulda", "coulda", "shoulda", "howdy", "day", "can", "could",
                       "my", "mine", "I" "hey", "yoo", "deliver", "delivery", "delivered", "piece", "want",
                       "send", "sent", "order", "address", "addrez", "to", "too"])
    clean_texts = " ".join(
        [word.replace("X", "").replace("/", "") for word in text.split() if word.lower() not in stop_words])
    return clean_texts

def get_keywords(text):
    pizza_size = ["Tea", "Water", "Lassi"]
    pizza_topping = ["Samosa", "Pasta", "Salad", "Sushi", "Fried-Chicken", "Masala-Dosa", "Pizza", "Biryani"]
    order_size, order_topping = [], []
    check_size = True
    for word in text.split():
        if check_size:
            for size in pizza_size:
                if SequenceMatcher(None, word, size).ratio() > 0.4:
                    order_size.append(size)
                    check_size = False
        for topping in pizza_topping:
            if SequenceMatcher(None, word, topping).ratio() > 0.4:
                order_topping.append(topping)
                pizza_topping.remove(topping)
    return order_size, order_topping


def play_local_wav_file(file_name):
    with open(str("./" + file_name), "rb") as wav:
        data = wav.read(1024)
        while data:
            yield data
            data = wav.read(1024)


def read_zip_file(zip_name):
    files = str(os.getcwd() + "/" + zip_name + ".zip")
    with ZipFile(files, "r") as zip_object:
        zip_object.extractall()

    path = str(os.getcwd() + "/" + zip_name + "/*.wav")
    folder = glob.glob(path)
    return sorted(folder, reverse=False)


def save_audio(file, file_name):
    with open(file_name, "wb") as audio:
        for chunk in file.chunks():
            audio.write(chunk)
    print("file uploaded successfully")



def speech_to_text(file_name):
    # speech url
    authenticator = IAMAuthenticator('kYccPkylDaa_vCAnKKIWdc_w9KdGp_erhRsBraCTvklR')
    speech_to_text_ = SpeechToTextV1(authenticator=authenticator)
    speech_to_text_.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/cd4839c5-ca88-4151-972e-14e8742e2905')

    with open(file_name, 'rb') as audio_file:
        response = speech_to_text_.recognize(
            audio=audio_file,
            content_type='audio/wav',
            model='en-US_BroadbandModel'
        ).get_result()
    # get transcript from json result
    output = ""
    results_data = response["results"]
    for r in results_data:
        for transcript in r["alternatives"]:
            output = output + " " + transcript["transcript"]
    return output


def text_to_speech(texts, name, language):
    # remove the existing files in the folder
    file_pattern = f"*{name}*"
    files = glob.glob(file_pattern)

    for file in files:
        try:
            os.remove(file)
            print("Deleted file:", file)
        except OSError as e:
            print(f"Error deleting file {file}: {e}")

    # text url
    authenticator = IAMAuthenticator('Cv5AJEQ4bQ4AI9JNmzX99FsoYTHkL1zYHM7A9ZuTrbgV')
    text_to_speech_ = TextToSpeechV1(authenticator=authenticator)
    text_to_speech_.set_service_url('https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/f2f807e7-f708-4f26-81d0-9cd01266cb15')
    # create a data in JSON format to send as a parameter to the service
    words = json.dumps({"text": texts})
    # method to get the Voice data from the text service
    response = text_to_speech_.synthesize(
        words,
        accept='audio/wav',
        voice=language
    ).get_result()
    print(response.status_code)
    if response.status_code != 200:
        print("TTS Service status:", response.text)
        print("Creating file ---", name)
    with open(name, mode='bx') as f:
        f.write(response.content)
