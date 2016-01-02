﻿from collections import defaultdict
import speech_recognition as sr

class SpeechRuleDecorator:
    """
    Speech Rule Decorator class
    Accepts an optional audio source input from the speech_recognition module
    """ 
    def __init__(self, audio_source = sr.Microphone()):
        """Initalizer"""
        self._recognizer = sr.Recognizer()
        self._source = audio_source
        self._func_registry = defaultdict(list)

        with self._source as source:
            print('Calibrating audio')
            self._recognizer.adjust_for_ambient_noise(source)


    def _callback(self, recognizer, audio):
        """Internal callback that looks in the function registry to see if the spoken text is a rule"""
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            stt = recognizer.recognize_google(audio)
            try:
                for func in self._func_registry.get(stt):
                    func()

            except KeyError as e:
                print("Rule '{0} not found.'".format(e))

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


    def onrecognize(self, eventname):
        """Decorator for rules. calls the associated functions when the rule is invoked via voice"""
        def eventdecorator(func):
            self._func_registry[eventname].append(func)
            return func
        return eventdecorator


    def listen(self):
        """Returns a callable that stops the listener"""
        stopper = self._recognizer.listen_in_background(self._source, self._callback)
        return stopper