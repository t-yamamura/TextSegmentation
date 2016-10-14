# coding: utf-8

class Log:
	'''
	ログファイルを./logに生成
	'''

	def __init__(self, sentences):
		self.sentences = sentences

	def execute(self):
		self.write_mecab_result_nodes()

	def write_mecab_result_nodes(self):
		'''
		MeCabによる解析結果をファイルに出力
		'''
		f = open('./log/mecab_result_nodes.log', 'w')

		for sentence in self.sentences:
			for morph in sentence.morphs:
				f.write(morph.read_morph() + "\n")
		f.close()