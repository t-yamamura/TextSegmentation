import math
import numpy as np

from lexical_chain import LexicalChain, AnalysisWindow
from border import Border
from segment import Segment
from sentence import Sentence
from tokenizer import load_parser


class LCseg(object):
    """
    Lexical Cohesion segmentationを実行するクラス
    """
    def __init__(self, gap, window, p_limit, alpha):
        self.gap = gap
        self.window = window
        self.p_limit = p_limit
        self.alpha = alpha
        self.text_length = None
        self.lexical_chains = None
        self.lexical_cohesion_scores = None
        self.borders = None
        self.segments = None

    def run(self, sentences, reference_border_num=None):
        """

        :param list[sentence.Sentence] sentences:
        :param None|int reference_border_num:
        :return:
        """
        self.lexical_chains = self.make_lexical_chain(sentences)
        self.lexical_cohesion_scores = self.calc_lexical_cohesion_score(self.lexical_chains)
        self.borders = self.make_borders(self.lexical_cohesion_scores)
        final_borders = self.get_final_borders(self.borders, reference_border_num)
        self.segments = self.border2segment(final_borders)
        segmented_sentences = self.get_segmented_sentences(sentences)
        return segmented_sentences

    def read_file(self, file_path, tokenizer='ja', dic='', stop_words=None):
        """

        :param file_path:
        :param str|function tokenizer:
        :param dic:
        :param stop_words:
        :return:
        :rtype: list[sentence.Sentence]
        """
        parser = load_parser(tokenizer, dic, stop_words)

        sentences = []
        with open(file_path, 'r') as f:
            line_num = 0
            for line in f:
                if line != '':
                    sentence = Sentence(line.rstrip(), line_num, parser)
                    sentences.append(sentence)
                    line_num += 1

        self.text_length = len(sentences)

        return sentences

    def read_data(self, list_data, tokenizer='ja', dic='', stop_words=None):
        """

        :param list list_data:
        :param str|function tokenizer:
        :param dic:
        :param stop_words:
        :return:
        :rtype: list[sentence.Sentence]
        """
        parser = load_parser(tokenizer, dic, stop_words)

        sentences = [Sentence(data, i, parser) for i, data in enumerate(list_data)]
        self.text_length = len(sentences)

        return sentences

    def make_lexical_chain(self, sentences):
        """
        連鎖語に対して，語彙的連鎖オブジェクト(LexicalChain)を生成し，リストで返す
        :params list[morph.Morph] sentences:
        :return:
        :rtype: list[lexical_chain.LexicalChain]
        """
        lexical_chains = []
        registered_morphs = []
        for (i, sentence) in enumerate(sentences):
            for morph in sentence.morphs:
                # まだ連鎖を生成していない単語ならば連鎖を生成
                if morph.surf not in registered_morphs and morph.surf is not None:

                    # 単語(morph)に対する語彙的連鎖を生成
                    morph_chains = self.create_word_chain(morph, i, sentences)
                    if morph_chains:
                        lexical_chains.extend(morph_chains)

                    # 生成した連鎖を登録
                    registered_morphs.append(morph.surf)
        return lexical_chains

    def create_word_chain(self, query_morph, i, sentences):
        """
        単語(morph)に対する語彙的連鎖を生成
        閾値gap以下で出現する単語同士を連鎖とし，閾値以上であれば連鎖を分割
        :param morph.Morph query_morph:
        :param int i:
        :param list[sentence.Sentence] sentences:
        :return:
        :rtype: list[lexical_chain.LexicalChain]
        """

        morph_chains = []

        # current chain status
        start_num, end_num = i, i
        length, word_cnt, gap_len = 1, 1, 0
        entries, morphs = [], []

        for j in range(i + 1, len(sentences)):
            next_morph = sentences[j].find_morph_in_sentence(query_morph.surf)
            if next_morph:
                # 出現した単語間の距離(gap)を更新
                gap_len = j - end_num

                # 連鎖を繋げる場合(gapが閾値以下)
                if gap_len <= self.gap:

                    # 連鎖情報の更新
                    end_num = j
                    length = end_num - start_num + 1
                    word_cnt += 1
                    entries.append(j)
                    morphs.append(next_morph)

                # 連鎖を分割する場合(gapが閾値より大きい)
                else:
                    # 連鎖の生成を行うとき(単語が一つだけの場合は連鎖としない)
                    if word_cnt > 1:
                        lc = LexicalChain(word=query_morph.surf,
                                          start_num=start_num,
                                          end_num=end_num,
                                          length=length,
                                          word_cnt=word_cnt,
                                          score=word_cnt * math.log(len(sentences) / length),
                                          entries=entries[:],
                                          morphs=morphs[:])
                        morph_chains.append(lc)

                    # 連鎖情報の更新
                    start_num, end_num = j, j
                    length, word_cnt, gap_len = 1, 1, 0
                    entries, morphs = [j], [next_morph]

        # 残った連鎖情報に対して連鎖の生成を行うか判断
        if word_cnt > 1:
            lc = LexicalChain(word=query_morph.surf,
                              start_num=start_num,
                              end_num=end_num,
                              length=length,
                              word_cnt=word_cnt,
                              score=word_cnt * math.log(len(sentences) / length),
                              entries=entries[:],
                              morphs=morphs[:])
            morph_chains.append(lc)

        return morph_chains

    def calc_lexical_cohesion_score(self, lexical_chains):
        """
        語彙的結束性スコアを計算
        
        左右の分析窓(window_left, window_right)に
        オーバーラップする語彙的連鎖のコサイン類似度を計算
        :param list[lexical_chain.LexicalChain] lexical_chains:
        :return:
        :rtype: list[float]
        """

        lexical_cohesion_scores = []
        for i in range(0, self.text_length - self.window * 2 + 1):

            # ２つの分析窓(window_left, window_right)の開始・終了点(start, end)の更新
            j = i + self.window
            wl = AnalysisWindow(start=i, end=j - 1)
            wr = AnalysisWindow(start=j, end=j + self.window - 1)
            # print("wl.s {} wl.e {}   wr.s {} wr.e {}".format(wl.start, wl.end, wr.start, wr.end))

            # 分析窓内の連鎖の内積を計算
            window_dot = 0
            for lexical_chain in lexical_chains:
                # 連鎖が2つの分析窓にオーバラップするとき
                if lexical_chain.check_overlap_window(wl) and lexical_chain.check_overlap_window(wr):
                    window_dot += lexical_chain.score ** 2

            # ２つの分析窓の連鎖の大きさの積を計算
            for lexical_chain in lexical_chains:
                if lexical_chain.check_overlap_window(wl):
                    wl.vecsize += lexical_chain.score ** 2
                if lexical_chain.check_overlap_window(wr):
                    wr.vecsize += lexical_chain.score ** 2
            window_vecsize = math.sqrt(wl.vecsize) * math.sqrt(wr.vecsize)

            # ２つの分析窓のコサイン類似度を計算
            window_cosine_sim = 0
            if window_vecsize != 0:
                window_cosine_sim = window_dot / window_vecsize

            # 類似度リストに追加
            lexical_cohesion_scores.append(window_cosine_sim)

        return lexical_cohesion_scores

    def make_borders(self, lexical_cohesion_scores):
        """
        分割する境界線の候補を選定

        :param list[float] lexical_cohesion_scores:
        :return:
        :rtype: list[border.Border]
        """
        borders = []
        for i in range(0, len(lexical_cohesion_scores) - 2):
            # 語彙的結束性スコアを用いて境界線信頼値の計算
            p_mi = (lexical_cohesion_scores[i] + lexical_cohesion_scores[i+2] - lexical_cohesion_scores[i+1] * 2) / 2
            # 境界線情報を保持
            border = Border(before=i+self.window,
                            after=i+self.window+1,
                            score=p_mi,
                            cand=True if p_mi >= self.p_limit else False)
            borders.append(border)

        return borders

    def get_final_borders(self, borders, reference_border_num):
        """

        :param list[border.Border] borders:
        :param None|int reference_border_num: the number of reference borders
        :return: final borders
        :rtype: list[border.Border]
        """
        if reference_border_num is not None and reference_border_num >= 1:
            # if reference_border_num (the number of reference borders) is given
            if reference_border_num > len(borders):
                print('The number of segment is lower than reference_border_num.')
            # Return borders with top reference_border_num scores.
            return sorted(borders, key=lambda x: x.score, reverse=True)[:reference_border_num]
        else:
            # if reference_border_num is unknown
            border_candidates = [border for border in borders if border.cand is True]
            if not border_candidates:
                return []
            else:
                border_candidate_scores = np.array(list(map(lambda x: x.score, border_candidates)))
                threshold = np.average(border_candidate_scores) - self.alpha * np.std(border_candidate_scores)

                return [border for border in border_candidates if border.score >= threshold]

    def border2segment(self, borders):
        """

        :param list[border.Border] borders:
        :return:
        :rtype: list[segment.Segment]
        """
        segments = []

        start_index = 0
        borders = sorted(borders, key=lambda x: x.before)
        for border in borders:
            segment = Segment(start=start_index, end=border.before, length=border.before-start_index+1)
            segments.append(segment)
            start_index = border.after
        last_segment = Segment(start=start_index, end=self.text_length-1, length=self.text_length-start_index)
        segments.append(last_segment)

        return segments

    def get_segmented_sentences(self, sentences):
        """
        :param list[sentence.Sentence] sentences:
        :return:
        :rtype: list[list[str]]
        """
        segmented_sentences = []
        for segment in self.segments:
            lines = [sentence.surf for sentence in sentences[segment.start:segment.end+1]]
            segmented_sentences.append(lines)
        return segmented_sentences
