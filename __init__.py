from mycroft import MycroftSkill, intent_file_handler


class Neato(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('neato.intent')
    def handle_neato(self, message):
        self.speak_dialog('neato')


def create_skill():
    return Neato()

