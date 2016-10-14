# coding: utf-8

class Morph:
	'''
	形態素(Morph)
	'''

	def __init__(self):
		self.surf   = None # 表層
		self.pos1   = None # 品詞1 (名詞,動詞,記号,etc)
		self.pos2   = None # 品詞2 (数,サ変接続,一般,固有名詞,終助詞,係助詞,非自立,etc)
		self.conj1  = None # 活用1 (サ変・-スル,etc)
		self.conj2  = None # 活用2 (未然系,カ行促音便,etc)
		self.base   = None # 原型

	# def is_stopword(self):
		'''
		オブジェクトがStopWordであるか判定
		Stop WordであればTrue, そうでなければFalseを返す

		[判定内容]
		1.品詞(名詞・動詞・形容詞)であるか
		2.
		'''
		# if self.pos1


	# def get_all_features(self):
	# 	'''
	# 	形態素オブジェクトの主要なfeaturesを返す
	# 	例) メニュー	メニュー,名詞,一般,抽象的実体,abstract_entity
	# 	'''
	# 	return "{}\t{},{},{},{},{}".format(self.surf, self.base, self.pos1, self.pos2, self.hypej, self.hypee)