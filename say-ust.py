#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Ustream 用 ハッシュタグ（メンション）読み上げスクリプト
# 
# Author:   Logi
# URL:      http://logi.hateblo.jp/
# require:  SayKotoeri, Saykana or SayKotoeri2
# OS:       for Mac Only
# Link:     [PythonでTwitterのタイムラインをストリーミングで読み上げさせるfor Mac[tweepy] « haya14busa](http://haya14busa.com/tweepy-read-aloud-tl/)
# Link:     [tweepyでstreamingを使う - 備忘録](http://monowasure78.hatenablog.com/entry/2013/11/26/tweepy%E3%81%A7streaming%E3%82%92%E4%BD%BF%E3%81%86)
# Link:     [tweepyでリアルタイムハッシュタグ検索 — 螺旋階段を一歩ずつ](http://hironow.bitbucket.org/blog/html/2014/01/18/tweepy_hashtag_search.html)

import tweepy
from subprocess import call
import re
#import unicodedata
import sys, codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

def Setup():
    global mode, name, exception, replace_str
    
    # 0（ハッシュタグ）、1（メンション）
    mode = 0
    # ハッシュタグもしくはメンションの文字列を指定
    name = 'xxxxx'
    # 自分自身のツイートを除外する場合、idを指定
    # （除外しない場合は空白に）
    exception = 'xxxxx'
    
    replace_str = [
    # 置換する文字列をカンマ区切りで指定
    # パターンには正規表現を使用できます
    u'(The |THE ),ザ ',
    u'[Tt]witter,ツイッター',
    u'[Uu]stream,ユーストリーム',
    u'[Uu]st,ユースト',
    u'[Pp]ixiv,ピクシブ',
    u'[Ii]nstagram,インスタグラム',
    u'[Aa]ppear,アピアー',
    u'[Aa]ppear.in,アピアー・イン',
    u'[Aa]dobe,アドビ',
    u'[Mm]acintosh,マッキントッシュ',
    u'[Mm]ac,マック',
    u'[Ww]indows,ウィンドーズ',
    u'(LINUX|Linux),リナックス',
    u'[Uu]buntu,ウブントゥ',
    u'[Ww]ord[Pp]ress,ワードプレス',
    u'[Pp]ython,パイソン',
    u'(VOCALOID|Vocaloid),ボーカロイド',
    u'[Bb]ot,ボット',
    u'℃,度',
    u'(orz|OTL),がっくり',
    u'読み上げ,よみあげ',
    u'[○●]+,まる',
    u'◎+,にじゅうまる',
    u'[□■]+,しかく',
    u'[△▲▽▼]+,さんかく',
    u'秋色,あきいろ',
    ]
    
    return Setup

def get_oauth():
    CONSUMER_KEY='Bo1d6GMo44oKQl62sHoJ1G7GM'
    CONSUMER_SECRET='pRFkPFm8PD0nhKjPGbZXauFv0QRYr8zV0TavaHoH6jbwOWMVFm'
    ACCESS_TOKEN_KEY='4239291-kHnmLLT1feTHRhPDbvDga5Ml0dnGH8a9VQSEo5YvKq'
    ACCESS_TOKEN_SECRET='HF7M9PcnmTKCv55gPC89sun2NU24Pte1V2ARtsrIqH85V'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    return auth

def str_replace(string):
    string = re.sub('&.+;', ' ', string)
    # Ustが追加する文字列を削除
    string = re.sub('\(\s?[#@]' + name + '[^\)]+\)', '', string)
    # remove URL
    string = re.sub('(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', 'URL', string)
    # remove quote
    string = re.sub('"', ' ', string)
    string = re.sub("'", ' ', string)
    string = re.sub('\/', ' ', string)
    
    string = re.sub('RT', 'Retweet', string)
    # ハッシュタグを削除
    string = re.sub('#[^#\s$]{1,}', '', string)  
    # メンション、リプライを削除
    string = re.sub('@[0-9a-zA-Z_]{1,15}', '', string)

    for buff in replace_str:
        list_value = buff.split(',')
        string = re.sub(list_value[0], list_value[1], string)

    # w（ワラ）、8（パチパチ）、TUEEE（つえー）
    if not (isinstance(string, unicode)):
        string = unicode(string, 'utf-8')
    string= string.replace('\u003d','=')
    #string = unicodedata.normalize('NFKC', string)
    match = re.search(u'([^A-Za-zＡ-Ｚａ-ｚ\s])[wW]\s', string, re.U)
    if match != None:
        buff = match.group(1)
        string = re.sub(u'[^A-Za-zＡ-Ｚａ-ｚ\s][wW]\s', buff + u'ワラ ', string)
    string = re.sub(u'[wWｗＷ]{2,}', u'ワラワラワラ', string)
    string = re.sub('[8８]{3,}', u'ぱちぱちぱち', string)
    string = re.sub('[TＴ][SＳ]?[UＵ][EＥ]{3,}', u'つえーーー', string)

    # 日付
    match = re.search(u'([\d]{1,2})[\/／]([\d]{1,2})', string, re.U)
    if match != None:
        string = re.sub(u'([\d]{1,2})[\/／]([\d]{1,2})', match.group(1) + u'月 ' + match.group(2) + '日' , string)

    # バージョン
    match = re.search(u'[VvＶｖ][eｅ][rｒ][\.．]?(\d)', string, re.U)
    if match != None:
        string = re.sub(u'[VvＶｖ][eｅ][rｒ][\.．]?\d', u'バージョン' + match.group(1) , string)
    
    string = re.sub(u'[\#＃]', u'シャープ', string)
    string = re.sub(u'[$＄]', u'ドル', string)
    string = re.sub(u'[%％]', u'パーセント', string)
    string = string.replace('&amp;', u'アンド')
    string = re.sub(u'[&＆]', u'アンド', string)
    string = re.sub(u'[@＠]', u'アット', string)
    match = re.search(u'[VvＶｖ][eｅ][rｒ][\.．]?(\d)', string, re.U)
    if match != None:
        buff = match.group(1)
        string = re.sub(u'[VvＶｖ][eｅ][rｒ][\.．]?\d', u'バージョン' + buff , string)
    
    # SaiKotoeriのエラー対策
    string = string.replace(u'•', u'・')
    string = string.replace('\)', '）')
    string = string.replace('*', u'＊')
    string = re.sub(u'[*⁎⁕]', u'＊', string)
    string = re.sub(u'[⁄⁄\`\´\'｀´\[\]©\|\(\)\{\}\*\․]', '', string)
    string = re.sub(u'[づ|ヅ]', u'ず', string)
    string = re.sub(u'[ぢ|ヂ]', u'じ', string)
    string = re.sub(u'鼻血', u'はなじ', string)
    string = re.sub(u'縮', u'ちじ', string)
    string = string.replace(u'°̥', '')
    string = re.sub('[\-]{2,}', u'——', string)
    #string = string.replace('?', u'？')

    # SayKotoeriでエラーになる文字を削除
    string = re.sub(ur'[^\u0020-\u007E\u0082\u0085\u0091-\u0094\u00A5\u00AB\u00B1\u00BB\u00F7\u2018-\u201F\u203B\u2212-\u2219\u221E\u22EF\u25A0\u25A1\u3000-\u303F\u3040-\u30FF\u4E00-\u9FFF\uFF01-\uFF9F]', u'　', string)

    return string

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if not hasattr(status, 'retweeted_status') or (status.author.screen_name == exception) :
            try:
                print u'---{name}/@{screen}---\n   {text}\nvia {src} {created}'.format(
                        name = status.author.name,
                        screen = status.author.screen_name,
                        text = status.text.replace('&amp;','&'),
                        src = status.source,
                        created = status.created_at)
                read_text = str_replace(status.author.name.encode('utf-8')) + 'さん　' + str_replace(status.text.encode('utf-8'))
            
                call(['SayKotoeri2 -s 110 "{text}" >/dev/null 2>&1'.format(text=read_text)], shell=True)
                # Kyokoさんを使う場合はこちら↓
                #call(['echo "{text}" | say -v Kyoko -r 200 >/dev/null 2>&1'.format(text=read_text)], shell=True)

            except Exception, e:
                print >> sys.stderr, 'Encountered Exception:', e
                pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

def main():
    auth = get_oauth()
    Setup()
    if not mode : str = '#' + name
    else : str = '@' + name
    stream = tweepy.Stream(auth, CustomStreamListener(), secure=True)
    stream.filter(languages=['ja'],track=[str])
    stream.timeout = None

if __name__ == "__main__":
    main()