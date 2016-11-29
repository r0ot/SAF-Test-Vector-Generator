import argparse
import string
import pprint
import itertools
import sys

#symbols
#{'&': [2, 6], '|': [4, 10]}
#vars
#{'a': [1, 7]}

#stucktest
#{"000": ["a0", "b1", "0&1"]}
#stuckat
#{"a0": ["000", "010"]}

def main():
	symbols = {}
	vars = {}
	stucktest = {}
	stuckat = {}
	pos = 0
	# loop through all the characters of the expression
	for letter in args.expression:
		# if the character is special (variable of symbol)
		if letter in ("|&^" + string.ascii_lowercase + string.ascii_uppercase):
			try:
				# append it's location to the correct dictionary (var or symbol)
				if letter in (string.ascii_lowercase + string.ascii_uppercase):
					vars[letter].append(pos)
				else:
					symbols[letter].append(pos)
			except KeyError, e:
				# or start a new entry
				if letter in (string.ascii_lowercase + string.ascii_uppercase):
					vars[letter] = [pos]
				else:
					symbols[letter] = [pos]
		pos += 1

	# loop through all the possible test vectors
	for i in range (2 ** len(vars)):
		exp = args.expression
		# replace each variable with the corresponding test vector digit
		for j in range(len(vars.keys())):
			exp = exp.replace(vars.keys()[j], "" + get_bin(i,len(vars))[j])
		# evaluate the expression to get the expected outcome for this test vector
		expected = eval(exp)
		# go through each variable, check its faults
		for var in vars.keys():
			exp = args.expression
			exp = exp.replace(var, '0')
			for j in range(len(vars.keys())):
				if var != vars.keys()[j]:
					exp = exp.replace(vars.keys()[j], "" + get_bin(i,len(vars))[j])
			if expected != eval(exp):
				if get_bin(i,len(vars)) not in stucktest.keys():
					stucktest[get_bin(i,len(vars))] = [var + '0']
				else:
					stucktest[get_bin(i,len(vars))].append(var + '0')
				if var + '0' not in stuckat.keys():
					stuckat[var + '0'] = [get_bin(i,len(vars))]
				else:
					stuckat[var + '0'].append(get_bin(i,len(vars)))
			exp = args.expression
			exp = exp.replace(var, '1')
			for j in range(len(vars.keys())):
				if var != vars.keys()[j]:
					exp = exp.replace(vars.keys()[j], "" + get_bin(i,len(vars))[j])
			if expected != eval(exp):
				if get_bin(i,len(vars)) not in stucktest.keys():
					stucktest[get_bin(i,len(vars))] = [var + '1']
				else:
					stucktest[get_bin(i,len(vars))].append(var + '1')
				if var + '1' not in stuckat.keys():
					stuckat[var + '1'] = [get_bin(i,len(vars))]
				else:
					stuckat[var + '1'].append(get_bin(i,len(vars)))

		# go through each type of symbol because each corresponds to an internal signal
		for sym in symbols.keys():
			# go through each specific symbol
			index = 0
			for place in symbols[sym]:
				opens = 0
				closes = 0
				exp = args.expression
				spot = place-1
				letter = exp[spot]
				# find the left closest variable or end parenthesis
				while spot > 0 and (letter not in vars.keys() or opens != 0) and (opens != closes or opens == 0):
					spot -= 1
					letter = exp[spot]
					if letter == ')':
						opens += 1
					elif letter == '(':
						closes += 1
				leftspot = spot

				opens = 0
				closes = 0
				exp = args.expression
				spot = place+1
				letter = exp[spot]
				# find the right closest variable or end parenthesis
				while spot < len(exp)-1 and (letter not in vars.keys() or opens != 0) and (opens != closes or opens == 0):
					spot += 1
					letter = exp[spot]
					if letter == '(':
						opens += 1
					elif letter == ')':
						closes += 1
				rightspot = spot + 1

				exp = args.expression
				# replace current internal signal with '0'
				exp = exp.replace(exp[leftspot:rightspot], '0')
				# now replace rest of vars with inputs
				for j in range(len(vars.keys())):
					exp = exp.replace(vars.keys()[j], "" + get_bin(i,len(vars))[j])
				# if expected isn't the same, we found a testable input
				if expected != eval(exp):
					if get_bin(i,len(vars)) not in stucktest.keys():
						stucktest[get_bin(i,len(vars))] = [str(index) + sym + '0']
					else:
						stucktest[get_bin(i,len(vars))].append(str(index) + sym + '0')
					if sym + '0' not in stuckat.keys():
						stuckat[str(index) + sym + '0'] = [get_bin(i,len(vars))]
					else:
						stuckat[str(index) + sym + '0'].append(get_bin(i,len(vars)))

				exp = args.expression
				# replace current internal signal with '1'
				exp = exp.replace(exp[leftspot:rightspot], '1')
				# now replace rest of vars with inputs
				for j in range(len(vars.keys())):
					exp = exp.replace(vars.keys()[j], "" + get_bin(i,len(vars))[j])
				# if expected isn't the same, we found a testable input
				if expected != eval(exp):
					if get_bin(i,len(vars)) not in stucktest.keys():
						stucktest[get_bin(i,len(vars))] = [str(index) + sym + '1']
					else:
						stucktest[get_bin(i,len(vars))].append(str(index) + sym + '1')
					if sym + '1' not in stuckat.keys():
						stuckat[str(index) + sym + '1'] = [get_bin(i,len(vars))]
					else:
						stuckat[str(index) + sym + '1'].append(get_bin(i,len(vars)))
				index += 1

	# pprint.pprint(stucktest, width=20)

	check = {}
	done = True
	# iterate through each possible number of test vectors (from t to all)
	for i in range (1, len(stucktest)+1):
		# iterate through every combination of test vectors of that length
		for combo in itertools.combinations(stucktest.keys(),i):
			# clear check list
			for key in stuckat.keys():
				check[key] = False
			# iterate through those test vectors
			for test in combo:
				# iterate through the test cases that this test vector checks
				for validated in stucktest[test]:
					check[validated] = True
			done = True
			# find out if ALL faults can be detected with this set of test vectors
			for key in check.keys():
				if not check[key]:
					done = False
			if done:
				break
		if done:
			break

	if done:
		print "Your test vectors are:"
		print str(''.join(sorted(vars.keys())))
		for vector in combo:
			betterVec = ""
			for letter in sorted(vars.keys()):
				pos = vars.keys().index(letter)
				betterVec += vector[pos]
			print betterVec
	else:
		print "Error"

# wish I could've just used bin(num) but it only gives the minimum
# number of bits that the number requires.  So this function just
# 0-extends the bit string for a given number of total bits
def get_bin(x, l):
	ret = ""
	for i in range (l - len(bin(x)[2:])):
		ret += "0"
	ret += bin(x)[2:]
	return ret

parser = argparse.ArgumentParser()
parser.add_argument("expression", help="The boolean expression to test")
args = parser.parse_args()
if __name__ == "__main__":
	main()