import os
import random
import re
import yaml

import pydub
import pydub.playback

print_template = '-'*10

def position(position_str):
    '''
    converts the string format 'mm:ss.f' to seconds
    '''
    m, s = position_str.split(':')
    return int(m)*60 + float(s)

def review(l, n=100, form='en2jp'):
    '''
    randomly pulls a card from a sample of `n` cards for reviews
    '''
    correct = True
    while True:
        if correct:
            d = random.choice(l[:n])
            if form == 'en2jp':
                question = d[1]
            elif form == 'jp2en':
                question = d[0]

        print(question)
        kb = input('> ')

        if form == 'en2jp':
            if kb and kb == d[0].replace('。', '').replace(' ', ''):
                print('Correct!')
                print(print_template)
                play(d)
                correct = True
            else:
                print('Try again')
                print(print_template)
                correct = False
        elif form == 'jp2en':
            if kb and kb.lower() in d[1].lower():
                print('Correct!')
                print(print_template)
                correct = True
            else:
                print('Try again.')
                print(print_template)
                correct = False

def play(d):
    '''
    plays an audio file of a card `d`
    '''
    fn = d[2]
    start = position(d[3])
    stop = position(d[4])

    if os.path.isfile(fn):
        sound = pydub.AudioSegment.from_mp3(fn)
        splice = sound[start*1000:stop*1000]
        pydub.playback.play(splice)
    else:
        print('audio file not found')

def search(l, key):
    '''
    prints a card and plays the sound
    '''
    for d in l:
        if key in d[0] or key in d[1]:
            print(d)
            play(d)

def read(y, pages='all'):
    with open(y, encoding='utf-8') as f:
        raw = yaml.load(f, Loader=yaml.FullLoader)
    if pages == 'all':
        pages = raw.keys()
    l = []
    for page, defns in raw.items():
        if page in pages:
            mp3 = raw[page]['mp3']
            for jp, defn in defns.items():
                if jp == 'mp3':
                    continue
                else:
                    l.append([jp, defn[0], mp3, defn[1][0], defn[1][1]])
    return l

l = read('dict.yaml', ['p040', 'p041'])
# review(l)
search(l, 'job')
