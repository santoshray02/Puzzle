# coding=utf-8


class WrongInputException(ValueError):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return "Error code: {}. Message: {}".format(self.code, self.message)

class PuzzleSolver:
    '''
    FindWords should return the number of all non-distinct occurrences 
    of the words found in the array, horizontally, vertically or diagonally, 
    and also the reverse in each direction. 
    The input to FindWords is a rectangular matrix of characters 
    (list of list of char).
    
    We are trying to see the quality of the code you write (hint: unit tests).  
    Don’t worry too much about performance and efficiency 
    but you program should work correctly. 
    It should also be capable of scaling to puzzles 
    with dimensions such as 4x4, 6x9, 9x9. 
    '''

    DICTIONARY = ['OX','CAT','TOY','AT','DOG','CATAPULT','T']    

    def __init__(self, input_list):
        self.input_list = input_list        
        if self.input_valid():
            self.result = 0
            self.puzzle_width = len(input_list[0])
            self.puzzle_height = len(input_list)

    def input_valid(self):
        if not isinstance(self.input_list, list) or len(self.input_list) == 0:
            raise WrongInputException(
                0, 'Init parameter is not instance of the list or is empty')
        else:
            inner_list_length = 0
            for index, charList in enumerate(self.input_list):
                if not hasattr(charList, '__iter__'):
                    raise WrongInputException(1, 'Row {} is not iterable'.format(index))
                else:
                    inner_list_length = len(charList)

            for index, charList in enumerate(self.input_list):
                if len(charList) != inner_list_length:
                    raise WrongInputException(2, 'Row #{} have different length'.format(index))

            for i, charList in enumerate(self.input_list):
                for j, char in enumerate(charList):
                    if not isinstance(char, str):
                        raise WrongInputException(3, 'Element #{} in #{} is not string: "{}"'.format(j, i, char))
                    elif not char.isalpha():
                        raise WrongInputException(4, 'Element #{} in #{} row is not alphabetical: "{}"'.format(j, i, char))
                    elif len(char) != 1:
                        raise WrongInputException(5, 'Element #{} in #{} is not a single char: "{}"'.format(j, i, char))
            return True


    def find_words(self):
        if self.input_valid():
            string_list = self.get_string_list()
            
            for word in self.DICTIONARY:
                if len(word) == 1:
                    for char_list in self.input_list:
                        string = ''.join(char_list)
                        self.result += string.count(word)
                else:
                    for string in string_list:
                        self.result += self.find_word_in_string(word, string)
            return self.result

    @staticmethod
    def find_word_in_string(word, string):
        result = 0
        if len(word) > 1:            
            result += sum(string[i:].startswith(word) for i in range(len(string)))
            result += sum(string[i:].startswith(word[::-1]) for i in range(len(string)))                
            return result

    def get_string_list(self):
        axis = [''.join(char_list) for char_list in self.input_list]

        for i in range(self.puzzle_width):
            axis.append(''.join([char_list[i] for char_list in self.input_list]))


        original_puzzle = self.input_list

        if self.puzzle_height > self.puzzle_width:
            # rotating clockwise            
            self.__init__(zip(*original_puzzle[::-1]))

        diagonales, diagonales_reversed = [], []
        for i in range(self.puzzle_width-1):
            diagonal = []
            another_diagonal = []
            j = 0
            for v_index, char_list in enumerate(self.input_list):
                if i+j < self.puzzle_width:
                    diagonal.append(char_list[i+j])
                    another_diagonal.append(char_list[::-1][i+j])
                    j += 1
            diagonales.append(''.join(diagonal))
            diagonales_reversed.append(''.join(another_diagonal))

        for i in range(self.puzzle_width)[:0:-1]:
            diagonal = []
            another_diagonal = []
            j = 0
            for char_list in reversed(self.input_list):
                if i - j >= 0:
                    diagonal.append(char_list[i-j])
                    another_diagonal.append(char_list[::-1][i-j])
                    j += 1
            diagonales.append(''.join(reversed(diagonal)))
            diagonales_reversed.append(''.join(reversed(another_diagonal)))

        self.__init__(original_puzzle)

        return axis + list(set(diagonales)) + list(set(diagonales_reversed))