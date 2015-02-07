# -*- coding: utf-8 -*-
import blurb

__author__ = 'mustafacamurcu'
from PyMarkovTextGenerator import Markov
def dehtml(str):
    b = 0
    i = 0
    for c in str:
        if c == '(' :
            b += 1
            str = str[:i] + str[i+1:]
            i -= 1
        elif c == ')':
            b -= 1
            str = str[:i] + str[i+1:]
            i -= 1
        if c == '<' :
            b += 1
            str = str[:i] + str[i+1:]
            i -= 1
        elif c == '>':
            b -= 1
            str = str[:i] + str[i+1:]
            i -= 1
        elif c == '\\':
            b -= 1
            str = str[:i] + str[i+1:]
            i -= 1
        elif b > 0:
            str = str[:i] + str[i+1:]
            i -= 1
        elif c == '—':
            str = str[:i] + '-' + str[i+1:]
        i += 1

    return str


def clean(data):
    """
    :param data: list of (title, author, blurb) tuples
    :return: tuple of Markov chains for (title, author, blurb)
    Strip HTML tags and parse each into Markov chain of appropriate depth
    """
    titles, authors, descriptions = zip(*data)

    t_string = ""
    for str in titles:
        t_string = t_string + str + "\\ "

    a_string = ""
    for str in authors:
        a_string = a_string + "\\ " + str

    d_string = ""
    for str in descriptions:
        d_string = d_string + " " + str

    t_string = dehtml(t_string)
    a_string = dehtml(a_string)
    d_string = dehtml(d_string)
    print "done cleaning"
    return (t_string, a_string, d_string)

def generate_title(m):
    def end(s):
        interpunction = ("\\")
        if s[len(s)-1] in interpunction:
            return True
        else:
            return False

    return m.generate(endf=end)

def generate_description(m):
    def end(s):
        interpunction = (".", "!", "?")
        if s[len(s)-1] in interpunction and len(s.split()) > 50:
            return True
        else:
            return False

    return m.generate(endf=end)

def generate_author(m):
    def end(s):
        interpunction = ('\\')
        if s[len(s)-1] in interpunction:
            return True
        else:
            return False

    return m.generate(endf=end)

def generate_all(strings):
    """
    :param strings: (all_titles, all_authors, all_descr)
    :return: (new_title, new_author, new_descr)
    Generate the random title/author/description using the Markov chains
    """
    m1 = Markov(prob=True, level=1)
    m2 = Markov(prob=True, level=1)
    m3 = Markov(prob=True, level=3)

    m1.parse(strings[0])
    m2.parse(strings[1])
    m3.parse(strings[2])

    t_string = generate_title(m1)
    a_string = generate_author(m2)
    d_string = generate_description(m3)

    return (t_string,a_string,d_string)




def pkgen():
    """
    :return: alphanumeric primary key (String)
    Generate a random 6-digit primary key
    """
    from base64 import b32encode
    from hashlib import sha1
    from random import random
    rude = ('fuck', 'shit', 'damn', 'bitch', 'hell',)
    bad_pk = True
    while bad_pk:
        pk = b32encode(sha1(str(random())).digest()).lower()[:6]
        bad_pk = False
        for rw in rude:
            if pk.find(rw) >= 0: bad_pk = True
    return pk

print '<' == '<'