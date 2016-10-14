# coding: utf-8

import math
from lexical_chain import LexicalChain

class LCseg:

	def __init__(self, options):
		self.options = options

	def make_lexical_chain(self, sentences):
		'''
		連鎖語に対して，語彙的連鎖オブジェクト(LexicalChain)を生成し，リストで返す
		'''
		lexical_chains = []
		registerd_morphs = []
		for (i, sentence) in enumerate(sentences):
			for morph in sentence.morphs:
				# まだ連鎖を生成していない単語ならば連鎖を生成
				if morph.surf not in registerd_morphs and morph.surf is not None:

					morph_chains = self.create_word_chain(morph, i, sentences)
					if morph_chains:
						for morph_chain in morph_chains:
							lexical_chains.append(morph_chain)

					# 生成した連鎖を登録
					registerd_morphs.append(morph.surf)
		return lexical_chains

	def create_word_chain(self, query_morph, i, sentences):

		morph_chains = []

		# 現在の連鎖情報を保持
		status = {'start_num':i,
		          'end_num'  :i,
		          'length'   :1,
		          'word_cnt' :1,
		          'gap_len'  :0,
		          'entries'  :[],
		          'morphs'   :[]}

		for j in range(i+1, len(sentences)):
			next_morph = sentences[j].find_morph_in_sentence(query_morph.surf)
			if next_morph is not None:
				# 出現した単語間の距離(gap)を更新
				status['gap_len'] = j - status['end_num']

				# 連鎖を繋げる場合(gapが閾値以下)
				if status['gap_len'] <= self.options.gap:

					# 連鎖情報の更新
					status['end_num']  = j
					status['length']   = status['end_num'] - status['start_num'] + 1
					status['word_cnt'] += 1
					status['entries'].append(j)
					status['morphs'].append(next_morph)

				# 連鎖を分割する場合(gapが閾値より大きい)
				else:

					# 連鎖の生成を行うとき(単語が一つだけの場合は連鎖としない)
					if status['word_cnt'] > 1:
						lc = LexicalChain()
						lc.word      = query_morph.surf
						lc.start_num = status['start_num']
						lc.end_num   = status['end_num']
						lc.length    = status['length']
						lc.word_cnt  = status['word_cnt']
						lc.score     = status['word_cnt'] * math.log(len(sentences) / status['length'])
						lc.entries   = status['entries'][:]
						lc.morphs    = status['morphs'][:]
						morph_chains.append(lc)

					# 連鎖情報の更新
					status['start_num']  = j
					status['end_num']    = j
					status['length']     = 1
					status['word_cnt']   = 1
					status['entries']    = []
					status['morphs']     = []
					status['entries'].append(j)
					status['morphs'].append(next_morph)

		# 残った連鎖情報に対して連鎖の生成を行うか判断
		if status['word_cnt'] > 1:
			lc = LexicalChain()
			lc.word      = query_morph.surf
			lc.start_num = status['start_num']
			lc.end_num   = status['end_num']
			lc.length    = status['length']
			lc.word_cnt  = status['word_cnt']
			lc.score     = status['word_cnt'] * math.log(len(sentences) / status['length'])
			lc.entries   = status['entries'][:]
			lc.morphs    = status['morphs'][:]
			morph_chains.append(lc)

		return morph_chains