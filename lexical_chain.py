# coding: utf-8


class LexicalChain:
	'''
	語彙的連鎖
	'''

	def __init__(self):
		self.word      = None # str   連鎖語
		self.start_num = None # int   連鎖の開始点(文番号)
		self.end_num   = None # int   連鎖の終了点(文番号)
		self.length    = None # int   連鎖長
		self.word_cnt  = None # int   連鎖内の単語数
		self.score     = None # float 連鎖スコア
		self.entries   = None # list  連鎖語の発話番号
		self.morphs    = None # list  連鎖語の形態素リスト

	def check_overlap_window(self, analysis_window):
		'''
		語彙的連鎖が分析窓にオーバラップするか判定
		'''
		if self.end_num < analysis_window.start or analysis_window.end < self.start_num:
			return False
		else:
			return True

class AnalysisWindow:
	'''
	分析窓
	'''

	def __init__(self, start, end):
		self.start   = start # int   分析窓の開始点（文番号）
		self.end     = end   # int   分析窓の終了点（文番号）
		self.vecsize = 0     # float 分析窓内の連鎖の大きさ