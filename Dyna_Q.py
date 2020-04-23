import random
import operator
import copy
import numpy as np

def model_based_learn(env_map, rwd_map):
	# define epsilon
	epsilon = .5

	# define lr
	lr = .5

	# define gamma
	gamma = .8

	# define n
	n = 10000

	# define n_prime
	n_prime = 300

	# define previously observed state
	prev_states = []

	# define previosuly observed actions from states
	prev_actions = {}

	# Step 1: Initialize Q Table
	q_table = {}

	# Step 2: Initialize T Table
	TC = copy.deepcopy(env_map)

	# Step 3: Initialie R Table
	R = {}
	for state in env_map:
		R[state] = {}
		for action in env_map[state]:
			R[state][action] = 0

	for state in TC:
		for action in TC[state]:
			for new_state in TC[state][action]:
				TC[state][action][new_state] = .00000001

	for state in env_map:
		if state not in q_table:
			q_table[state] = {}

		for action in env_map[state]:
			q_table[state][action] = 0;


	# run process n times
	for i in range(0, n):
		# select start ing state randomly
		curr_state = random.choice(list(q_table.keys()))


		# while path not terminated
		while curr_state != "In":
			# declare action to be taken
			action = ""

			# check if generate random action, or select one with max value
			if random.uniform(0, 1) < epsilon:
				action = random.choice((list(env_map[curr_state].keys())))
			else:
				# find action with highest q value
				maxi = -1
				for possaction in q_table[curr_state]:
					if q_table[curr_state][possaction] > maxi:
						action = possaction
						maxi = q_table[curr_state][action]

			
			

			# determine which state we're moving into
			new_state = dictionary_dice_roll(env_map[curr_state][action])

			
			# if landed in hole, keep goin			
			if new_state == "In":
				TC[curr_state][action][new_state] = TC [curr_state][action][new_state] + 1
				curr_state = new_state
				continue

			# determine max Q
			max_q = -1

			for qaction in q_table[new_state]:
				if  q_table[new_state][qaction] > max_q:
					max_q = q_table[new_state][qaction]

			# update estimate for R value
			R[curr_state][action] = ((1 - lr) * R[curr_state][action]) + (lr * rwd_map[new_state])

			# update q value for given action
			q_table[curr_state][action] = q_table[curr_state][action] + lr * (rwd_map[new_state] + gamma * max_q - q_table[curr_state][action])

			# TC increment
			TC[curr_state][action][new_state] = TC [curr_state][action][new_state] + 1

			# DYNA-Q			
			for i in range(0, n_prime):
				prev_states.append(curr_state)
				if curr_state not in prev_actions:
					prev_actions[curr_state] = []
				
				prev_actions[curr_state].append(action)
				
				# randomly select state and action
				rand_state = random.choice(prev_states)
				rand_action = random.choice(prev_actions[rand_state])

				# select new state based on probability model
				new_state_prime = dictionary_dice_roll(TC[rand_state][rand_action])
				reward_prime = R[rand_state][rand_action]


				if new_state_prime == "In":
					continue

				max_q_prime = -1
				for qaction in q_table[new_state_prime]:
					if q_table[new_state_prime][qaction] > max_q_prime:
						max_q_prime = q_table[new_state_prime][qaction]

				q_table[rand_state][rand_action] = q_table[rand_state][rand_action] + lr * (R[rand_state][rand_action] + gamma * max_q_prime - q_table[rand_state][rand_action])
				
			
			curr_state = new_state


	print("Final transition model")
	for state in TC:
		print("State: " + state)
		for action in TC[state]:
			print("    Action: " + action)
			for new_state in TC[state][action]:
				print("        " + new_state + " occurred " + str(TC[state][action][new_state]) + " times.")

	return q_table



def dictionary_dice_roll(dic):
	# get total value of dice
	total = 0
	for k, v in dic.items():
		total = total + v

	rand_val = random.random() * float(total)
	total = 0
	for k, v in dic.items():
		total += v
		if rand_val <= total:
			return k
	assert False, 'Should not reach this'
