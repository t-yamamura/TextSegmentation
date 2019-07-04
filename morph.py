# coding: utf-8
import re


class Morph:
    """
    形態素(Morph)
    """

    def __init__(self, surf, pos1, pos2, conj1, conj2, base):
        """
        :param str surf: 表層
        :param str pos1: 品詞1 (名詞,動詞,記号,etc)
        :param str pos2: 品詞2 (数,サ変接続,一般,固有名詞,終助詞,係助詞,非自立,etc)
        :param str conj1: 活用1 (サ変・-スル,etc)
        :param str conj2: 活用2 (未然系,カ行促音便,etc)
        :param str base: 原型
        """
        self.surf = surf
        self.pos1 = pos1
        self.pos2 = pos2
        self.conj1 = conj1
        self.conj2 = conj2
        self.base = base

    def read_morph(self):
        return "{}\t{},{},{},{},{}".format(self.surf, self.pos1, self.pos2, self.conj1, self.conj2, self.base)

    def is_stopword(self):
        """
        オブジェクトがStopWordであるか判定
        Stop WordであればTrue, そうでなければFalseを返す

        [判定内容]
        1.品詞が名詞・動詞・形容詞でなければStopWordと判定
        2.形式名詞(ex.こと)であればStopWordと判定
        3.ひらがな・カタカナの1文字の名詞であればStopWordと判定
        """

        # 品詞が名詞・動詞・形容詞でなければStopWordと判定
        if re.match(r"名詞|動詞|形容詞", self.pos1) is None:
            return True

        # 2.形式名詞(ex.こと)であればStopWordと判定
        if re.search(r"もの|こと|よう|ところ|わけ|はず|つもり", self.surf) and self.pos1 == '名詞' and self.pos2 == '非自立':
            return True

        # 3.ひらがな・カタカナの1文字の名詞であればStopWordと判定
        if re.match(r"[ぁ-んァ-ン]", self.surf) is not None and len(self.surf) == 1 and self.pos1 == '名詞':
            return True

        return False
