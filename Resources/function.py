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
    try:
        with urllib.request.urlopen(config.HEADURL + '://' + config.IP + '/Api/Api_v2.php?data=weather&key='+config.TOKEN_WEATHER) as response:
            res = response.read()
            res_decode = json.loads(res)
            if res_decode['Code'] == 0:
                # print(res_encode)
                logging.info('Getting weather...')

                weather_json = res_decode['Weather']
                print(weather_json['main'])

                temperature = weather_json['main']['temp'] - 273.15
                temperature = round(temperature, 2)
                pressure = weather_json['main']['pressure']

                state['weather'] = "Temperatura: " + str(temperature) + ' stopni Celsjusza, ciśnienie: ' + str(pressure) + ' hektopaskali'

                logging.info(state['weather'])
            state['status'] = True
    except urllib.error.URLError as e:
        logging.warning(m.short(e.reason, 'error'))
        print(e.reason)
        state['status'] = False

    return state
