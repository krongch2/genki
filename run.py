import os
import random
import re
import yaml

import pydub
import pydub.playback

print_template = '-'*10

p035 = [
    ['おはよう', 'good morning', 'book_1/K00-G.mp3', '00:03.9', '00:04.8'],
    ['こんにちは', 'good afternoon', 'book_1/K00-G.mp3', '00:12.5', '00:14.5'],
    ['こんばんは', 'good evening', 'book_1/K00-G.mp3', '00:17.0', '00:18.5'],
    ['さようなら', 'goodbye', 'book_1/K00-G.mp3', '00:21.2', '00:23.0'],
    ['おやすみなさい', 'good night', 'book_1/K00-G.mp3', '00:25.5', '00:27.0'],
    ['ありがとう', 'Thank you', 'book_1/K00-G.mp3', '00:29.5', '00:31.0'],
    ['すみません', "Excuse me; I'm sorry", 'book_1/K00-G.mp3', '00:38.0', '00:39.5'],
    ['いいえ', 'No; Not at all', 'book_1/K00-G.mp3', '00:44.2', '00:45.2'],
    ['いってきます', 'See you (said by a person leaving)', 'book_1/K00-G.mp3', '00:49.5', '00:51.0'],
    ['いってらっしゃい', 'See you (said by a person staying)', 'book_1/K00-G.mp3', '00:54.0', '00:55.5'],
    ['ただいま', "I'm home", 'book_1/K00-G.mp3', '00:58.5', '01:00.0'],
    ['おかえりなさい', 'Welcome home', 'book_1/K00-G.mp3', '01:02.5', '01:04.3'],
    ['いただきます', 'Thank you for the meal (before eating)', 'book_1/K00-G.mp3', '01:06.8', '01:08.3'],
    ['ごちそうさまでした', 'Thank you for the meal (after eating)', 'book_1/K00-G.mp3', '01:11.3', '01:13.1'],
    ['はじめまして', 'How do you do?', 'book_1/K00-G.mp3', '01:16.3', '01:17.1'],
    ['よろしく　おねがいします', 'Nice to meet you', 'book_1/K00-G.mp3', '01:20.4', '01:22.5']
]

p038 = [
    ['いま　なんじですか。', 'What time is it now?', 'book_1/K01-02.mp3', '00:06.0', '00:07.7'],
    ['じゅうにじはんです。', "It's half past twelve.", 'book_1/K01-02.mp3', '00:10.5', '00:11.8'],
    ['ありがとうございます。', 'Thank you.', 'book_1/K01-02.mp3', '00:13.8', '00:15.3']
]

p039 = [
    ['りゅうがくせいですか。', 'Are you an international student?', 'book_1/K01-03.mp3', '00:02.5', '00:03.9'],
    ['アリゾナだいがくのがくせいです。', 'I am a student at the University of Arizona.', 'book_1/K01-03.mp3', '00:06.2', '00:08.8'],
    ['そうですか。', 'I see.', 'book_1/K01-03.mp3', '00:09.1', '00:10.5'],
    ['せんこうは　なんですか。', 'What is your major?', 'book_1/K01-03.mp3', '00:10.5', '00:12.3'],
    ['いま　にねんせいです。', 'I am a sophomore now.', 'book_1/K01-03.mp3', '00:14.6', '00:16.9']
]

p040 = [
    ['あの', 'um', 'book_1/K01-05.mp3', '00:05.4', '00:06.6'],
    ['いま', 'now', 'book_1/K01-05.mp3', '00:09.5', '00:10.3'],
    ['えいご', 'English (language)', 'book_1/K01-05.mp3', '00:12.7', '00:13.7'],
    # ['ええ', 'yes', 'book_1/K01-05.mp3', '00:16.3', '00:17.1'],
    ['がくせい', 'student', 'book_1/K01-05.mp3', '00:19.6', '00:20.8'],
    ['にほんご', 'Japanese (language)', 'book_1/K01-05.mp3', '00:26.8', '00:27.8'],
    ['こうこう', 'high school', 'book_1/K01-05.mp3', '00:31.0', '00:32.2'],
    ['ごご', 'P.M.', 'book_1/K01-05.mp3', '00:34.5', '00:35.7'],
    ['ごぜん', 'A.M.', 'book_1/K01-05.mp3', '00:38.1', '00:38.8'],
    # ['。。。さい', '... years old', 'book_1/K01-05.mp3', '00:41.2', '00:42.2'],
    ['いちじ', "one o'clock", 'book_1/K01-05.mp3', '00:52.1', '00:53.1'],
    ['にほんじん', 'Japanese people', 'book_1/K01-05.mp3', '00:59.1', '01:00.2'],
    ['せんこう', 'major', 'book_1/K01-05.mp3', '01:02.8', '01:04.1'],
    ['せんせい', 'teacher', 'book_1/K01-05.mp3', '01:06.2', '01:07.6'],
    ['そうです', "that's right", 'book_1/K01-05.mp3', '01:11.7', '01:12.7'],
    ['だいがく', 'university', 'book_1/K01-05.mp3', '01:15.0', '01:16.5'],
    ['でんわ', 'telephone', 'book_1/K01-05.mp3', '01:20.6', '01:21.9'],
    ['ともだち', 'friend', 'book_1/K01-05.mp3', '01:24.5', '01:25.8'],
    ['なまえ', 'name', 'book_1/K01-05.mp3', '01:28.2', '01:29.5'],
    ['なに', 'what', 'book_1/K01-05.mp3', '01:33.6', '01:34.6'],
    ['にほん', 'Japan', 'book_1/K01-05.mp3', '01:37.6', '01:38.4'],
    ['いちねんせい', 'first-year student', 'book_1/K01-05.mp3', '01:44.8', '01:46.2'],
    # ['はい', 'yes', 'book_1/K01-05.mp3', '01:49.5', '01:50.2'],
    ['はん', 'half', 'book_1/K01-05.mp3', '01:53.0', '01:53.8'],
    ['にじはん', 'half past two', 'book_1/K01-05.mp3', '01:56.2', '01:57.5'],
    ['ばんごう', 'number', 'book_1/K01-05.mp3', '02:01.0', '02:02.5'],
    ['りゅうがくせい', 'international student', 'book_1/K01-05.mp3', '02:04.9', '02:06.4'],
    ['わたし', 'I', 'book_1/K01-05.mp3', '02:10.3', '02:11.2']
]

p041 = [
    ['アメリカ', 'America', 'book_1/K01-06.mp3', '00:04.1', '00:05.4'],
    ['イギリス', 'English', 'book_1/K01-06.mp3', '00:08.4', '00:09.4']
]


    #
    # 'かんこく': 'Korea',
    # 'ちゅうごく': 'China',
    # 'かがく': 'science',
    # 'けいざい': 'economics',
    # 'コンピューター': 'computer',
    # 'せいじ': 'politics',
    # 'ビジネス': 'business',
    # 'ぶんがく': 'literature',
    # 'れきし': 'history',
    # 'しごと': 'job',
    # 'いしゃ': 'doctor',
    # 'かいしゃいん': 'office worker',
    # 'こうこうせい': 'high school student',
    # 'しゅふ': 'housewife',
    # 'だいがくいんせい': 'graduate student',
    # 'だいがくせい': 'college student',
    # 'べんごし': 'lawyer',
    # 'おかあさん': 'mother',
    # 'おとうさん': 'father',
    # 'おねえさん': 'older sister',
    # 'おにいさん': 'older brother',
    # 'いもうと': 'younger sister',
    # 'おとうと': 'younger brother',

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

def search(key):
    '''
    prints a card and plays the sound
    '''
    for d in l:
        if key in d[0] or key in d[1]:
            print(d)
            play(d)

l = p035 + p038 + p039 + p040
l = p041
# review(l)
# search('number')
def read(y):
    with open(y, encoding='utf-8') as f:
        raw = yaml.load(f, Loader=yaml.FullLoader)
    print(raw)

read('dict.yaml')
