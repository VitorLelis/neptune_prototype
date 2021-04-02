"""
Function to write the prototype logo in the file.
"""
def logo_proto_file(file):
	file.write("\n              #")
	file.write("\n             ###")          
	file.write("\n      #     #####     #")   
	file.write("\n     ##    #######    ##")
	file.write("\n    ###      ###      ###")
	file.write("\n   ####      ###      ####")
	file.write("\n     ##      ###      ##")
	file.write("\n     ##      ###      ##")   
	file.write("\n    ####    #####    ####")  
	file.write("\n   #######################") 
	file.write("\n  ######## NEPTUNE ########")
	file.write("\n     ###################")
	file.write("\n        #############")
	file.write("\n           #######")
	file.write("\n             ###")

"""
This function is used to check if the user is writting the proper answer (Yes/No). 
"""
def check_answer(answer):
	ans = answer.lower()

	while((ans != "yes") and (ans != "no")):
		ans = (input("Sorry, I can't understand. Please repeat:\n")).lower()
	
	if ans == "yes": return True

"""
This is the main function of "aux_proto.". 
It's responsible for create a new file (or season as we call here) and write the basic infomartion about the user.
"""
def info():
	control = True

	while(control):
		season_name = input("\nWhat will be the name of this Season?\n")
		try:
			season_handle = open(season_name+".txt" ,"x")
			control = False
		except:
			print("You already have a season named", season_name)
	
	control = True

	while(control):
		athlete = input("What's your name?\n")
		age = input("How old are you?\n")
		stroke = input("Specialty:\n")

		print("\nName:", athlete, "\nAge:", age, "\nSpecialty:", stroke, "\nSeason:", season_name)
		answer1 = input("\nAre the informations correct?[Yes/No]\n")
		if check_answer(answer1): control = False

	answer2 = input("Do you want to set a goal this season?[Yes/No]\n")
	if check_answer(answer2):
		goal = input("What kind of goal do you wish?\n")
	else:
		goal = "No goal estabilished"

	season_handle.write("Name: %s\n" % athlete)
	season_handle.write("Age: %s\n" % age)
	season_handle.write("Specialty: %s\n" % stroke)
	season_handle.write("\nSeason: %s\n" % season_name)
	season_handle.write("\nGoal: %s\n" % goal)
	season_handle.write("\nPractices:\nNo practices yet\n")
	season_handle.write("\nTimes:\nNo times for events yet\n")
	logo_proto_file(season_handle)
	season_handle.close()