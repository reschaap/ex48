#!/usr/bin/env python

"""
To start the game create a Map object with a scene name as an argument.
Then create an Engine object with the Map object as an argument. 
Finally call the play() method on the Engine object.

Example:

    a_map = Map('central_corridor')
    a_game = Engine(a_map)
    a_game.play()
"""
from sys import exit
from random import randint

import textoutput
import game_text
import lexicon
import parser

class Scene(object):
    
    def enter(self):
        print "This scene is not yet configured. Subclass it and implement enter()."
        exit(1)


class Engine(object):
    
    def __init__(self, scene_map):
        self.scene_map = scene_map
        
    def play(self):
        current_scene = self.scene_map.opening_scene()
        
        while True:
            print "\n--------"
            
            scene_name = current_scene.enter()
            if scene_name == 'death':
                death_scene = Death()
                death_scene.enter()
                continue
            else:
                next_scene_name = scene_name
                
            current_scene = self.scene_map.next_scene(next_scene_name)


class Death(Scene):
    
    quips = [
        "You died. You kinda suck at this.",
        "Your mom would be proud...if she were smarter.",
        "Such a luser.",
        "I have a small puppy that's better at this."
    ]
    
    def enter(self):
        text_quip = Death.quips[randint(0, len(self.quips)-1)]
        display_text(text_quip)
        
        text =  "Do you still want to go on?"
        display_text
        
        answer = raw_input("y/n? >..")
        if answer == 'y':
            pass
        else:
            exit(1)


class CentralCorridor(Scene):
    
    def enter(self):
        text = game_text.centralcorridor_enter
        display_text(text)
        
        combat = CombatRound('central_corridor')
        if combat.play() == 'player':
            text = game_text.centralcorridor_win
            display_text(text)
            return 'laser_weapon_armory'
        else:
            return 'death'


class LaserWeaponArmory(Scene):
    
    def enter(self):
        text = game_text.laser_weapon_armory_enter
        code = "{0}{1}{2}".format(randint(1,9), randint(1,9), randint(1,9))
        
        guess = get_input(text)
        guesses = 1
        while str(guess.object) != code and guesses < 15:
            guesses += 1
            correct = 0
        
            for i in range(0, len(code)):
                if str(guess.object)[i] == code[i]:
                    correct += 1
                else:
                    continue
                
            text = "BZZZZEDDD! \\n You have got {0} right".format(correct)
            guess = get_input(text)
            
        if str(guess.object) == code:
            text = game_text.laser_weapon_armory_right_code
            display_text(text)
            return 'the_bridge'
        else:
            text = game_text.laser_weapon_armory_wrong_code
            display_text(text)
            return 'death'


class TheBridge(Scene):
    
    def enter(self):
        text = game_text.the_bridge_enter
        display_text(text)
        
        combat = CombatRound('the_bridge')
        if combat.play() == 'player':
            text = game_text.the_bridge_win
            display_text(text)
            return 'escape_pod'
        else:
            return 'death'


class EscapePod(Scene):

    def enter(self):
        text = game_text.escape_pod_enter
        good_pod = randint(1,5)
        
        guess = get_input(text)
        if guess.object == good_pod:
            text =  game_text.escape_pod_right_choice.format(guess)
            display_text(text)
            exit(1)
        elif guess.object != good_pod:
            bad_escape_pods = range(1, 6)
            bad_escape_pods.remove(good_pod)
            bad_escape_pods.remove(guess.object)
            second_choice = []
            second_choice.append(good_pod)
            second_choice.append(guess.object)
            second_choice.append(bad_escape_pods.pop(randint(0,2)))
            second_choice.sort()
            
            text = game_text.escape_pod_choice.format(
                guess.object, bad_escape_pods[0], bad_escape_pods[1], 
                second_choice[0], second_choice[1], second_choice[2]
                )
            
            guess = get_input(text)
            if guess.object == good_pod:
                text =  game_text.escape_pod_right_choice.format(guess)
                display_text(text)
                exit(1)
            elif guess.object != good_pod:
                text = game_text.escape_pod_wrong_choice.format(guess.object)
                display_text(text)
                return 'death'
            else:
                raise ValueError("Guess is: {0}".format(guess.object))
        else:
            raise ValueError("Guess is: {0}".format(guess.object))
        

class Map(object):
    
    scenes = {
        'central_corridor': CentralCorridor(),
        'laser_weapon_armory': LaserWeaponArmory(),
        'the_bridge': TheBridge(),
        'escape_pod': EscapePod(),
        'death': Death()
    }
    
    def __init__(self, start_scene):
        self.start_scene = start_scene
        print "start_scene in __init__", self.start_scene
    
    def next_scene(self, scene_name):
        print "start_scene in next_scene", self.start_scene
        val = Map.scenes.get(scene_name)
        print "next_scene returns", val
        return val
    
    def opening_scene(self):
        return self.next_scene(self.start_scene) 


class Player(object):
    """
    Keeps track of the player status. Used to see which player wins or 
    loses a round.
    """
    def __init__(self, hits):
        self.hits = hits


class CombatRound(object):
    """
    Plays out combat between the player and a Gothon. It is a rock, 
    paper, scisors style of combat.
    
    Ask the player which action the player will take and choose a 
    random action for the Gothon. 
    
    Call Result() with 'choices' as argument to process the actions and 
    show the result of the chosen actions.    
    
    Check to see if the player or the Gothon has no more hits left. If 
    so return the winner who still has hits left as 'end_result' to the 
    Scene().
    """
    def __init__(self, current_scene):
        self.current_scene = current_scene
        self.get_result = Result()
        self.player = Player(5)
        self.gothon = Player(2)
        
    def play(self):
        choices = self.choose()
        result = self.get_result.get_result(choices)
        show_result = self.get_result.show_result(choices, result)
        end_result = self.check_hits(result)
        player_health = str(self.player.hits)
        gothon_health = str(self.gothon.hits)
        
        score = "\\n Player health: {0} Gothon health: {1}".format(player_health, 
                                                               gothon_health)
        display_text(show_result + score)
        
        while end_result == None:
            choices = self.choose()
            result = self.get_result.get_result(choices)
            show_result = self.get_result.show_result(choices, result)
            end_result = self.check_hits(result)
            player_health = str(self.player.hits)
            gothon_health = str(self.gothon.hits)
            
            score = "\\n Player health: {0} Gothon health: {1}".format(
                                                                player_health, 
                                                               gothon_health)
            display_text(show_result + score)
            
        return end_result
    
    def match(self, sentence, choice_list):
        if choice_list.count(sentence) == 1:
            return 1
        else:
            return None
    
    def choose(self):
        if self.current_scene == "central_corridor":
            text = game_text.centralcorridor_combat
        elif self.current_scene == "the_bridge":
            text = game_text.the_bridge_combat
        else:
            text = "no text"
        
        shoot_list = ['shoot', 'fire']
        duck_list = ['hide', 'duck', 'sit', 'stand']
        melee_list = ['attack', 'hit', 'kick', 'punch', 'fight']
        player_choice = None
        
        while not player_choice:
#            player_input = PlayerInput()
#            sentence = player_input.get_input(text)
            sentence = get_input(text)
                        
            if self.match(sentence.verb, shoot_list):
                player_choice = 'shoot'
            elif self.match(sentence.verb, duck_list):
                player_choice = 'duck'
            elif self.match(sentence.verb, melee_list):
                player_choice = 'melee'
            else:
                text = "try again"
                continue
        
        gothon_choices = ['shoot', 'duck', 'melee']
        gothon_choice = gothon_choices[randint(0, 2)]
        return (player_choice, gothon_choice)

    def check_hits(self, result):
        if result == 'player':
            self.gothon.hits -= 1
        elif result == 'gothon':
            self.player.hits -= 1
        else:
            pass
        
        if self.player.hits > 0 and self.gothon.hits > 0:
            return None
        elif self.player.hits < 1:
            return 'gothon'
        elif self.gothon.hits < 1:
            return 'player'
        else:
            ValueError("player hits :",CombatRound.player.hits, 
                       "gothon hits:", CombatRound.gothon.hits)


class Result(object):
    """
    Use 'choices' to determine whether the player or the Gothon or 
    neither gets hit. Update the correct Player.hits when necessary.
    
    Use 'choices' and 'result' to show a description of the result to 
    the player. (The scene specific descriptions are taken from the 
    Scene() objects.)
    """
    def get_result(self, choices):
        player_choice, gothon_choice = choices
        
        if player_choice == gothon_choice:
            result = 'neither'
        elif player_choice == 'shoot':
            if gothon_choice == 'melee':
                result = 'player'
            else:
                result = 'gothon'
        elif player_choice == 'duck':
            if gothon_choice == 'shoot':
                result = 'player'
            else:
                result = 'gothon'
        elif player_choice == 'melee':
            if gothon_choice == 'duck':
                result = 'player'
            else:
                result = 'gothon'
        else:
            raise ValueError("player_choice :", player_choice
                             , "gothon_choice :", gothon_choice)
        
        return result
    
    def show_result(self, choices, result):
        player_choice, gothon_choice = choices
        
        if player_choice == 'shoot':
            player_action = "You shoot at the Gothon"
        elif player_choice == 'duck':
            player_action = "You hide in the doorway"
        elif player_choice == 'melee':
            player_action = """You run up to the Gothon to take him on with 
                            your fists"""
        else:
            raise ValueError("choices :", choices)
        
        if gothon_choice == 'shoot':
            gothon_action = " and the Gothon takes a shot at you."
        elif gothon_choice == 'duck':
            gothon_action = " and the Gothon hides in a doorway."
        elif gothon_choice == 'melee':
            gothon_action = " and the Gothon runs up to you waving his fists."
        else:
            raise ValueError("choices :", choices)
        
        if result == 'player':
            if player_choice == 'shoot':
                result_descr = game_text.combat_result_player_shoot
            elif player_choice == 'duck':
                result_descr = game_text.combat_result_player_duck
            elif player_choice == 'melee':
                result_descr = game_text.combat_result_player_melee
            else:
                raise ValueError("player_choice :", player_choice)
            
        elif result == 'gothon':
            if gothon_choice == 'shoot':
                result_descr = game_text.combat_result_gothon_shoot
            elif gothon_choice == 'duck':
                result_descr = game_text.combat_result_gothon_duck
            elif gothon_choice == 'melee':
                result_descr = game_text.combat_result_gothon_melee
            else:
                raise ValueError("gothon_choice :", gothon_choice)
        
        elif result == 'neither':
            if player_choice == 'shoot':
                result_descr = game_text.combat_result_neither_shoot
            elif player_choice == 'duck':
                result_descr = game_text.combat_result_neither_duck
            elif player_choice == 'melee':
                result_descr = game_text.combat_result_neither_melee
        
        else:
            raise ValueError("result :", result)
        
        show_result = player_action + gothon_action + " \\n" + result_descr
        return show_result


def display_text(text):
    text_output = textoutput.TextOutput(text, 60, 40)
    text_output.display_text()
    

def get_input(text):
    display_text(text)
    
    choice = raw_input(">.. ")
    if choice == "end":
        exit(0)
    else:
       scan = lexicon.scan(choice)
       sentence = parser.parse_sentence(scan)  
    
    while not sentence:
        text = """
        You make no sense. \\n
        You can enter a sentence like 'Shoot the Gothon' or 
        'Hide in the doorway' \\n
        Try again
        """
        display_text(text)
        
        choice = raw_input(">..")
        if choice == "end":
            exit(0)
        else:
            scan = lexicon.scan(choice)
            sentence = parser.parse_sentence(scan)  
        
    return sentence