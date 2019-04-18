# coding: utf-8
import re


class Morph:
    """
    形態素(Morph)
    """

    def __init__(self):
        self.surf = None  # str 表層
        self.pos1 = None  # str 品詞1 (名詞,動詞,記号,etc)
        self.pos2 = None  # str 品詞2 (数,サ変接続,一般,固有名詞,終助詞,係助詞,非自立,etc)
        self.conj1 = None  # str 活用1 (サ変・-スル,etc)
        self.conj2 = None  # str 活用2 (未然系,カ行促音便,etc)
        self.base = None  # str 原型

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
