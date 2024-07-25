class Barrel:
    def __init__(self, num):
        self.num = num

    def get_num(self):
        return self.num

    def __key(self):
        return self.num

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Barrel):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        return str(self.num)

    def __repr__(self):
        return str(self.num)

    def __ne__(self, other):
        return self.num != other.num
