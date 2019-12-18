import math
import time
from pygame import mixer

from . import Component


class Sound(Component):

    def __init__(self,path_sound, helper, debug=False):
        name = 'sound'
        super(Sound, self).__init__(name)
        self.debug = debug
        self.helper = helper
        self.path_sound = path_sound

    def handleMessage(self, message):
        result = {}

        try:
            if self.debug:
                print(self.name + ' received ' + str(message))

            if "play" in message:
                _result = self.playSound(message["play"])
                result[self.name] = _result
            if "get" in message:
                what = message['get']
                if "all" == what:
                    _files = str(self.files_sound())
                    result[self.name] = str(_files)
        except Exception as e:
            result[self.name] =  'failed with ' + str(e)

        return result

    # -------------------------------------------------------
    def files_sound(self):
        return self.helper.files_in_path(self.path_sound)

    def playSound(self, file_sound):
        result = {}
        files = self.files_sound()
        if self.debug:
            print('sound files\n' + str(files))
        if file_sound in files:
            mixer.init()
            sound = mixer.Sound(self.path_sound + "/" + file_sound)
            slen = math.ceil(sound.get_length())
            if self.debug:
                print('play for {0} seconds'.format(str(slen)))
            sound.play()
            time.sleep(slen)
            result[self.name] = 'played'
        else:
            result[self.name] = file_sound + ' not found'
        return result
