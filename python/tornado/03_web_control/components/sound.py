from . import Component
import pygame


class Sound(Component):

    def __init__(self,config, helper, debug=False):
        name = 'sound'
        super(Sound, self).__init__(name)
        self.debug = debug
        self.helper = helper
        self.path_sound = config.path_fpvcar + '/sound'
        pygame.mixer.init(44100, -16, 1, 1024)

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

    def playSound(self, name):
        files = self.files_sound()
        if name in files:
            pygame.mixer.music.load(self.path_sound + "/" + name)
            pygame.mixer.music.play()
            result = 'played'
        else:
            result = name + ' not found'
        return result
