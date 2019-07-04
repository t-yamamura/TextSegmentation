class Border(object):
    def __init__(self, before, after, score, cand):
        """

        :param int before:
        :param int after:
        :param float score:
        :param bool cand:
        """
        self.before = before
        self.after = after
        self.score = score
        self.cand = cand
