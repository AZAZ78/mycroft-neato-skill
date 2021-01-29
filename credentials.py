#!/usr/bin/env python

import base64
import pickle

try:
    input = raw_input
except NameError:
    pass

n = base64.b64encode(str(input('Name of the robot: ')).encode('ascii'))
snr = base64.b64encode(str(input('Serialnumber of the robot: ')).encode('ascii'))
sec = base64.b64encode(str(input('Your client secret: ')).encode('ascii'))

credentials = {'n': n, 'snr': snr, 'sec': sec}

with open('/opt/mycroft/skills/mycroft-neato-skill.azaz78/credentials.store', 'wb') as f:
    pickle.dump(credentials, f, pickle.HIGHEST_PROTOCOL)
