from SpeechRuleDecorator import SpeechRuleDecorator
from time import sleep

srd = SpeechRuleDecorator()

@srd.onrecognize('test')
def main():
    print('foo')

if __name__ == '__main__':
    stop = srd.listen()
    try:
        while True:
            sleep(5)
            print('Listening...')
    except KeyboardInterrupt:
        stop()
