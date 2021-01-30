# <img src='https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg' card_color='#628279' width='50' height='50' style='vertical-align:bottom'/> Neato
Controls your neato or vorwerk vacuum cleaner

## About
This skill allows you to control your vacuum cleaner robot with your voice. Lay back on your coach and tell your Neato to start cleaning the house or single rooms.
Also room specific NoGo Lines are supported by persistend maps (can be configured in your corresponding vacuum cleaner app)

You have to provide the name of your robot, its serial number and its secret. You can get those information by executing getcredentials.py from the skill directory.
To persist your credentials you can set them online in the skill settings (comfortable) or locally via credentials.py (more secure).

If you want to clean explicit rooms with NoGo Lines, you have to specify them in the optional rooms setting in json format (example is already provided). To get the right map id for your persistent maps there is another helper-script in the skill directory called getmapid.py  

## Examples
* "tell Neato to start cleaning"
* "tell the robot to clean the living room"
* "tell <name of your robot> to clean"

## Credits
Alexander Zeh (@azaz78)

## Category
Daily
**IoT**
Productivity

## Tags
#Vacuum cleaner
#Neato
