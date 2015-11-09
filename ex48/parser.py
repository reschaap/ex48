class ParserError(Exception):
    pass


class Sentencte(object):
    
    def __init__(self, subject, verb, obj):
        # remember we take ('noun', 'princess') tuples and convert them
        self.subject = subject[1]
        self.verb = verb [1]
        self.object = obj[1]
        
        
def peek(word_list):
    if word_list:
        word = word_list[0]
        return word[0]
    else:
        return None
    
    
def match(word_list, expecting):
    if word_list:
        word = word_list.pop(0)
        
        if word[0] == expecting:
            return word
        else:
            return None
    else:
        return None
    
    
def skip(word_list, word_type):
    while peek(word_list) == word_type:
        match(word_list, word_type)
        
        
def parse_verb(word_list):
    skip(word_list, 'stop')
    
    if peek(word_list) == 'verb':
        return match(word_list, 'verb')
    else:
        raise ParserError("Expected a verb next.", word_list)
    
    
def parse_object(word_list):
    skip(word_list, 'stop')
    next_word = peek(word_list)
    
    if next_word == 'noun':
        return match(word_list, 'noun')
    elif next_word == 'direction':
        return match(word_list, 'direction')
    elif next_word == 'number':
        return match(word_list, 'number')
    else:
        raise ParserError("Expected a noun, direction or number next. ", 
                          word_list)
    
    
def parse_subject(word_list):
    skip(word_list, 'stop')
    next_word = peek(word_list)
    
    if next_word == 'noun':
        return match(word_list, 'noun')
    elif next_word == 'verb':
        return ('noun', 'player')
    else:
        raise ParserError("Expected a verb next.", word_list)
    
    
def parse_sentence(word_list):
    try:
        subj = parse_subject(word_list)
    except ParserError:
        return None
        
    try:
        verb = parse_verb(word_list)
    except ParserError:
        return None
    
    try:
        obj = parse_object(word_list)
    except ParserError:
        return None
    
    return Sentencte(subj, verb, obj)

def display_help(text):
    pass