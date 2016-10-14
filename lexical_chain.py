# coding: utf-8

class LexicalChain:

	def __init__(self):
		self.word      = None # str   連鎖語
		self.start_num = None # int   連鎖の開始点(文番号)
		self.end_num   = None # int   連鎖の終了点(文番号)
		self.length    = None # int   連鎖長
		self.word_cnt  = None # int   連鎖内の単語数
		self.score     = None # float 連鎖スコア
		self.entries   = None # list  連鎖語の発話番号
		self.morphs    = None # list  連鎖語の形態素リスト

