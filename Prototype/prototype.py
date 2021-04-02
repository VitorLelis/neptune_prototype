from aux_proto import info, check_answer
from aux_proto_2 import update_season

print("\nWelcome to the Prototype of Neptune!\n\nWhat do you wish?")

control = True

"""
The main loop in the prototype.
Based in the option made by the user, the prototype execute a different action until the user chooses to stop. 
"""

while(control):
	print("\n1->Start a new season\n2->Update a previous season\n3->Quit\n")
	start = input()
	try:
		s = int(start)
	except:
		s = 0

	if s in [1,2,3]: 
		if s == 1: info()
		elif s == 2: update_season()

	else: print("\nSorry, I didn't undertand it\n")

	new_op = input("\nDo you want to do something else?[Yes/No]\n")
	control = check_answer(new_op)

print("\nGood luck, swimmer!\n")
quit()
