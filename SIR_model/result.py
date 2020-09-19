class Result:
    def __init__(self, initalDict={}):
        self.dictionary = initalDict

    def __setitem__(self, key, value):
        if not key in self.dictionary:
            self.dictionary[key] = []
        self.dictionary[key].append(value)

    def __getitem__(self, key):
        if not key in self.dictionary:
            self.dictionary[key] = []
        return self.dictionary[key]
