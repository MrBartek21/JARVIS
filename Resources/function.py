import sys
import os
import logging
import urllib
import Resources.config as config
import json
import main as m


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
    user_settings = m.load_json(config.FILE_USER)
    try:
        with urllib.request.urlopen(config.HEADURL + '://' + config.IP + '/Api/Api_v2.php?data=weather&key='+config.TOKEN_WEATHER+'&UserID='+str(user_settings['userid'])) as response:
            res = response.read()
            res_encode = json.loads(res)
            if res_encode['Code'] == 0:
                logging.info('Getting weather...')

                weather_json = res_encode['Weather']

                temperature = weather_json['main']['temp'] - 273.15
                temperature = round(temperature, 2)
                pressure = weather_json['main']['pressure']
                humidity = weather_json['main']['humidity']

                state['weather'] = "Temperatura: "+str(temperature)+' stopni Celsjusza, ciśnienie: '+str(pressure)+' hektopaskali, wilgotność '+str(humidity)+' procent.'

                logging.info('Weather - '+state['weather'])
                state['status'] = True
            else:
                state['status'] = False
    except urllib.error.URLError as e:
        logging.warning(m.short(e.reason, 'error'))
        state['status'] = False

    return state

