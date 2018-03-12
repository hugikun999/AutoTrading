import numpy as np
import pandas as pd
import os

def get_act(act):
	act += 1
	prob = table[act]
	while True:
		action = np.random.choice(np.arange(-1, 2), p=[prob[0],prob[1],prob[2]])
		after = status + action
		if after < 2 and after > -2:
			break
	return action

def cal_prob():
	for i in range(3):
		for k in range(3):
			table.setdefault(i, []).append(0)
	train = pd.read_csv(args.training)
	for i in range(len(train)):
		if i < (len(train) - 1):
			first = train.loc[i, 'action']
			second = train.loc[i+1, 'action']
			table[first + 1][second + 1] += 1

	for i in range(3):
		total = table[i][0] + table[i][1] + table[i][2]
		for k in range(3):
			table[i][k] = table[i][k] / total
	return table

def preprocess():
	train = open(args.training, 'r')
	out = open('header_training.csv', 'w')
	out.write("open,high,low,close\n")
	for line in train:
		out.write(line)
	train.closed
	out.closed
	os.rename('header_training.csv', args.training)
	train = pd.read_csv(args.training)
	train['action'] = 0
	for i in range(len(train)):
		if i < (len(train) - 1):
			f_open = train.at[i, 'open']
			s_open = train.at[i+1, 'open']
			diff = s_open - f_open
			if diff > 1:
				train.loc[i, 'action'] = -1
			elif diff < -1:
				train.loc[i, 'action'] = 1
			else:
				train.loc[i, 'action'] = 0
	train.to_csv(args.training, index=False)

status = 0
table = {}
if __name__ == '__main__':
    # You should not modify this part.
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
	parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
	parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
	args = parser.parse_args()
	preprocess()
	table = cal_prob()
	num_lines = sum(1 for line in open(args.testing))

	count = 0
	total_count = [0,0,0]
	testing_data = open(args.testing, 'r')
	with open(args.output, 'w') as output_file:
		for line in testing_data:
			line = line[:-1]
			line = line.split(',')
			value = []
			for i in range(len(line)):
				value.append(float(line[i]))
			if count == 0:
				yes_ope = value[0]
				output_file.write('1\n')
				status = 1
			elif count == num_lines - 1:
				break
			else:
				ope = value[0]
				diff = ope - yes_ope
				if diff > 1:
					true_act = -1
				elif diff < -1:
					true_act = 1
				else:
					true_act = 0
				act = get_act(true_act)
				status += act
				yes_ope = value[0]
				output_file.write(str(act))
				output_file.write('\n')
			count += 1
			total_count[status] += 1
	print(total_count)
