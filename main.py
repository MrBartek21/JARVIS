# -*- coding: utf-8 -*-
import urllib.request
import logging
import json
import pyttsx3
import speech_recognition as sr
import Resources.config as config
import Resources.function as function


# Check config file before init
def check_json(file_js, choice):
    try:
        with open(file_js) as f:
            print("The file exists and is valid")
            logging.info("The file exists and is valid")
    except IOError:
        print("File not accessible")
        logging.info("File not accessible")
        f = open(file_js, "a")

        if choice == "words":
            data = {
                "count": 3,
                "word1": {
                    "name": "wyłącz się",
                    "response": "Wyłączam się",
                    "actionid": 1,
                    "action": "shutdown"
                },
                "word2": {
                    "name": "restart",
                    "response": "Trwa restart...",
                    "actionid": 1,
                    "action": "restart"
                },
                "word3": {
                    "name": "pogoda",
                    "response": "",
                    "actionid": 2,
                    "action": "weather"
                }
            }

        f.write(json.dumps(data))
        f.close()


# load json file
def load_json(file_js):
    with open(file_js, 'r') as file:
        data = file.read().replace('\n', '')
        data = json.loads(data)
        logging.info("File load successfully")
    return data


# Add word to database to machine learning
def add_word(text, actionid, action):
    text = short(text, 'all')
    try:
        with urllib.request.urlopen(
                config.HEADURL + '://' + config.IP + '/Api/Api_v2.php?data=waadd&key=' + config.TOKEN_ADD_WORD + '&Word=' + text + '&ACNU=' + str(
                    actionid) + '&Action=' + action) as response:
            res = response.read()
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                print(res_encode)
                logging.info('Word added to database successfully')

            status = True
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))
        print(e.reason)
        status = False

    return status


# recognize speak
def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language=config.LANG)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["success"] = False
        response["error"] = "Unable to recognize speech"
    return response


# Change polish char to english
def change(text, char, char_new):
    for ch in char:
        if ch in text:
            text = text.replace(ch, char_new)
    return text


# Function to fast change all polish char
def short(text, choice):
    if choice == 'all':
        text = change(text, ' ', '%20')
    text = change(text, 'ę', 'e')
    text = change(text, 'ó', 'o')
    text = change(text, 'ą', 'a')
    text = change(text, 'ś', 's')
    text = change(text, 'ł', 'l')
    text = change(text, 'ż', 'z')
    text = change(text, 'ź', 'z')
    text = change(text, 'ć', 'c')
    text = change(text, 'ń', 'n')
    return text


def active_agent():
    tts_engine.say(config.RESPONSE)
    tts_engine.runAndWait()

    # Wait for a user speech
    user_word = recognize_speech_from_mic(recognizer, microphone)
    print(user_word)

    # If speech is recognize corectly
    if user_word['success']:
        recognize_word = user_word['transcription'].lower()
        logging.info("Command registered on active bot - " + recognize_word)

        find = False
        for i in range(words['count']):
            word = words['word' + str(i + 1)]
            if recognize_word == word['name']:
                word_find = word
                find = True

        if find:
            action_id = word_find['actionid']
            if action_id == 0:
                # Only response
                tts_engine.say(word_find['response'])
                tts_engine.runAndWait()
            elif action_id == 1:
                # Response and action
                tts_engine.say(word_find['response'])
                tts_engine.runAndWait()

                state_aw = add_word(recognize_word, action_id, word_find['action'])

                method_to_call = getattr(function, word_find['action'])
                result = method_to_call()
            elif action_id == 2:
                method_to_call = getattr(function, word_find['action'])
                result = method_to_call()
                print(result)

                if result['status']:
                    tts_engine.say(word_find['response'] + result['weather'])
                    tts_engine.runAndWait()
        else:
            tts_engine.say("Przepraszam nie zrozumiałem.")
            tts_engine.runAndWait()
            state_aw = add_word(recognize_word, -1, 'ERROR')


# Main loop
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    tts_engine = pyttsx3.init()
    logging.basicConfig(format=config.LOG_FORMAT, filename=config.LOG_FOLDER+'/'+config.LOG_FILE, level=config.LOG_LEVEL)
    logging.info("Starting...")
    check_json(config.FILE_NAME_WORDS, 'words')
    words = load_json(config.FILE_NAME_WORDS)

    while True:
        # Wait for a user speech
        user_word = recognize_speech_from_mic(recognizer, microphone)
        print(user_word)

        # If speech is recognize corectly
        if user_word['success']:
            recognize_word = user_word['transcription'].lower()
            logging.info("Command registered - " + recognize_word)
            state_aw = add_word(recognize_word, 0, "")

            # If user activate a bot
            if recognize_word == config.ACTIVATOR:
                active_agent()
