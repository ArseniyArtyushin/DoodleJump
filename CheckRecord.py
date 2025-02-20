class Record:
    def __init__(self):
        self.score = 0

    def read_score(self):
        with open('record.txt', 'r') as record:
            self.score = int(record.readlines()[-1].strip())
        return self.score

    def write_score(self, s):
        with open('record.txt', 'w+') as record:
            record.write(str(s))
