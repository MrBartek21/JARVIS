# -*- coding: utf-8 -*-
import urllib.request
import logging
import json
import pyttsx3
import speech_recognition as sr
import Resources.config as config
import Resources.function as function
import platform
import os


# Check connection
def check_connection():
    try:
        with urllib.request.urlopen(config.HEADURL+'://'+config.IP+'/Api/Api_v2.php?data=status&key='+config.TOKEN_STATUS) as response:
            res = response.read()
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                status = True
                logging.info('Server connection valid')
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))
        status = False

    return status


# Check update
def check_update(user_id, file, version):
    try:
        with urllib.request.urlopen(config.HEADURL+'://'+config.IP +'/Api/Api_v2.php?data=update&key='+config.TOKEN_UPDATE+'&UserID='+str(user_id)+'&File='+file+'&Version='+str(version)) as response:
            res = response.read()
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:

                # Validation Status Code
                if res_encode['Status'] == "Update":
                    update_content = res_encode['Update']
                    new_version = update_content['version']
                    os.remove(file)
                    file = open(file, 'w')
                    file.write(update_content)
                    file.close()

                    logging.info("Updating - "+file+' from version '+version+' to '+new_version)
                    status = True
                else:
                    logging.info("No updates available - "+file)
                    status = False
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))
        status = False

    return status


# Get system info
def system_info(userid):
    sys_info = {'machine': platform.machine(), 'version': platform.version(), 'system': platform.system()}

    try:
        with urllib.request.urlopen(config.HEADURL+'://'+config.IP+'/Api/Api_v2.php?data=status&key='+config.TOKEN_STATUS+'&add=Yes&UserID='+str(userid)+'&Code='+str(config.CODE)+'&machine='+sys_info['machine']+'&version='+sys_info['version']+'&system='+sys_info['system']) as response:
            res = response.read()
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                logging.info('Debug data sent')
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))


# Add word to database to machine learning
def add_word(text, actionid, action):
    text_short = short(text, 'all')
    try:
        with urllib.request.urlopen(config.HEADURL+'://'+config.IP+'/Api/Api_v2.php?data=waadd&key='+config.TOKEN_ADD_WORD+'&Word='+text_short+'&ACNU='+str(actionid)+'&Action='+action) as response:
            res = response.read()
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                logging.info('Word added to database successfully - '+text)

            status = True
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))
        status = False

    return status


# Led information function
def led(color, anim):
    print(color)


# ====================================[FILE FUNCTION]====================================
# Check file
def check_json(file_js):
    try:
        with open(file_js) as f:
            logging.info("The file exists and is valid - " + file_js)

            state = True
    except IOError:
        logging.info("File not accessible - " + file_js)

        state = False
    return state


# load json file
def load_json(file_js):
    with open(file_js, 'r') as file:
        data = file.read().replace('\n', '')
        data = json.loads(data)
        logging.info("File load successfully - " + file_js)
    return data

# =======================================================================================


# ====================================[OTHER FUNCTION]===================================
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

# =======================================================================================


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
        "state": None,
        "transcription": None
    }

    '''
    state = ok jezeli przetłumaczono słowa
    state = api jezeli nie mozna poczłaczy wymagany restart 
    state = unable recognize jezeli nie mozna rozpoznac, czekanie na kolejna kolejke
    '''

    try:
        response["transcription"] = recognizer.recognize_google(audio, language=user_settings['lang'])
        response["state"] = "OK"
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["state"] = "API"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["state"] = "Unable_Recognize"
    return response


def active_agent():
    tts_engine.say(user_settings['response'])
    tts_engine.runAndWait()

    # Wait for a user speech
    user_word = recognize_speech_from_mic(recognizer, microphone)
    print(user_word)

    # If speech is recognize corectly
    if user_word['state'] == "OK":
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
                logging.info("ACTION " + str(action_id) + " - " + word_find['action'])
                tts_engine.say(word_find['response'])
                tts_engine.runAndWait()
            elif action_id == 1:
                # Response and action
                logging.info("ACTION " + str(action_id) + " - " + word_find['action'])

                tts_engine.say(word_find['response'])
                tts_engine.runAndWait()

                state_aw = add_word(recognize_word, str(action_id), word_find['action'])

                method_to_call = getattr(function, word_find['action'])
                result = method_to_call()
            elif action_id == 2:
                logging.info("ACTION " + str(action_id) + " - " + word_find['action'])

                method_to_call = getattr(function, word_find['action'])
                result = method_to_call()
                print(result)

                if result['status']:
                    tts_engine.say(word_find['response'] + result['weather'])
                    tts_engine.runAndWait()
        else:
            tts_engine.say(user_settings['no_response'])
            tts_engine.runAndWait()
            state_aw = add_word(recognize_word, -1, 'ERROR')


# Main function
if __name__ == "__main__":
    active = False
    # Microphone and Recognizer init
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # TTS Engine init
    tts_engine = pyttsx3.init()

    # Logging init
    logging.basicConfig(format=config.LOG_FORMAT, filename=config.LOG_FOLDER + '/' + config.LOG_FILE, level=config.LOG_LEVEL)
    logging.info("Starting...")

    # Check all file
    check_json(config.FILE_WORDS)
    check_json(config.FILE_USER)

    # Check connection init
    if check_connection():
        # Active main loop and check all file and update
        led("green", "all")

        # Loads all file
        words = load_json(config.FILE_WORDS)
        version_words = words['version']
        user_settings = load_json(config.FILE_USER)
        user_id = user_settings['userid']
        version_user_settings = user_settings['version']

        if user_id != 0:
            # Check update and send system info
            system_info(user_id)
            check_update(user_id, config.FILE_WORDS, version_words)

            if check_update(user_id, config.FILE_USER, version_user_settings):
                # Load all file
                words = load_json(config.FILE_WORDS)
                user_settings = load_json(config.FILE_USER)
                active = True
            else:
                # Load others file
                active = True

        else:
            # wymagaj połączenia z kontem
            active = False
            led("yellow", "all")

    else:
        # Stop main loop
        active = False
        # Ledy czerwone powiedz że nie ma połączenia
        led("red", "all")

    led("black", "all")
    # Main loop
    while active:
        # Wait for a user speech
        user_word = recognize_speech_from_mic(recognizer, microphone)

        # If speech is recognize correctly
        if user_word['state'] == "OK":
            recognize_word = user_word['transcription'].lower()
            logging.info("Command registered - " + recognize_word)
            state_aw = add_word(recognize_word, 0, "")

            # If user activate a bot
            if recognize_word == user_settings['activator']:
                active_agent()
        elif user_word['state'] == "API":
            # Unable to connect to server recognize
            logging.info("Unable to connect to server, restart wymagany")
            tts_engine.say(user_settings['no_connection'])
            tts_engine.runAndWait()
