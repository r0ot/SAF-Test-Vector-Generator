Ian Perry
Extra Credit
Test Vector Generator

To find the shortest number of test vectors to test a given combinational circuit for all possible stuck-at faults, I first needed a way to tell the script what the circuit looked like.  The most logical way to do this to me was with boolean expressions like (a & ~b | (c ^ d)).  The language I adopted to solve this problem was Python because it’s easy and quick.  So, a user can call the script with the given boolean expression in quotes on the command line like this (taking special care to include spaces like in the example above and below):

	python script.py “a | (b & c)"

The script first parses through the expression and makes note of where each variable and symbol are.  A loop of all possible test vectors is entered into next, in the case of the example above, there would be 8 test vectors because there are 3 variables.  Each digit of the test vector is then used to replace the corresponding variable in the expression string and is evaluated using python’s built-in eval function.  A test vector of 101 would yield an expression string like this after replacement:

	“1 | (0 & 1)”

which using eval, evaluates to 1 which is saved as the expected outcome of the current test vector.  Then one variable at a time is replaced by 0 and then 1 and evaluated.  If it evaluates to the opposite of the expected outcome for that test vector, then the fault is detected and made note of.

So far this covers all faults that can occur on the input wires.  The internal wires are the tricky part.  Every symbol in the expression corresponds to a gate and every gate has an output wire that is internal to the circuit.  So in order to check these faults, a symbol and its full left and right side entities needs to be replaced by a 0 or 1 in the expression to check for a fault.  This means that parenthesis need to looked at correctly as a left or right side entity to a symbol.  This was probably the hardest part of the entire assignment.

So once every possible fault was checked for every possible test vector, the smallest number of test vectors was bruteforced.  So, every possible set of test vectors is checked for full coverage and the first one that is found is given to the user.

Here are some test cases:
ianperry$ python script.py "((a & b) | c) & ((~c & d) | ~(a & b))"
Your test vectors are (‘acbd’): 
('0110', '1010', '1011', '1001')

And the one from the lecture slides:
ianperry$ python script.py "a | (b & c)"
Your test vectors are (‘acb’): 
('010', '011', '001', '110')

The second one is very easy to check (it’s already done on the lecture slides).

Overall this program wasn’t too bad.  Once I thought about how I was going to do it for long enough, then it just came down to putting it in code.  Like I said, the hardest part was handling the internal wire faults.  I feel extremely accomplished after completing this assignment.

