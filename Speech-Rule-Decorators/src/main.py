import SpeechRuleDecorator
from time import sleep

rules = SpeechRuleDecorator.SpeechRules()
rules.debug = True

@rules.onrecognize('I like {animal}')
def main(kwargs):
    print('foo', kwargs)

if __name__ == '__main__':
    stop = rules.listen_in_background()
    try:
        while True:
            sleep(5)
            print('Listening...')
    except KeyboardInterrupt:
        stop()
