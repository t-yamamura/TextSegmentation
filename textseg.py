# coding: utf-8
import argparse
from sentence import Sentence
from lcseg import LCseg
from log import Log


class TextSeg:
    def __init__(self):
        """
        引数をargparseで解析しオブジェクトに追加
        """
        parser = argparse.ArgumentParser(description='This script is to segment text using LCseg.')
        # file parameter
        parser.add_argument('-i', '--input_file_path',
                            default="./dat/sample.dat",
                            help='File path of input text you want to segment.')
        # MeCab dic parameter
        parser.add_argument('-d', '--dic',
                            default="",
                            help='Dictionary path for MeCab')
        # text segmentation's parameter
        parser.add_argument('-g', '--gap',
                            type=int,
                            default=11,
                            help='連鎖を分割する空白の長さ(gap)')
        parser.add_argument('-w', '--window',
                            type=int,
                            default=2,
                            help='分析窓幅(window)')
        parser.add_argument('-pl', '--p_limit',
                            type=float,
                            default=0.1,
                            help='境界線信頼値の足きり閾値')
        parser.add_argument('-a', '--alpha',
                            type=float,
                            default=0.5,
                            help='仮定した境界線に対する閾値の限界')

        self.options = parser.parse_args()
        self.options.text_length = 0
        if self.options.dic != "":
            self.options.dic = "-d " + self.options.dic

    def read_input(self, input_file_path):
        """
        入力ファイルを読み込み，文オブジェクト(Sentence)のリストを返す
        """
        sentences = []
        sentence_num = 0
        f = open(input_file_path, 'r')
        for readline in f.readlines():
            readline = readline.rstrip()
            if readline != '':
                s = Sentence()
                s.surf = readline
                s.num = sentence_num
                s.morphs = s.make_mecab_result_nodes(self.options.dic)
                sentences.append(s)
                sentence_num += 1
        f.close()
        self.options.text_length = len(sentences)
        return sentences

    def execute_lexical_segmentation(self):
        sentences = self.read_input(self.options.input_file_path)

        lcseg = LCseg(self.options)
        lexical_chains = lcseg.make_lexical_chain(sentences)
        lexical_cohesion_scores = lcseg.calc_lexical_cohesion_score(lexical_chains)
        borders = lcseg.const_segment_borders_info(lexical_cohesion_scores)
        segments = lcseg.const_segments_info(borders)
        segmented_sentences = lcseg.segment_sentences(borders, sentences)

        for ss in segmented_sentences:
            print("{}\n=== SEGMENT ===\n".format(ss))

        # ログの書き出し
        log = Log(sentences, lexical_chains, borders, segments, segmented_sentences)
        log.execute()


if __name__ == '__main__':
    ts = TextSeg()
    ts.execute_lexical_segmentation()
