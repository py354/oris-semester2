import bcrypt

class A:
    def __init__(self, a, b, **kwargs):
        self.a = a
        self.b = b
        print(kwargs)

    def __str__(self):
        return str(self.__dict__)

o = A(**{'a': 1, 'b': 2, 'c': 3})
print(o)