"""
Speech Rule Decorator Module
Need to add docstring
"""
from collections import defaultdict
from parse import parse

import logging
import speech_recognition as sr


class SpeechRules(object):
    """
    Speech Rule Decorator class
    Accepts an optional audio source input from the speech_recognition module
    """

    def __init__(self, audio_source=sr.Microphone()):
        """Initalizer"""
        self.callback = None
        self.debug = False
        self._func_registry = defaultdict(list)
        self._recognizer = sr.Recognizer()
        self._source = audio_source

        with self._source as source:
            print('Calibrating audio...')
            self._recognizer.adjust_for_ambient_noise(source)


    def onrecognize(self, eventname):
        """Decorator for rules. Calls the associated functions when the rule is invoked via voice"""
        def eventdecorator(func):
            """Event decorator closure thing"""
            self._func_registry[eventname.lower()].append(func)
            return func
        return eventdecorator


    def listen_in_background(self):
        """Returns a callable that stops the listener"""
        if not self.callback:
            self.callback = self._function_lookup

        if self.debug:
            logging.debug('Audio Source: {0}'.format(self._source))
            logging.debug('Callback: {0}'.format(self.callback))
            logging.debug('Function Registry {0}'.format(self._func_registry))

        stopper = self._recognizer.listen_in_background(self._source, self.callback)
        return stopper


    def _function_lookup(self, recognizer, audio):
        """
        Default allback that looks in the function registry
        to see if the spoken text is a rule
        """
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            speech_to_text = recognizer.recognize_google(audio)

        except sr.UnknownValueError:
            logging.debug("Google Speech Recognition could not understand audio")

        except sr.RequestError as error:
            logging.debug("Could not request results from Google Speech Recognition service; {0}".format(error))

        key_registry = []
        try:
            for key in self._func_registry.keys():
                key_registry.append({'key': key, 
                                        'parse_resp': parse(key, speech_to_text.lower())})

            key_registry = [x for x in key_registry if x['parse_resp']]

            for i in key_registry: 
                for func in self._func_registry.get(i['key']):
                    func(i['parse_resp'].named)

        except KeyError as error:
            logging.debug("Rule '{0} not found or matched.'".format(error))

        except UnboundLocalError:
            pass
