import random
import operator

def model_free_learn(env_map, rwd_map):
	# define epsilon
	epsilon = .5

	# define lr
	lr = .5

	# define gamma
	gamma = .8

	# define n
	n = 10000

	# Step 1: Initialize Q Table
	q_table = {}
	for state in env_map:
		if state not in q_table:
			q_table[state] = {}

		for action in env_map[state]:
			q_table[state][action] = 0;


	# run process n times
	for i in range(0, n):
		# select start ing state randomly
		curr_state = random.choice(list(q_table.keys()))

		print("Selected state: " + curr_state)

		# while path not terminated
		while curr_state != "In":
			# declare action to be taken
			action = ""

			# check if generate random action, or select one with max value
			if random.uniform(0, 1) < epsilon:
				action = random.choice((list(env_map[curr_state].keys())))
				print("Random actions selected: " + action)
			else:
				# find action with highest q value
				maxi = -1
				for possaction in q_table[curr_state]:
					if q_table[curr_state][possaction] > maxi:
						action = possaction
						maxi = q_table[curr_state][action]

				print("Best action selected: " + action)
			
			

			# determine which state we're moving into
			new_state = dictionary_dice_roll(env_map[curr_state][action])

			print("Rolled State: " + new_state)
			
			# if landed in hole, keep goin			
			if new_state == "In":
				curr_state = new_state
				continue

			# determine max Q
			max_q = -1

			for qaction in q_table[new_state]:
				if  q_table[new_state][qaction] > max_q:
					max_q = q_table[new_state][qaction]



			# update q value for given action
			q_table[curr_state][action] = q_table[curr_state][action] + lr * (rwd_map[new_state] + gamma * max_q - q_table[curr_state][action])

			curr_state = new_state


	return q_table



def dictionary_dice_roll(dic):
	rand_val = random.random()
	total = 0
	for k, v in dic.items():
		total += v
		if rand_val <= total:
			return k
	assert False, 'Should not reach this'
