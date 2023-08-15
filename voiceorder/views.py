import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .helperFunctions import *

language, raw_order, pizza_size, pizza_topping, play_audio =  None, "A Lassi with pizza with Fried-Chicken topping", None, None, None


def root(request):
    global language, raw_order, pizza_size, pizza_topping, play_audio
    language, raw_order, pizza_size, pizza_topping, play_audio =  None, "A Lassi with pizza with Fried-Chicken topping", None, None, None

    # remove the existing files in the folder
    file = ["info.wav", "info_record.wav", "info_repeat.wav", "topping.wav", "topping_record.wav", "topping_repeat.wav"]
    for i in file:
        bash_command = str("find . -path \*/" + i + " -delete")
        os.system(bash_command)
    return render(request, "main.html")

def get_topping(request):
    global play_audio
    play_audio = "topping.wav"
    result = "At Little Lemon Plaza, we offer a mouth-watering selection and draw inspiration from Indian, South Indian, Japaneses, Greek, and French culture. " \
             "See the options in the picture below and indulge in the perfect meal for you!"
    text_to_speech(result, play_audio, language)
    return render(request, "getTopping.html")


def get_topping_redirect(request):
    global pizza_size, pizza_topping, play_audio
    clean_order = clean_text(raw_order)  # clean the stop words from audio files
    pizza_size, pizza_topping = get_keywords(clean_order)

    play_audio = "topping_repeat.wav"
    result = "Just wanted to make sure, did ya order a " + pizza_size[0] + " pizza with: " + " ".join(
        map(str, pizza_topping)) + \
             " on it? If not, no worries, just give the recording again button another press."
    text_to_speech(result, play_audio, language)
    return render(request, "getToppingRedirect.html", {"pizzaSize": pizza_size[0], "pizzaTopping": pizza_topping})


def get_order(request):
    global play_audio
    play_audio = "order.wav"
    result = str(
        "Thanks for using the Little Lemon Plaza to place your order. Just wanted to double check that I got it right, ya want a " +
        pizza_size[0] + " pizza with " + " ".join(
            map(str, pizza_topping))  +
        ", is that correct?")
    text_to_speech(result, play_audio, language)
    return render(request, "getOrder.html",
                  {"orderSize": pizza_size[0], "orderTopping": pizza_topping})



def get_topping_upload_wav(request):
    global raw_order
    if "topping_upload_wav" not in request.FILES:
        return HttpResponse("No audio file found")
    else:
        file = request.FILES["topping_upload_wav"]
        if file.name == "":
            return HttpResponse("No audio file selected")
        else:
            raw_order = speech_to_text(file)
            print(raw_order)
    return render(request, "getToppingRedirect.html")


def get_topping_record_wav(request):
    global raw_order
    if "topping_record_wav" not in request.FILES:
        return HttpResponse("No audio file found")
    else:
        file = request.FILES["topping_record_wav"]
        if file.name == "":
            return HttpResponse("No audio file selected")
        else:
            save_audio(file, "topping_record.wav")
            raw_order = speech_to_text("topping_record.wav")
            print(raw_order)
    return redirect("get_topping_redirect")


def play_local_wav(request):
    response = HttpResponse(content_type="audio/x-wav")
    response['Content-Disposition'] = f'attachment; filename="{play_audio}"'

    for audio_chunk in play_local_wav_file(play_audio):
        response.write(audio_chunk)

    return response
