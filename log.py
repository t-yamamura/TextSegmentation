# coding: utf-8

class Log:
	'''
	ログファイルを./logに生成
	'''

	def __init__(self, sentences, lexical_chains, borders, segments, segmented_sentences):
		self.sentences           = sentences
		self.lexical_chains      = lexical_chains
		self.borders             = borders
		self.segments            = segments
		self.segmented_sentences = segmented_sentences

	def execute(self):
		self.write_mecab_result_nodes()
		self.write_lexical_chain_list()
		self.write_border_list()
		self.write_segment_list()
		self.write_segmented_sentences()

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

	def write_border_list(self):
		'''
		分割境界線情報のリストを出力
		'''
		f = open('./log/border_list.log', 'w')

		f.write("before\tafter\tscore\n")
		for sb in self.borders:
			f.write("{}\t{}\t{}\t{}\n".format(sb.cand, sb.before, sb.after, sb.score))
		f.close()

	def write_segment_list(self):

		f = open('./log/segment_list.log', 'w')

		f.write("start\tend\tlength\n")
		for s in self.segments:
			f.write("{}\t{}\t{}\n".format(s.start, s.end, s.length))
		f.close()

	def write_segmented_sentences(self):

		f = open('log/segmented_sentences.log', 'w')

		for sentence in self.segmented_sentences:
			f.write("{}\n=== SEGMENT ===\n\n".format(sentence))
		f.close()