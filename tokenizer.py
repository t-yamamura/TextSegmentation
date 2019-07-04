import MeCab
from morph import Morph


def load_parser(tokenizer, dic, stop_words):
    if tokenizer == 'ja':
        parser = lambda x: mecab_parser(x, dic=dic, stop_words=stop_words)
    elif tokenizer == 'space':
        parser = lambda x: space_split_parser(x, stop_words=stop_words)
    elif isinstance(tokenizer, function):
        parser = lambda x: user_parser(tokenizer, x, stop_words=stop_words)
    else:
        raise ValueError("tokenizer parameter is 'ja' or 'space' or user default function.")
    return parser


def mecab_parser(line, dic='', stop_words=None):
    """
    parser for japanese sentence

    :param str line:
    :param str dic: dictionary path of MeCab
    :param stop_words:
    :return: parsed words
    :rtype: list[morph.Morph]
    """
    morphs = []

    if dic:
        dic = '-d ' + dic

    stop = None
    if stop_words == 'default':
        stop = 'default'
    elif isinstance(stop_words, list) and all([isinstance(stop_word, str) for stop_word in stop_words]):
        stop = 'list'
    elif stop_words is None:
        pass
    else:
        raise ValueError("stop_words must be 'default' or list[str]")

    tagger = MeCab.Tagger(dic)
    tagger.parse(dic)
    node = tagger.parseToNode(line)
    while node:
        if not node.feature.startswith('BOS/EOS'):
            features = node.feature.split(',')
            morph = Morph(surf=node.surface,
                          pos1=features[0],
                          pos2=features[1],
                          conj1=features[4],
                          conj2=features[5],
                          base=features[6])
            if morph.base == '*':
                morph.base = morph.surf

            if stop == 'default':
                if not morph.is_stopword():
                    morphs.append(morph)
            elif stop == 'list':
                if morph.surf not in stop_words:
                    morphs.append(morph)
            else:
                morphs.append(morph)

        node = node.next

    return morphs


def space_split_parser(line, stop_words=None):
    """

    :param str line:
    :param list[str] stop_words:
    :return: parsed words
    :rtype: list[morph.Morph]
    """
    if stop_words is None:
        stop_words = []
    return [Morph(word, '', '', '', '', word) for word in line.split(' ') if word not in stop_words]


def words_parser(words, stop_words=list):
    """

    :param list[str] words:
    :param list[str] stop_words:
    :return: parsed words
    :rtype: list[morph.Morph]
    """
    if stop_words is None:
        stop_words = []
    return [Morph(word, '', '', '', '', word) for word in words if word not in stop_words]


def user_parser(parser, line, stop_words=None):
    """

    :param function parser:
    :param str line:
    :param stop_words:
    :return:
    """
    if stop_words is None:
        stop_words = []
    return [Morph(word, '', '', '', '', word) for word in parser(line) if word not in stop_words]