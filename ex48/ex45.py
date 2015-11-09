"""
Use this module to display text within a border.

'text' has to be string that is delimited by three qoutes. In this 
string new line characters must have two slashes (ie '\\n') for them 
work.

'width' determines how many characters a line of text can be.
'height' determines how many lines will be displayed within one border.
'border_char' determines the character that will be used as the border.
"""

class TextOutput(object):
    """
    Uses TextFormat to reformat the 'text' and then prints the 
    resulting pages.
    """
    def __init__(self, text, width=60, height=15, border_char='#'):
        self.text = text
        self.width = width
        self.height = height
        self.border_char = border_char
        self.text_format = TextFormat(self.text, self.width, self.height,
                                 self.border_char)
        
        self.text_format.text_formatting()
    
    def display_text(self):
        """
        Gets the text pages from TextFormat and then displays the pages
        with the ability to browse through them.
        """
        text_end = "Press 'e' to end. "
        text_next = "Press 'n' for next. "
        text_back = "Press 'b' for back. "
        cls = 100 * '\n'
        total = len(self.text_format.border_text_list)
        end = False
        index = 0
        
        while end == False:
            print cls
            for lines in self.text_format.border_text_list[index]:
                print lines
            
            if total == 1:
                answer = raw_input(text_end)
                end = True
                continue
            elif index == 0:
                answer = raw_input(text_next + text_end)
#                print answer
                if answer == 'n':
                    index += 1
                    continue
                else:
                    end = True
                    continue
            elif index > 0 and index < total - 1:
                answer = raw_input(text_next + text_back + text_end)
                if answer == 'n':
                    index += 1
                    continue
                elif answer == 'b':
                    index -= 1
                    continue
                else:
                    end = True
                    continue
            elif index == total - 1:
                answer = raw_input(text_back + text_end)
                if answer == 'b':
                    index -= 1
                    continue
                else:
                    end = True 
                    continue
            else:
                raise ValueError("len, index: ", total, index)
            

class TextFormat(object):
    """
    The string 'text' is reformatted in several pages with borders 
    around them. 
    """
    def __init__(self, text, width, height, border_char):
        self.text = text
        self.width = width
        self.height = height
        self.border_char = border_char
        self.words = self.text.split()
        self.border_text_list = []

    def text_formatting(self):
        while self.words:
            border_text = self.create_border_text()
            self.border_text_list.append(border_text)
    
    def create_border_text(self):
        """
        Cuts the 'text' into pages and creates a border around the 
        page.
        """
        border_char = self.border_char
        border_width = self.width + 4
        border_line = '{0:{1}^{2}}'.format('', border_char, border_width)
        space = '{0:{1}^{2}}'.format('', ' ', self.width)
        border_line_space = '{0} {1} {2}'.format(border_char, space, border_char)
        border_text = []
        line = border_char
        border_text.append(border_line)
        border_text.append(border_line_space)
   
        while len(border_text) <= self.height and self.words != []:
            word = self.words.pop(0)
            new_lines = word.count('\\n')
            if new_lines > 0 and line != border_char:
                line = '{0: <{1}} {2}'.format(line, self.width + 2, border_char)
                border_text.append(line)
                for i in range(0, new_lines):
                    border_text.append(border_line_space) 
                line = border_char
                continue
            elif new_lines > 0 and line == border_char:
                line = '{0: <{1}} {2}'.format(line, self.width + 2, border_char)
                border_text.append(line)
                line = border_char
                continue
            elif new_lines == 0:
                test_width = line + ' ' + word
                if len(test_width) <= self.width:
                    line = line + ' ' + word
                else:
                    line = '{0: <{1}} {2}'.format(line, self.width + 2, border_char)
                    border_text.append(line)
                    line = border_char + ' ' + word
            else:
                raise ValueError("new_lines, line : ", new_lines, line)
    
        line = '{0: <{1}} {2}'.format(line, self.width + 2, border_char)
        border_text.append(line)
        border_text.append(border_line_space)
        border_text.append(border_line)
        return border_text