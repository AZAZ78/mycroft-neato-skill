#!/usr/bin/env python
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

#List all maps associated with a robot
print("Maps:")
for map_data in account.maps:
    print(map_data)
#List all maps associated with a robot
print("Persistent Maps:")
for robot_data in account.persistent_maps:
    print(robot_data)
    for map_data in account.persistent_maps[robot_data]:
        print(map_data)
