# coding: utf-8


class LexicalChain:
    """
    語彙的連鎖
    """

    def __init__(self, word, start_num, end_num, length, word_cnt, score, entries, morphs):
        """
        :param str word: 連鎖語
        :param int start_num: 連鎖の開始点(文番号)
        :param int end_num: 連鎖の終了点(文番号)
        :param int length: 連鎖長
        :param int word_cnt: 連鎖内の単語数
        :param float score: 連鎖スコア
        :param list entries: 連鎖語の発話番号
        :param list morphs: 連鎖語の形態素リスト
        """
        self.word = word
        self.start_num = start_num
        self.end_num = end_num
        self.length = length
        self.word_cnt = word_cnt
        self.score = score
        self.entries = entries
        self.morphs = morphs

    def check_overlap_window(self, analysis_window):
        """
        語彙的連鎖が分析窓にオーバラップするか判定
        """
        if self.end_num < analysis_window.start or analysis_window.end < self.start_num:
            return False
        else:
            return True


class AnalysisWindow:
    """
    分析窓
    """

    def __init__(self, start, end):
        self.start = start  # int 分析窓の開始点（文番号）
        self.end = end  # int 分析窓の終了点（文番号）
        self.vecsize = 0  # float 分析窓内の連鎖の大きさ
