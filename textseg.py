# coding: utf-8

import argparse
from sentence import Sentence
from log import Log

class TextSeg:
	def __init__(self):
		'''
		引数をargparseで解析しオブジェクトに追加
		'''
		parser = argparse.ArgumentParser(description='This script is to segment text using LCseg.')
		# file parameter
		parser.add_argument('-i', '--input_file_path',
                            default="./dat/sample.dat",
                            help='File path of input text you want to segment.')
		# text segmentation's parameter
		parser.add_argument('-d', '--dic',
                            default="",
                            help='Dictionary path for MeCab')

		# ...
		self.options = parser.parse_args()
		if self.options.dic != "":
			self.options.dic = "-d " + self.options.dic



	def read_input(self, input_file_path):
		sentences = []
		sentence_num = 0
		f = open(input_file_path, 'r')
		for readline in f.readlines():
			readline = readline.rstrip()
			if readline != '':
				s = Sentence()
				s.surf   = readline
				s.num    = sentence_num
				s.morphs = s.make_mecab_result_nodes(self.options.dic)
				sentences.append(s)
		f.close()
		return sentences


	def LCseg(self):
		sentences = self.read_input(self.options.input_file_path)


		log = Log(sentences)
		log.execute()



if __name__ == '__main__':
	ts = TextSeg()
	ts.LCseg()