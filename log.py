# coding: utf-8

class Log:
	'''
	ログファイルを./logに生成
	'''

	def __init__(self, sentences, lexical_chains):
		self.sentences = sentences
		self.lexical_chains = lexical_chains

	def execute(self):
		self.write_mecab_result_nodes()
		self.write_lexical_chain_list()

	def write_mecab_result_nodes(self):
		'''
		MeCabによる解析結果をファイルに出力
		'''
		f = open('./log/mecab_result_nodes.log', 'w')

		for sentence in self.sentences:
			for morph in sentence.morphs:
				f.write(morph.read_morph() + "\n")
		f.close()

	def write_lexical_chain_list(self):
		'''
		LCsegの語彙的連鎖のリストをファイルに出力
		'''
		f = open('./log/lexical_chain_list.log', 'w')

		for lc in self.lexical_chains:
			f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(lc.word, lc.start_num, lc.end_num, lc.length, lc.word_cnt, lc.score))
		f.close()