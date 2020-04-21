# Make python file executable
#/usr/bin/env python

# import Model-Free Learning module
import ModelFree

# import Model-Based Learning module
import ModelBased

# Open and read input file
f = open("input.txt", "r")
input_string = f.read()

# split lines in order to more easily handle input
input_string_split = input_string.splitlines()

# declare envrionment map
env_map = {}

for line in input_string_split:
	# split line by forward slash
	split_array = line.split('/')

	# assign variables to split line
	state = split_array[0]
	action = split_array[1]
	new_state = split_array[2]
	p = split_array[3]

	# check if state is in env_map
	if state in env_map:
		# check if action is in state
		if action in env_map[state]:
			# adding probability to action for state
			env_map[state][action][new_state] = float(p)
		else:
			# Add action to state
			env_map[state][action] = {}
			env_map[state][action][new_state] = float(p)
	else:
		# add state to map
		env_map[state] = {}
		env_map[state][action] = {}
		env_map[state][action][new_state] = float(p)

# declare reward dictionary
rwd_dict = {}
rwd_dict["In"] = 1
rwd_dict["Close"] = .8
rwd_dict["Same"] = .6
rwd_dict["Left"] = .5
rwd_dict["Over"] = .3
rwd_dict["Fairway"] = .25
rwd_dict["Ravine"] = .1
