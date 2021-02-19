import pickle
import base64
import yaml

from pybotvac import Account, Neato, PasswordSession, Robot

from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import getLogger

__author__ = 'azaz78'

class NeatoSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.robot_name = ""
        self.robot_serial = ""
        self.robot_secret = ""
        self._rooms = None

    def initialize(self, web_update = False):
        # handle credentials
        credentials = self._load_credentials_store()
        if credentials:
            self.robot_name = str((base64.b64decode(credentials['n'])).decode('ascii'))
            self.robot_serial = str((base64.b64decode(credentials['snr'])).decode('ascii'))
            self.robot_secret = str((base64.b64decode(credentials['sec'])).decode('ascii'))
            self._rooms = self._load_rooms_store()
        else:
            login = self.settings.get("login", "")
            passwd = self.settings.get("passwd", "")
            self.robot_name = self.settings.get("name", "")
            self.robot_serial, self.robot_secret, self._rooms = self._get_credentials_and_rooms(self.robot_name, login, passwd)
        
        if self.robot_serial:
            self.log.info ("Loaded credentials for {}".format(self.robot_name))
            rooms = self.settings.get('rooms')
            if rooms is not None:
                self._rooms = yaml.safe_load(rooms)

            if web_update is False: 
                self.register_vocabulary(self.robot_name, "RobotName")
                self.register_intent(IntentBuilder("NeatoStartIntent")\
                                .require("RobotName")\
                                .require("neato.action.start")\
                                .build(), self.handle_neato_start)
                self.register_intent(IntentBuilder("NeatoStopIntent")\
                                .require("RobotName")\
                                .require("neato.action.stop")\
                                .build(), self.handle_neato_stop)
        else:
           self.log.warning("Loading credentials failed")
           self.speak_dialog('neato.error.connect')
        return

    def on_websettings_changed(self):
        # Force a setting refresh after the websettings changed
        # Otherwise new settings will not be regarded
        self.initialize(True)
        return

    @intent_handler(IntentBuilder("NeatoStartDefaultIntent")
                              .require("neato.robot")
                              .require("neato.action.start"))
    def handle_neato_start(self, message):
        self.log.info ("Handle Neato start")
        utterance = message.data.get('utterance')
        self.log.info ("Utterance: {}".format(utterance))

        robot = Robot(self.robot_serial, self.robot_secret, self.robot_name)
        if robot is None:
            self.log.warning ("robot is none")
            self.speak_dialog('neato.error', data={"name": self.robot_name})
            return
        map_id = self._get_map(utterance, self._rooms)
        if map_id is None:
            self.log.info ("Start cleaning")
            robot.start_cleaning()
        else:
            self.log.info ("Start cleaning map {}".format(map_id))
            robot.start_cleaning(category=4, map_id=map_id)

        self.speak_dialog('neato.success', data={"name": self.robot_name})
        return

    @intent_handler(IntentBuilder("NeatoStopDefaultIntent")
                              .require("neato.robot")
                              .require("neato.action.stop"))
    def handle_neato_stop(self, message):
        self.log.info ("Handle Neato stop")
        robot = Robot(self.robot_serial, self.robot_secret, self.robot_name)
        if robot is None:
            self.log.warning ("robot is none")
            self.speak_dialog('neato.error', data={"name": self.robot_name})
            return
        #robot.stop_cleaning()
        robot.send_to_base()
        self.speak_dialog('neato.success.stop', data={"name": self.robot_name})
        return

    def _load_credentials_store(self):
        credentials = None
        credentials_file = 'credentials.store'
        if self.file_system.exists(credentials_file):
            with self.file_system.open(credentials_file, 'rb') as f:
                credentials = pickle.load(f)
        return credentials

    def _load_rooms_store(self):
        rooms = None
        rooms_file = 'rooms.store'
        if self.file_system.exists(rooms_file):
            with self.file_system.open(rooms_file, 'r') as f:
                rooms = yaml.safe_load(f)
        return rooms

    def _get_credentials_and_rooms(self, name, login, passwd):
        password_session = PasswordSession(email=login, password=passwd, vendor=Neato())
        account = Account(password_session)
        for robot in account.robots:
            if robot.name == name:
                maps = {}
                # This dummy thing is necessary, otherwise no persistent maps are available
                dummy = account.maps
                persMaps = account.persistent_maps
                if robot.serial in persMaps:
                    myRobotsMaps = persMaps[robot.serial]
                    for mapData in myRobotsMaps:
                         maps[mapData['name']] = mapData['id']
                return robot.serial, robot.secret, maps 
        return None, None, None

    def _register_voc(self, entities, nameset):
        if entities is None:
            return False
        for keys, value in entities.items():
            for key in keys.split("|"):
                if key != "Default":
                    self.register_vocabulary(key, nameset)
        return True

    def _get_map(self, text, rooms):
        default = None
        for keys, target in rooms.items():
            for key in keys.split("|"):
                if key in text:
                    self.log.debug ("Found {} in {}".format(key, text))
                    return target
                if key == 'default':
                    default = target
        if default is not None:
            self.log.debug ("Found no key but default")
            return default
        return None

def create_skill():
    return NeatoSkill()

