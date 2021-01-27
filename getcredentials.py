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

# List all robots associated with account
for robot in account.robots:
    print(robot)
