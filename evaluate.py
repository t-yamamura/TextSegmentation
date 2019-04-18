
import segeval

from sentence import Sentence
from lcseg import LCseg
from tqdm import tqdm


def get_opts():
    import argparse

    parser = argparse.ArgumentParser()
    # file parameter
    parser.add_argument('-i', '--input_file_path',
                        default="label_utter/20150313_C1.txt",
                        help='File path of input text you want to segment.')
    # MeCab dic parameter
    parser.add_argument('-d', '--dic',
                        default="",
                        help='Dictionary path for MeCab')
    # text segmentation's parameter
    parser.add_argument('-g', '--gap',
                        type=int,
                        default=4,
                        help='連鎖を分割する空白の長さ(gap)')
    parser.add_argument('-w', '--window',
                        type=int,
                        default=1,
                        help='分析窓幅(window)')
    parser.add_argument('-pl', '--p_limit',
                        type=float,
                        default=0.1,
                        help='境界線信頼値の足きり閾値')
    parser.add_argument('-a', '--alpha',
                        type=float,
                        default=0.6,
                        help='仮定した境界線に対する閾値の限界')

    options = parser.parse_args()
    options.text_length = 0
    if options.dic != "":
        options.dic = "-d " + options.dic
    return options


def read_input(input_file_path, dic):
    labels = []
    sentences = []
    sentence_num = 0
    with open(input_file_path, 'r') as f:
        for line in f:
            label, utterance = line.rstrip().split(',')
            if line != '':
                s = Sentence()
                s.surf = utterance
                s.num = sentence_num
                s.morphs = s.make_mecab_result_nodes(dic)
                sentences.append(s)
                sentence_num += 1
                labels.append(label)
    return labels, sentences


def get_ref_segments(labels):
    segs = []
    prev_tag = ''
    tmp = []
    for label in labels:
        if prev_tag == '':
            tmp.append(label)
            prev_tag = label
        elif prev_tag == label:
            tmp.append(label)
        elif prev_tag != label:
            segs.append(tmp[:])
            tmp = []
            tmp.append(label)
            prev_tag = label
    segs.append(tmp[:])
    return segs


def main(opts):
    labels, sentences = read_input(opts.input_file_path, opts.dic)
    opts.text_length = len(labels)

    best_pk = 1
    best_wd = 1
    param_pk = (None, None, None, None)
    param_wd = (None, None, None, None)

    # for g in range(1, 21):
    #     opts.gap = g
    #     for w in range(1, 21):
    #         opts.window = w
    #         for pl in tqdm(range(1, 11)):
    #             opts.p_limit = pl / 10
    #             for a in range(1, 11):
    #                 opts.alpha = a / 10

    lcseg = LCseg(opts)
    lexical_chains = lcseg.make_lexical_chain(sentences)
    lexical_cohesion_scores = lcseg.calc_lexical_cohesion_score(lexical_chains)
    borders = lcseg.const_segment_borders_info(lexical_cohesion_scores)
    if borders:
        segments = lcseg.const_segments_info(borders)
        hyp = tuple(map(lambda x: x.length, segments))
        ref = tuple(map(len, get_ref_segments(labels)))
        pk = segeval.pk(ref, hyp)
        wd = segeval.window_diff(ref, hyp)
        print(hyp)
        print(ref)
        print(pk)
        print(wd)
    #     if wd < best_wd:
    #         best_wd = wd
    #         param_wd = (opts.gap, opts.window, opts.p_limit, opts.alpha)
    #     if pk < best_pk:
    #         best_pk = pk
    #         param_pk = (opts.gap, opts.window, opts.p_limit, opts.alpha)
    #
    # print(best_pk)
    # print(param_pk)
    # print(best_wd)
    # print(param_wd)


if __name__ == '__main__':
    main(get_opts())
