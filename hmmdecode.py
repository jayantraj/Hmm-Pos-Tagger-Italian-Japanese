import sys
from collections import defaultdict

class hmm_decode:
	def __init__(self,tags_dictionary,transition_matrix,emission_matrix,vocabulary):
		self.tags_dictionary = tags_dictionary
		self.transition_matrix = transition_matrix
		self.emission_matrix = emission_matrix
		self.vocabulary = vocabulary
		self.viterbi = defaultdict(int)
		self.back_pointer = defaultdict(int)
		self.starting_state = '220222__s!@r+__220222'
		self.ending_state = '220222__e^d__220222'
		self.current_tag = None


	def get_maximum_probability(self,viterbi_path):
		maximum_probability,prev_pointer = float('-inf'),None

		for s in viterbi_path:
			if maximum_probability < viterbi_path[s]+self.transition_matrix[s][self.current_tag]:
				maximum_probability,prev_pointer =  viterbi_path[s]+self.transition_matrix[s][self.current_tag],s	
		return maximum_probability, prev_pointer


	def viterbi_algorithm(self,file_path):
		file = open(file_path,'r',encoding = 'UTF-8')
		f1 = open('hmmoutput.txt','w',encoding = 'UTF-8')
		data = file.readlines()
		for line_ in data:
			#print(line_)
			self.viterbi = defaultdict(int)
			self.back_pointer = defaultdict(int)
			final_probability,final_tag,output_token,predicted_tag = float('-inf'),None,[],None
			tokens = line_.strip().split()
			n= len(tokens)

			self.viterbi[0],self.back_pointer[0],first_word={},{},tokens[0]
			for tag in self.tags_dictionary:

				if first_word in self.vocabulary and first_word in self.emission_matrix[tag]:
					#print(first_word,tag)
					#print(self.transition_matrix[self.starting_state])
					#print(self.emission_matrix[tag])
					self.viterbi[0][tag] = self.transition_matrix[self.starting_state][tag]+self.emission_matrix[tag][first_word]
					self.back_pointer[0][tag] = self.starting_state
				elif first_word not in self.vocabulary:
					self.viterbi[0][tag] = self.transition_matrix[self.starting_state][tag]
					self.back_pointer[0][tag] = self.starting_state

			# print(self.viterbi)
			# print('\n\n')
			# print(self.back_pointer)
			for i in range(1,n):
				self.viterbi[i],self.back_pointer[i]={},{}
				for tag in self.tags_dictionary:
					if tokens[i] in self.vocabulary and tokens[i] in self.emission_matrix[tag]:
						self.current_tag=tag
						self.viterbi[i][tag],self.back_pointer[i][tag]=self.get_maximum_probability(self.viterbi[i-1])
						self.viterbi[i][tag]+=self.emission_matrix[tag][tokens[i]]
					elif tokens[i] not in self.vocabulary:
						self.current_tag=tag
						self.viterbi[i][tag],self.back_pointer[i][tag]=self.get_maximum_probability(self.viterbi[i-1])

			# print(self.viterbi)
			# print(self.back_pointer)
			# print('\n\n')

			for tag in self.viterbi[n-1]:
				if final_probability < self.transition_matrix[tag][self.ending_state]+self.viterbi[n-1][tag]:
					final_probability = self.transition_matrix[tag][self.ending_state]+self.viterbi[n-1][tag]
					final_tag = tag
					
			predicted_tag = final_tag
			# print(predicted)
			# print('\n\n')
			for i in range(n- 1,-1,-1):
				temp = tokens[i]+'/'+predicted_tag
				#print('temp ',temp)
				#print("{}/{}".format(tokens[i], predicted_tag))
				#output_token.append("{}/{}".format(tokens[i], predicted))
				output_token.append(temp)
				predicted_tag = self.back_pointer[i][predicted_tag]
			
			output_token = output_token[::-1]
			result = " ".join(output_token)
			f1.write(result)
			f1.write('\n')
			#print(result)
			#print('\n\n')
		file.close()
		f1.close()
			


def main():
	file=open('hmmmodel.txt','r',encoding = 'UTF-8')
	tags_dictionary = eval(file.readline())
	transition_matrix= eval(file.readline())
	emission_matrix=eval(file.readline())
	vocabulary=eval(file.readline())

	# print('tags_dictionary ',tags_dictionary)
	# print('transition_matrix ',transition_matrix)
	# print('emission_matrix ',emission_matrix)
	# print('vocabulary ',vocabulary)

	file.close()

	input_path = sys.argv[1]

	hmm = hmm_decode(tags_dictionary,transition_matrix,emission_matrix,vocabulary)
	
	hmm.viterbi_algorithm(input_path)
main()

