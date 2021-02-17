#!/usr/bin/env python

import re
import base64
import pickle
from os.path import join
from mycroft.filesystem import FileSystemAccess
from pybotvac import Account, Neato, PasswordSession, Robot

try:
    input = raw_input
except NameError:
    pass

login = str(input('Your neato account login/email: '))
passwd = str(input('Your neato account password: '))

# Authenticate via Email and Password
password_session = PasswordSession(email=login, password=passwd, vendor=Neato())

# Create an account with one of the generated sessions
account = Account(password_session)

print('---------------------------------------------------------------------------------------------------------')
# List all robots associated with account
for robot in account.robots:
    print(robot)
print('---------------------------------------------------------------------------------------------------------')

myRobot = str(input('Please type the name of the robot you want to configure (None): ') or 'None') 
if myRobot != 'None':
    # Unfortunatly the pybotvac library has no easy access for the robots data, so parse it manually from the objects string
    reg = re.compile('Name: (?P<Name>[^, ]*).*Serial: (?P<Serial>[^, ]*).*Secret: (?P<Secret>[^, ]*)')
    for robot in account.robots:
       match = reg.match(str(robot))
       if match.group('Name') == myRobot:
           n = base64.b64encode(str(match.group('Name')).encode('ascii'))
           snr = base64.b64encode(str(match.group('Serial')).encode('ascii'))
           sec = base64.b64encode(str(match.group('Secret')).encode('ascii'))

           credentials = {'n': n, 'snr': snr, 'sec': sec}

           file_system = FileSystemAccess(join('skills', 'NeatoSkill'))

           with file_system.open('credentials.store', 'wb') as f:
               pickle.dump(credentials, f, pickle.HIGHEST_PROTOCOL)

           print('Created credentials.store in {}'.format(file_system.path))
           exit() 

print('No credentials saved')
