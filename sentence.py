class Sentence:
    """
    文
    """

    def __init__(self, surf, num, parser):
        """

        :param str surf: 表層
        :param int num: 文番号
        :param function parser: 形態素
        """
        self.surf = surf
        self.num = num
        self.morphs = parser(self.surf)

    def find_morph_in_sentence(self, surf):
        for morph in self.morphs:
            if morph.surf == surf:
                return morph
        return None
