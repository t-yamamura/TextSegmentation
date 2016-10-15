# coding: utf-8

import math
from lexical_chain import LexicalChain
from lexical_chain import AnalysisWindow
from segment_border import SegmentBorder

class LCseg:
	'''
	Lexical Cohesion segmentationを実行するクラス
	'''

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

					# 単語(morph)に対する語彙的連鎖を生成
					morph_chains = self.create_word_chain(morph, i, sentences)
					if morph_chains:
						lexical_chains.extend(morph_chains)

					# 生成した連鎖を登録
					registerd_morphs.append(morph.surf)
		return lexical_chains

	def create_word_chain(self, query_morph, i, sentences):
		'''
		単語(morph)に対する語彙的連鎖を生成
		閾値gap以下で出現する単語同士を連鎖とし，閾値以上であれば連鎖を分割
		'''

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

	def calc_lexical_cohesion_score(self, lexical_chains):
		'''
		語彙的結束性スコアを計算
		
		左右の分析窓(window_left, window_right)に
		オーバーラップする語彙的連鎖のコサイン類似度を計算
		'''
		lexical_cohesion_scores = []
		for i in range(0, self.options.text_length - self.options.window * 2 + 1):

			# ２つの分析窓(window_left, window_right)の開始・終了点(start, end)の更新
			j = i + self.options.window
			wl = AnalysisWindow(start=i, end=j-1)
			wr = AnalysisWindow(start=j, end=j+self.options.window-1)
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
			if window_vecsize != 0:
				window_cosine_sim = window_dot / window_vecsize

			# 類似度リストに追加
			lexical_cohesion_scores.append(window_cosine_sim)

		return lexical_cohesion_scores


	def const_segment_info(self, lexical_cohesion_scores):

		'''
		分割する境界線の候補を選定
		各境界線に対して，境界線信頼値を計算し，閾値以上のものを選定
		'''
		sb_cands = []
		sb_cands_pmi_sum = 0
		for i in range(0, len(lexical_cohesion_scores) - 2):

			# 語彙的結束性スコアを用いて境界線信頼値の計算
			p_mi = (lexical_cohesion_scores[i] + lexical_cohesion_scores[i+2] - lexical_cohesion_scores[i+1] * 2) / 2

			# 境界線情報を保持
			sb = SegmentBorder()
			sb.before = i + self.options.window
			sb.after  = i + self.options.window + 1
			sb.score  = p_mi
			sb.cand   = True

			# 境界線信頼値の閾値以上の境界候補のみを選定
			if sb.score >= self.options.p_limit:
				sb_cands.append(sb)
				sb_cands_pmi_sum += sb.score

		'''
		分割する境界線の決定
		足きりで残った境界線に対して，最終的な境界線信頼値を計算
		'''
		# 分割する境界線が存在しない場合
		if len(sb_cands) == 0:
			print("分割する境界線が存在しません.")
			exit(0)
		else:
			# 境界線信頼値の平均を計算
			sb_cands_pmi_ave = sb_cands_pmi_sum / len(sb_cands)
			# 標準偏差の計算
			disp = 0
