import numpy as np
import pandas as pd
import os

def cal_MA(price):
	total_5 = 0
	total_10 = 0
	for i in range(10):
		if i < 5:
			total_5	+= price[9 - i]
		total_10 += price[9 - i]
	total_5 /= 5
	total_10 /= 10
	return total_5, total_10

def get_act(act):
	act += 1
	prob = table[act]
	while True:
		action = np.random.choice(np.arange(-1, 2), p=[prob[0],prob[1],prob[2]])
		after = status + action
		if after < 2 and after > -2:
			break
	return action

def cal_prob(pd_training):
	for i in range(3):
		for k in range(3):
			table.setdefault(i, []).append(0)
	for i in range(len(pd_training)):
		if i < (len(pd_training) - 1):
			first = pd_training.loc[i, 'action']
			second = pd_training.loc[i+1, 'action']
			table[first + 1][second + 1] += 1

	for i in range(3):
		total = table[i][0] + table[i][1] + table[i][2]
		for k in range(3):
			table[i][k] = table[i][k] / total
	return table

def preprocess():
	train = pd.read_csv(args.training, header=None)
	train['action'] = 0
	for i in range(len(train)):
		if i < (len(train) - 1):
			f_open = train.loc[i, 0]
			s_open = train.loc[i+1, 0]
			diff = s_open - f_open
			if diff > 1:
				train.loc[i, 'action'] = 1
			elif diff < -1:
				train.loc[i, 'action'] = -1
			else:
				train.loc[i, 'action'] = 0
	return train

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
	pd_training = preprocess()
	table = cal_prob(pd_training)
	num_lines = sum(1 for line in open(args.testing))

	count = 0
	close_price = []
	testing_data = open(args.testing, 'r')
	with open(args.output, 'w') as output_file:
		for line in testing_data:
			line = line[:-1]
			line = line.split(',')
			value = []
			for i in range(len(line)):
				value.append(float(line[i]))

			if count == 0:
				close_price.append(value[3])
				yes_ope = value[0]
				output_file.write('1\n')
				status = 1
			elif count < 10:
				close_price.append(value[3])
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
			elif count == num_lines - 1:
				break
			else:
				close_price.pop(0)
				close_price.append(value[3])
				MA5, MA10 = cal_MA(close_price)
				if value[3] > MA5 and MA5 > MA10:
						act = 1
				elif value[3] < MA5 and MA5 < MA10:
						act = -1
				else:
					act = 0

				check = status + act
				if check > 1 or check < -1:
					act = 0
				
				status += act
				output_file.write(str(act))
				output_file.write('\n')
			count += 1
