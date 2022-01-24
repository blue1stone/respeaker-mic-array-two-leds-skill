from mycroft import MycroftSkill, intent_file_handler
from pixel_ring import pixel_ring
from usb.core import USBError
from math import ceil
from time import sleep

class RespeakerMicArrayTwoLeds(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.shows_volume = False


    def initialize(self):
        self.add_event('mycroft.skills.initialized',
                        self.handler_mycroft_skills_initialized)

        self.add_event('recognizer_loop:wakeword',
                        self.handler_wakeword)
        self.add_event('recognizer_loop:record_begin',
                        self.handler_record_begin)
        self.add_event('recognizer_loop:record_end',
                        self.handler_record_end)

        self.add_event('recognizer_loop:audio_output_start',
                        self.handler_audio_output_start)
        self.add_event('recognizer_loop:audio_output_end',
                        self.handler_audio_output_end)
        
        self.add_event('mycroft.mic.mute',
                        self.handler_mycroft_mic_mute)
        self.add_event('mycroft.mic.unmute',
                        self.handler_mycroft_mic_unmute)

        self.add_event('mycroft.volume.increase',
                        self.handler_mycroft_volume_changed)
        self.add_event('mycroft.volume.decrease',
                        self.handler_mycroft_volume_changed)
        self.add_event('mycroft.volume.get.response',
                        self.handler_mycroft_volume_get_response)



    def handler_mycroft_skills_initialized(self, message):
        # all skills have been loaded, turn off leds
        self.log.info("Setting pixel ring to off.")
        try:
            pixel_ring.off()
        except USBError as e:
            self.usb_error_notify(e)



    def handler_wakeword(self, message):
        # wakeword detected, keep leds on and trace source
        self.log.info("Setting pixel ring to listen.")
        try:
            pixel_ring.listen()
        except USBError as e:
            self.usb_error_notify(e)

    def handler_record_begin(self, message):
        # recording started, keep leds on and trace source
        self.log.info("Setting pixel ring to listen.")
        try:
            pixel_ring.listen()
        except USBError as e:
            self.usb_error_notify(e)

    def handler_record_end(self, message):
        # recording ended, turn off leds
        self.log.info("Setting pixel ring to off.")
        try:
            pixel_ring.off()
        except USBError as e:
            self.usb_error_notify(e)

    
    def handler_audio_output_start(self, message):
        # mycroft speaks, pulse leds
        self.log.info("Setting pixel ring to speak.")
        try:
            if not self.shows_volume:
                pixel_ring.speak()
        except USBError as e:
            self.usb_error_notify(e)

    def handler_audio_output_end(self, message):
        # speaking ended, turn off leds
        self.log.info("Setting pixel ring to off.")
        try:
            if not self.shows_volume:
                pixel_ring.off()
        except USBError as e:
            self.usb_error_notify(e)


    def handler_mycroft_mic_mute(self, message):
        # mic muted, turn red
        self.log.info("Setting pixel ring to color red.")
        try:
            pixel_ring.mono(0xe70e02)
        except USBError as e:
            self.usb_error_notify(e)

    def handler_mycroft_mic_unmute(self, message):
        # mic unmuted, turn off/normal again
        self.log.info("Setting pixel ring to off.")
        try:
            pixel_ring.off()
        except USBError as e:
            self.usb_error_notify(e)


    def handler_mycroft_volume_changed(self, message):
        # request volume
        self.log.info("Volume changed, requesting volume.")
        self.bus.emit(Message('mycroft.volume.get'))
    
    def handler_mycroft_volume_get_response(self, message):
        # show current percentage as leds
        self.log.info("Setting pixel ring to show current volume.")
        self.shows_volume = True
        volume = ceil(message.percent * 12)
        try:
            pixel_ring.show_volume(volume)
            sleep(2)
            if message.muted:
                pixel_ring.mono(0xe70e02)
            else:
                pixel_ring.off()
        except USBError as e:
            self.usb_error_notify(e)
        self.shows_volume = False


    def usb_error_notify(self, e):
        self.log.error("An USB Error occured. Are you sure you are using a Respeaker Mic Array v2.0?")
        self.log.error("If you just reconnected your device, try rebooting the system.")
        self.log.exception(e)



def create_skill():
    return RespeakerMicArrayTwoLeds()
