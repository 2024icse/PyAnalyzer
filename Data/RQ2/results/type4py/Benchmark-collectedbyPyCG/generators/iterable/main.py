class func(object):

    def __init__(self, n: int):
        self.n = n
        self.num = 0

    def __iter__(self) ->int:
        return self

    def __next__(self) ->int:
        if self.num < self.n:
            cur, self.num = self.num, self.num + 1
            return cur
        else:
            raise StopIteration()


for i in func(100):
    pass
