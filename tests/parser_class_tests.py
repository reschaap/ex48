from nose.tools import *
from ex48 import parser_class

word_list = [('verb', 'go'), ('direction', 'north')]
sentence = parser_class.Sentence(word_list)
word_list2 = [('stop', 'the'), ('noun', 'bear'), ('stop', 'will'), 
              ('verb', 'eat'), ('stop', 'the'), ('noun', 'honey')]
sentence2 = parser_class.Sentence(word_list2)

def test_atributes():
    assert_equal(sentence.subject, 'player')
    assert_equal(sentence.verb, 'go')
    assert_equal(sentence.object, 'north')
    
    assert_equal(sentence2.subject, 'bear')
    assert_equal(sentence2.verb, 'eat')
    assert_equal(sentence2.object, 'honey')
    
def test_peek():
    assert_equal(sentence.peek([('verb', 'run')]), 'verb')
    assert_equal(sentence.peek([('noun', 'bear'), ('verb', 'eat')]), 'noun')
    assert_equal(sentence.peek(None), None)
    
def test_match():
    assert_equal(sentence.match([('verb', 'go')], 'verb'), ('verb', 'go'))
    assert_equal(sentence.match([('stop', 'the')], 'noun'), None)
    assert_equal(sentence.match(None, 'stop'), None)
    
def test_skip():
    word_list = [('stop', 'will'), ('stop', 'the'), ('noun', 'bear')]
     
    sentence.skip(word_list, 'stop')
    match = sentence.match(word_list, 'noun')
    assert_equal(match, ('noun', 'bear'))
    
def test_parse_verb():
    verb = sentence.parse_verb([('verb', 'run')])
    assert_equal(verb, ('verb', 'run'))
    
    assert_raises(parser_class.ParserError, sentence.parse_verb, 
                  [('noun', 'bear')])

def test_parse_object():
    object_ = sentence.parse_object([('noun', 'princess')])
    assert_equal(object_, ('noun', 'princess'))
    
    object_ = sentence.parse_object([('direction', 'west')])
    assert_equal(object_, ('direction', 'west'))
    
    assert_raises(parser_class.ParserError, sentence.parse_object, 
                  [('verb', 'go')])