




class Cylinder(object):
    def __init__(self, diameter, height):
        self.diameter = diameter
        self.height = height

    def volume(self):
        r = self.diameter / 2
        v = r**2 * 3.14 * self.height
        return v



class Prism(object):
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def volume(self):
        return self.length * self.width * self.height



class Substance(object):
    CATALOG = {
        'water': {'symbol': 'w', 'cubic_feet': 62.42718356},
        'dirt': {'symbol': 'd', 'cubic_feet': 76.5},
        'salt': {'symbol': 'sa', 'cubic_feet': 80},
        'sugar': {'symbol': 'sug', 'cubic_feet': 52.77},
        'diesel': {'symbol': 'd', 'cubic_feet': 53.11},
        'bromine': {'symbol': 'b', 'cubic_feet': 193.78},

    }