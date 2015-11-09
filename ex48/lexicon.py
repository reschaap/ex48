#!/usr/bin/env python

def scan(text):
    # Take the argument string and seperate the words into a list. 
    # Determine the TYPE of the words and return the TYPE and word as
    # a tuple in a list.
    words_list = text.lower().split()
    direction_list = ['north', 'south', 'east', 'west', 'down', 'up', 'left',
                      'right', 'back']
    verb_list = ['go', 'kill', 'eat', 'stop', 'shoot', 'attack', 'hide',
                 'fire', 'hit', 'duck', 'sit', 'stand', 'kick', 'punch', 'fight']
    stop_list = ['the', 'in', 'of', 'from', 'at', 'it']
    nouns_list = ['door', 'cabinet', 'gothon', 'doorway',
                  'gun', 'him']
    
    scan = []
    
    for word in words_list:
        if direction_list.count(word) != 0:
            scan.append(('direction', word))
        elif verb_list.count(word) != 0:
            scan.append(('verb', word))
        elif stop_list.count(word) != 0:
            scan.append(('stop', word))
        elif nouns_list.count(word) != 0:
            scan.append(('noun', word))
        elif number_check(word) != None:
            scan.append(('number', number_check2(word)))
        else:
            scan.append(('error', word))
    
    return scan


def number_check(word):
    # 
    try:
        return int(word)
    except ValueError:
        return None
   
    
def number_check2(word):
    
    if word.isdigit():
        return int(word)
    else:
        return None