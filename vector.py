import random
import math

class Vector:
    '''Vector class - contains defined number of elements. Sample operations on a class:
adding, substracting or multiplication
'''
    def __init__(self, size = 3, _list = [0,0,0]):
        '''Class constructor - no, one or two arguments can be passed.
        If list is passed, then vector takes its arguments 
        '''
        if(_list == [0,0,0]):
            self.size = size
            self.values = self.__generate_values()
        else:
            self.size = len(_list)
            self.values = _list
    
    def load_from_list(self, _list):
        '''Vector takes arguments from a list'''
        self.values = _list
        self.size = len(_list)

    def __generate_values(self):
        '''Vector takes random arguments (in float format, 
        rounded to two decimal points)'''
        figures = []
        for i in range(self.size):
            figures.append(round(random.randint(-100, 100) + random.random(), 2))
        return figures

    def __add__(self, other):
        '''Adding two vectors by adding its arguments 
        (if its sizes are the same)'''
        if(other.size != self.size):
            raise ValueError("Different lenght of vectors!")
        add = []
        for i in range(self.size):
            add.append(self.values[i] + other.values[i])
        return Vector(len(add), add)
    
    def __sub__(self, other):
        '''Substracting two vectors by substracting its arguments 
        (if its sizes are the same)'''
        if(other.size != self.size):
            raise ValueError("Different lenght of vectors!")
        sub = []
        for i in range(self.size):
            sub.append(self.values[i] - other.values[i])
        return Vector(len(sub), sub)

    def __mul__(self, other: float):
        '''Multiplying vector by a scalar (every argument)'''
        new_values = []
        for i in range(self.size):
            new_values.append(self.values[i] * other)
        size = len(new_values)
        return Vector(size, new_values)
    
    def __rmul__(self, other: float):
        '''Multiplying vector by a scalar'''
        return self.__mul__(other)

    def __len__(self):
        return self.size

    def length(self):
        '''Returns length of a vector - square root of a sum of
        its coordinates raised to the second power'''
        _length = 0.0
        for i in range(self.size):
            _length += self.values[i] **2
        _length = math.sqrt(_length)
        return _length
    
    def sum(self):
        '''Sum of every coordinate'''
        Sum = 0
        for i in range(self.size):
            Sum += self.values[i]
        return Sum

    def dot_product(self, other):
        ''''Scalar product - sum of the corresponding coordinates which are multiplied
        by themself'''
        if(self.size != other.size):
            raise ValueError("Different lenght of vectors!")
        product = 0
        for i in range(self.size):
            product += self.values[i] * other.values[i]
        return product
    
    def __str__(self):
        '''Prints vector coordinates'''
        string = "Vector coordinates: "
        for i in range(self.size):
            string += f"{self.values[i]} "
        return string

    def __getitem__(self, index):
        '''Shows value of a particular coordinate'''
        if index > self.size or index < 1:
            raise ValueError("Index is out of vector lenght")
        return self.values[index - 1]
    
    def __contains__(self, item):
        '''Checks if a particular value is present in one of the coordinates'''
        for i in range(self.size):
            if(item == self.values[i]):
                return True
        return False






