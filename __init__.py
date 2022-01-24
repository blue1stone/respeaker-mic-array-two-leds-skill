from mycroft import MycroftSkill, intent_file_handler


class RespeakerMicArrayTwoLeds(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('leds.two.array.mic.respeaker.intent')
    def handle_leds_two_array_mic_respeaker(self, message):
        self.speak_dialog('leds.two.array.mic.respeaker')


def create_skill():
    return RespeakerMicArrayTwoLeds()

