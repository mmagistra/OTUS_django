class Barrel:
    def __init__(self, num):
        self.num = num

    def get_num(self):
        return self.num

    def __str__(self):
        return str(self.num)

    def __repr__(self):
        return str(self.num)

    def __eq__(self, other):
        return self.num == other.num

    def __ne__(self, other):
        return self.num != other.num
