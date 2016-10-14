# coding: utf-8

import MeCab
from morph import Morph

class Sentence:
	'''
	文
	'''

	def __init__(self):
		self.surf   = None # str  表層
		self.num    = None # int  文番号
		self.morphs = None # list 形態素


	def make_mecab_result_nodes(self, dic):
		morphs = []
		tagger = MeCab.Tagger(dic)
		tagger.parse('')
		node = tagger.parseToNode(self.surf)
		while node:
			if node.feature.startswith('BOS/EOS') == False:
				features = node.feature.split(',')

				morph = Morph()
				morph.surf = node.surface
				morph.pos1 = features[0]
				morph.pos2 = features[1]
				morph.conj1 = features[4]
				morph.conj2 = features[5]
				morph.base = features[6]

				if morph.base == '*':
					morph.base = morph.surf

				# ストップワード以外をリストに追加
				if morph.is_stopword() == False:
					morphs.append(morph)

			node = node.next

		return morphs