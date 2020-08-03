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
import time

#Import led
# import board
# import neopixel

# pixel_pin = board.D18
# num_pixels = 8
# ORDER = neopixel.RGB
# pixels = neopixel.NeoPixel(
 #    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
# )

# Check connection
def check_connection():
    try:
        with urllib.request.urlopen(config.HEADURL+'://'+config.IP+'/Api/Api_v2.php?data=status&key='+config.TOKEN_STATUS) as response:
            res = response.read()
            res = res.decode("utf-8")
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                status = True
                logging.info('Server connection valid')
            else:
                status = True
                logging.info('Server connection not valid - '+res_encode['Code']+' '+res_encode['Description'])
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))
        status = False

    return status


# Check update
def check_update(user_id, file, version):
    version = str(version)
    user_id = str(user_id)

    try:
        with urllib.request.urlopen(config.HEADURL+'://'+config.IP +'/Api/Api_v2.php?data=update&key='+config.TOKEN_UPDATE+'&UserID='+user_id+'&File='+file+'&Version='+version) as response:
            res = response.read()
            res = res.decode("utf-8")
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:

                # Validation Status Code
                if res_encode['Status'] == "Update":
                    # Load all string to var
                    update_content = res_encode['Update']
                    # Convert string to json
                    content = json.loads(update_content)
                    new_version = str(content['version'])
                    os.remove(file)
                    file = open(file, 'w')
                    # Convert json to string
                    file.write(json.dumps(content))
                    file.close()

                    logging.info("Updating - "+str(file)+' from version '+version+' to '+new_version)
                    status = True
                else:
                    logging.info("No updates available - "+file)
                    status = False
            else:
                logging.info('Unable to check for updates - ' + res_encode['Code'] + ' ' + res_encode['Description'])
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
            res = res.decode("utf-8")
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                logging.info('Debug data sent')
            else:
                logging.info('Debug data not sent - '+res_encode['Code']+' '+res_encode['Description'])
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))


# Add word to database to machine learning
def add_word(text, u_id, active_bot):
    text_short = short(text, 'all')
    u_id = str(u_id)
    active_bot = str(active_bot)
    try:
        with urllib.request.urlopen(config.HEADURL+'://'+config.IP+'/Api/Api_v2.php?data=waadd&key='+config.TOKEN_ADD_WORD+'&Word='+text_short+'&UserID='+u_id+'&Active='+active_bot) as response:
            res = response.read()
            res = res.decode("utf-8")
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                logging.info('The word has been successfully sent to the database - '+text)
            else:
                logging.info('The word was not successfully sent to the database - '+text+' - '+res_encode['Code']+' '+res_encode['Description'])
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))


# Led information function
def led(color, anim):
    pass
"""   print(color)
    if color == 'black':
        pixels.fill((0, 0, 0))
    elif color == 'green':
        pixels.fill((0, 255, 0))
    elif color == 'red':
        pixels.fill((255, 0, 0))
    elif color == 'yellow':
        pixels.fill((255, 255, 0))
    elif color == 'blue':
        pixels.fill((0, 0, 255))
    else:
        pixels.fill((255, 255, 255))
    pixels.show()"""


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


# Active status update function
def active_status(u_id, dev_code):
    u_id = str(u_id)
    dev_code = str(dev_code)
    try:
        with urllib.request.urlopen(config.HEADURL+'://'+config.IP+'/Api/Api_v2.php?data=active&key='+config.TOKEN_ACTIVE+'&UserID='+u_id+'&Code='+dev_code) as response:
            res = response.read()
            res = res.decode("utf-8")
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                logging.info('Activity status changed correctly - Code '+str(res_encode['Code']))
            else:
                logging.info('Activity status changed incorrectly - Code '+str(res_encode['Code']))
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))

# =======================================================================================


# recognize speak
def recognize_speech_from_mic(recognizer, microphone, lang):
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
    state = api jezeli nie mozna poczłaczy
    state = unable recognize jezeli nie mozna rozpoznac, czekanie na kolejna kolejke
    '''

    try:
        response["transcription"] = recognizer.recognize_google(audio, language=lang)
        response["state"] = "OK"
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["state"] = "API"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["state"] = "Unable_Recognize"
    print(response)
    return response


def active_agent(settings):
    global word_find
    tts_engine.say(config.RESPONSE)
    tts_engine.runAndWait()
    active_status(settings['userid'], config.CODE)
    led('blue', 'ring')

    # Wait for a user speech
    user_word_agent = recognize_speech_from_mic(recognizer, microphone, settings['lang'])

    # If speech is recognize correctly
    if user_word_agent['state'] == "OK":
        recognize_word_agent = user_word_agent['transcription'].lower()
        logging.info("Command registered on active agent - " + recognize_word_agent)
        add_word(recognize_word_agent, settings['userid'], 1)

        result = recognize_word_agent.find('czy')
        if result == 0:
            recognize_word_agent = "czy"

        find = False
        for i in range(words['count']):
            word = words['word' + str(i + 1)]
            if recognize_word_agent == word['name']:
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

                method_to_call = getattr(function, word_find['action'])
                method_to_call()
            elif action_id == 2:
                # Response action and response action
                logging.info("ACTION " + str(action_id) + " - " + word_find['action'])

                method_to_call = getattr(function, word_find['action'])
                result = method_to_call()
                print(result)

                if result['status']:
                    tts_engine.say(word_find['response'] + result['response'])
                    tts_engine.runAndWait()
                else:
                    # Unable to connect to server recognize
                    led("red", "full")
                    logging.info("Unable to connect to server speech recognize on active agent")
                    tts_engine.say(config.API_ERROR)
                    tts_engine.runAndWait()
        else:
            tts_engine.say(config.NO_RESPONSE)
            tts_engine.runAndWait()
    elif user_word_agent['state'] == "API":
        # Unable to connect to server recognize
        logging.info("Unable to connect to server speech recognize on active agent")
        tts_engine.say(config.API_ERROR)
        tts_engine.runAndWait()
        led("red", "ring")
    led('black', 'ring')


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
        led("green", "ring")

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
        tts_engine.say(config.NO_CONNECTION)
        tts_engine.runAndWait()
        led("red", "all")

    time.sleep(5)
    if active:
        led("black", "ring")
    # Main loop
    while active:
        # Wait for a user speech
        user_word = recognize_speech_from_mic(recognizer, microphone, user_settings['lang'])

        # If speech is recognize correctly
        if user_word['state'] == "OK":
            recognize_word = user_word['transcription'].lower()
            logging.info("Command registered - " + recognize_word)
            add_word(recognize_word, user_settings['userid'], 0)

            # If user activate a bot
            if recognize_word == user_settings['activator']:
                active_agent(user_settings)
        elif user_word['state'] == "API":
            # Unable to connect to server recognize
            logging.info("Unable to connect to server speech recognize")
            led("red", "ring")
