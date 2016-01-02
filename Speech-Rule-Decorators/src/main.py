import SpeechRuleDecorator
from time import sleep

rules = SpeechRuleDecorator.SpeechRules()

@rules.onrecognize('test')
def main():
    print('foo')

if __name__ == '__main__':
    stop = rules.listen_in_background()
    try:
        while True:
            sleep(5)
            print('Listening...')
    except KeyboardInterrupt:
        stop()
