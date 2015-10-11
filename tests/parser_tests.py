from nose.tools import *
from ex48 import parser

def test_peek():
    assert_equal(parser.peek([('verb', 'run')]), 'verb')
    assert_equal(parser.peek([('noun', 'bear'), ('verb', 'eat')]), 'noun')
    assert_equal(parser.peek(None), None)
    
    
def test_match():
    assert_equal(parser.match([('verb', 'go')], 'verb'), ('verb', 'go'))
    assert_equal(parser.match([('stop', 'the')], 'noun'), None)
    assert_equal(parser.match(None, 'stop'), None)
    
    
def test_skip():
     word_list = [('stop', 'will'), ('stop', 'the'), ('noun', 'bear')]
     
     parser.skip(word_list, 'stop')
     match = parser.match(word_list, 'noun')
     assert_equal(match, ('noun', 'bear'))
     
     
def test_parse_verb():
    verb = parser.parse_verb([('verb', 'run')])
    assert_equal(verb, ('verb', 'run'))
    
    assert_raises(parser.ParserError, parser.parse_verb, [('noun', 'bear')])
    
    
def test_parse_object():
    object_ = parser.parse_object([('noun', 'princess')])
    assert_equal(object_, ('noun', 'princess'))
    
    object_ = parser.parse_object([('direction', 'west')])
    assert_equal(object_, ('direction', 'west'))
    
    object_ = parser.parse_object([('number', 1234)])
    
    assert_raises(parser.ParserError, parser.parse_object, [('verb', 'go')])
    
    
def test_parse_subject():
    subject = parser.parse_subject([('noun', 'bear')])
    assert_equal(subject, ('noun', 'bear'))
    
    subject = parser.parse_subject([('verb', 'run')])
    assert_equal(subject, ('noun', 'player'))
    
    
def test_parse_sentence():
    word_list = [('noun', 'princess'), ('verb', 'eat'), ('stop', 'the'), 
                ('noun', 'pea')]
    word_list2 = [('verb', 'go'), ('direction', 'south')]
    
    sentence = parser.parse_sentence(word_list)
    assert_equal(sentence.subject, 'princess')
    assert_equal(sentence.verb, 'eat')
    assert_equal(sentence.object, 'pea')
    
    sentence = parser.parse_sentence(word_list2)
    assert_equal(sentence.subject, 'player')
    assert_equal(sentence.verb, 'go')
    assert_equal(sentence.object, 'south')