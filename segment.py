# coding: utf-8


class Border:
    def __init__(self):
        self.before = None  # int
        self.after = None  # int
        self.score = None  # float
        self.cand = None  # bool


class Segment:
    def __init__(self, start, end, length):
        self.start = start  # int
        self.end = end  # int
        self.length = length  # int
