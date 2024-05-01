from collections import OrderedDict

class OrderedSet:
    """ An OrderedSet contains a sequence of items with no repetition. 
    
        Uses a collections.OrderedDict where each key has a single None value. """
    def __init__(self, string: str=None):
        """ Creates an ordered set. If a string is given, the set is created
            from the characters in the string, using the first appearance of
            a letter as its order in the set. """
        self.set = OrderedDict()
        if not string == None:
            self.set = OrderedDict.fromkeys(list(string))
            
    def append(self, item):
        """ If the item is not in the set, append it to the end of the set """
        self.set[item] = None
        
    def remove(self, item):
        """ Removes item from the set. Throws error if item is not in the set. """
        del self.set[item]
        
    def discard(self, item):
        """ Discards item from the set, if the item is in the set. """
        self.set.pop(item, None)
        
    def __iter__(self):
        """ Iterate through items """
        return iter(self.set.keys())
        
    def __str__(self):
        """ Returns string of the set """
        return "{" + ", ".join(map(str, self.set.keys())) + "}"