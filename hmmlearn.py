import sys
from collections import defaultdict
import math


class hmm_training:
	def __init__(self):
		self.tags_dictionary = defaultdict(int)
		#self.start_states_pi = defaultdict(int)
		self.transition_matrix = defaultdict(dict)
		self.emission_matrix = defaultdict(dict)
		self.vocabulary = defaultdict(int)
		self.total_start_states = 0
		self.uniq_num_of_words_in_corpus = 0
		self.uniq_num_of_tags_in_corpus = 0
		self.starting_state = '220222__s!@r+__220222'
		self.ending_state = '220222__e^d__220222'

	def update_the_counts(self,file_path):
		file = open(file_path,'r',encoding = 'UTF-8')
		data = file.readlines()
		for line_ in data:
			# check if it is needed to lowercase the data.
			tokens = line_.strip().split()
			#print(tokens)
			prev_tag = None
			for token in tokens:
				word,current_tag = token.rsplit('/',1)
				if not prev_tag:
					#self.start_states_pi[current_tag]+=1
					self.tags_dictionary[self.starting_state]+=1
					if current_tag not in self.transition_matrix[self.starting_state]:
						self.transition_matrix[self.starting_state][current_tag]=1
					else:
						self.transition_matrix[self.starting_state][current_tag]+=1
					
				else:
					if current_tag not in self.transition_matrix[prev_tag]:
						self.transition_matrix[prev_tag][current_tag]=1
					else:
						self.transition_matrix[prev_tag][current_tag]+=1
				if word not in self.emission_matrix[current_tag]:
					self.emission_matrix[current_tag][word]=1
				else:
					self.emission_matrix[current_tag][word]+=1

				self.vocabulary[word]+=1
				self.tags_dictionary[current_tag]+=1
				prev_tag = current_tag

			self.tags_dictionary[self.ending_state]+=1
			if self.ending_state not in self.transition_matrix[current_tag]:

				self.transition_matrix[current_tag][self.ending_state]=1
			else:
				self.transition_matrix[current_tag][self.ending_state]+=1
			
		# print('Tags dictionary ',self.tags_dictionary)
		# print('Start State ',self.start_states_pi)
		# print('Transition matrix ',self.transition_matrix)
		# print('Emission matrix ',self.emission_matrix)
		# print('Vocabulary ',self.vocabulary)

		file.close()

	def get_probabilities(self):
		self.total_start_states = self.tags_dictionary[self.starting_state]
		self.uniq_num_of_words_in_corpus = len(self.vocabulary)
		self.uniq_num_of_tags_in_corpus = len(self.tags_dictionary)
		#for start_state in self.start_states_pi:
			#self.start_states_pi[start_state]/=self.total_start_states

		
		for tag in self.tags_dictionary:
			for trans_matrix_tag in self.transition_matrix:
				if tag not in self.transition_matrix[trans_matrix_tag]:
					self.transition_matrix[trans_matrix_tag][tag]=1
				else:
					self.transition_matrix[trans_matrix_tag][tag]+=1
			
			for trans_matrix_tag in self.transition_matrix:
				self.transition_matrix[trans_matrix_tag][tag] = math.log(self.transition_matrix[trans_matrix_tag][tag]/(self.tags_dictionary[trans_matrix_tag]+self.uniq_num_of_tags_in_corpus))

		# no smoothing for emission matrix
		for tag in self.emission_matrix:
			count = sum(self.emission_matrix[tag].values())
			for word in self.emission_matrix[tag]:
				self.emission_matrix[tag][word]=math.log(self.emission_matrix[tag][word]/count)


		#for i in self.emission_matrix:
			#print(sum(self.emission_matrix[i].values()))
		#for i in self.transition_matrix:
			#print(sum(self.transition_matrix[i].values()))

		self.tags_dictionary.pop(self.starting_state)
		self.tags_dictionary.pop(self.ending_state)
		file = open('hmmmodel.txt','w')
		l_index = str(self.tags_dictionary).index('{')
		r_index = str(self.tags_dictionary).rindex(')')
		file.write(str(self.tags_dictionary)[l_index:r_index])
		file.write('\n')
		#file.write(str(self.start_states_pi))
		#file.write('\n')
		l_index = str(self.transition_matrix).index('{')
		r_index = str(self.transition_matrix).rindex(')')
		file.write(str(self.transition_matrix)[l_index:r_index])
		file.write('\n')
		l_index = str(self.emission_matrix).index('{')
		r_index = str(self.emission_matrix).rindex(')')
		file.write(str(self.emission_matrix)[l_index:r_index])
		file.write('\n')
		l_index = str(self.vocabulary).index('{')
		r_index = str(self.vocabulary).rindex(')')
		file.write(str(self.vocabulary)[l_index:r_index])
		file.close()

		# print('Start State ',self.start_states_pi)
		# print('All Tags ',self.tags_dictionary)
		# print('\n\n')
		# print('Transition matrix ',self.transition_matrix)
		# print('\n\n')
		# print('Emission matrix ',self.emission_matrix)
		# print('\n\n')
		# print('vocabulary ',self.vocabulary)
		# print(self.uniq_num_of_words_in_corpus)
		# print(self.uniq_num_of_tags_in_corpus)

def main():
	input_path = sys.argv[1]
	hmm = hmm_training()
	hmm.update_the_counts(input_path)
	hmm.get_probabilities()
main()