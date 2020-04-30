import sys
import os
import logging
import urllib
import Resources.config as config
import json
# import main as m

# load json file
def load_json(file_js):
    with open(file_js, 'r') as file:
        data = file.read().replace('\n', '')
        data = json.loads(data)
        logging.info("File load successfully - " + file_js)
    return data

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


# Shutdown function
def shutdown():
    logging.info("Shutting down...")
    sys.exit(0)


# Restart function
def restart():
    os.system("python main.py")
    logging.info("Restarting...")
    sys.exit(0)


# Weather
def weather():
    state = dict();
    user_settings = load_json(config.FILE_USER)
    try:
        with urllib.request.urlopen(config.HEADURL + '://' + config.IP + '/Api/Api_v2.php?data=weather&key='+config.TOKEN_WEATHER+'&UserID='+str(user_settings['userid'])) as response:
            res = response.read()
            res = res.decode("utf-8")
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                logging.info('Getting weather...')

                weather_json = res_encode['Weather']

                temperature = weather_json['main']['temp'] - 273.15
                temperature = round(temperature, 2)
                pressure = weather_json['main']['pressure']
                humidity = weather_json['main']['humidity']

                state['response'] = "Temperatura: "+str(temperature)+' stopni Celsjusza, ciśnienie: '+str(pressure)+' hektopaskali, wilgotność '+str(humidity)+' procent.'

                logging.info('Weather - '+state['response'])
                state['status'] = True
            else:
                logging.info('Getting weather... ERROR - '+res_encode['Code']+' '+res_encode['Description'])
                state['status'] = False
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))
        state['status'] = False

    return state

# Whether 'czy'
def whether():
    state = dict();
    try:
        with urllib.request.urlopen('https://yesno.wtf/api') as response:
            res = response.read()
            res = res.decode("utf-8")
            res_encode = json.loads(res)
            logging.info('Downloading answers...')

            if res_encode['answer'] == 'no':
                state['response'] = "nie"
            elif res_encode['answer'] == 'yes':
                state['response'] = "nie"
            else:
                state['response'] = "może"

            logging.info('Whether - ' + state['response'])
            state['status'] = True
    except urllib.error.URLError as e:
        logging.warning(short(e.reason, 'error'))
        state['status'] = False

    return state

