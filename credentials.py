#!/usr/bin/env python

import base64
import pickle
import json
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
    print('Robot: {}'.format(robot.name))
print('---------------------------------------------------------------------------------------------------------')

myRobot = str(input('Please type the name of the robot you want to configure (None): ') or 'None') 
if myRobot != 'None':
    for robot in account.robots:
       if robot.name == myRobot:
           n = base64.b64encode(robot.name.encode('ascii'))
           snr = base64.b64encode(robot.serial.encode('ascii'))
           sec = base64.b64encode(robot.secret.encode('ascii'))

           credentials = {'n': n, 'snr': snr, 'sec': sec}

           file_system = FileSystemAccess(join('skills', 'NeatoSkill'))

           with file_system.open('credentials.store', 'wb') as f:
               pickle.dump(credentials, f, pickle.HIGHEST_PROTOCOL)

           print('Name: {}'.format(robot.name))
           print('Serial: {}'.format(robot.serial))
           print('Secret: {}'.format(robot.secret))
           print('Created credentials.store for {} in {}'.format(robot.name, file_system.path))
          
           # Dump possible room configuration
           dummy = account.maps
           persMaps = account.persistent_maps
           if robot.serial in persMaps:
                maps = {}
                myRobotsMaps = persMaps[robot.serial]
                for mapData in myRobotsMaps:
                    maps[mapData['name']] = mapData['id']
           
                with file_system.open('rooms.store', 'w') as f:
                    json.dump(maps, f)
                
                print(maps) 
                print('Created rooms.store for {} in {}'.format(robot.name, file_system.path))

           exit() 

print('No credentials saved')
