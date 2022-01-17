class Cycle:
    def __init__(self, string, N) -> None:
        self.string = string
        self.l = len(string)
        self.N = N
        self.n = 0
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i == self.l:
            self.n += 1
            self.i = 0
                
        if self.n == self.N:
            raise StopIteration("THE END!")

        i = self.i % self.l
        self.i = self.i + 1
        return self.string[i]

c = Cycle("HI!", 2)
for i in c:
    print(i)