import argparse
from lcseg import LCseg
from log import Log


def get_options():
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

    options = parser.parse_args()
    return options


def main(options):

    lcseg = LCseg(gap=options.gap, window=options.window, p_limit=options.p_limit, alpha=options.alpha)
    sentences = lcseg.read_file(options.input_file_path)

    segmented_sentences = lcseg.run(sentences, reference_border_num=3)
    for ss in segmented_sentences:
        print('\n'.join(ss), end='\n\n')


if __name__ == '__main__':
    main(get_options())
