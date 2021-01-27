import pickle
import base64

from pybotvac import Robot

from os import listdir, path  # makedirs, remove,
from os.path import dirname, join  # exists, expanduser, isfile, abspath, isdir

from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import getLogger

__author__ = 'azaz78'

class NeatoSkill(MycroftSkill):
    def __init__(self):
        super().__init__(name="NeatoSkill")
        self.robot_name = ""
        self.robot_serial = ""
        self.robot_secret = ""

    def initialize(self):
        # handle credentials
        credentials = self._load_credentials_store()
        if credentials:
            self.robot_name = str((base64.b64decode(credentials['n'])).decode('ascii'))
            self.robot_serial = str((base64.b64decode(credentials['snr'])).decode('ascii'))
            self.robot_secret = str((base64.b64decode(credentials['sec'])).decode('ascii'))
        else:
            self.robot_name = self.settings.get("name", "")
            self.robot_serial = self.settings.get("serial", "")
            self.robot_secret = self.settings.get("secret", "")
        
        self.log.info ("Loaded credentials for {}".format(self.robot_name))
        
        self.register_vocabulary(self.robot_name, "RobotName")
        self.register_intent(IntentBuilder("NeatoStartIntent")\
                            .require("RobotName")\
                            .require("neato.action.start")\
                            .build(), self.handle_neato_start)
        self.register_intent(IntentBuilder("NeatoStopIntent")\
                            .require("RobotName")\
                            .require("neato.action.stop")\
                            .build(), self.handle_neato_stop)

    def on_websettings_changed(self):
        # Force a setting refresh after the websettings changed
        # Otherwise new settings will not be regarded
        return

    @intent_handler(IntentBuilder("NeatoStartDefaultIntent")
                              .require("neato.robot")
                              .require("neato.action.start"))
    def handle_neato_start(self, message):
        self.log.info ("Handle Neato start")
        robot = Robot(self.robot_serial, self.robot_secret, self.robot_name)
        if robot is None:
            self.log.warning ("robot is none")
            self.speak_dialog('neato.error', data={"name": self.robot_name})
            return
        robot.start_cleaning()
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
        robot.stop_cleaning()
        self.speak_dialog('neato.success.stop', data={"name": self.robot_name})
        return

    def _load_credentials_store(self):
        credentials = {}
        skill_dir = dirname(__file__)
        credentials_file = 'credentials.store'
        if path.exists(skill_dir):
            file_list = listdir(skill_dir)
            if credentials_file in file_list:
                with open(skill_dir + '/' + credentials_file, 'rb') as f:
                    credentials = pickle.load(f)
        return credentials

    def _register_voc(self, entities, nameset):
        if entities is None:
            return False
        for keys, value in entities.items():
            for key in keys.split("|"):
                if key != "Default":
                    self.register_vocabulary(key, nameset)
        return True

def create_skill():
    return NeatoSkill()

