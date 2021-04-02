import re
from aux_proto import check_answer, logo_proto_file

"""
The function "save_info" creates 3 dictionary containing different types of information:
-> The basic info about the user(Name, Age, etc)
-> The practices info (Distance in yards or meters and comments about the practice)
-> The times info (Best time in each event)
"""
def save_info(handle):
	basic_info = {}
	practice_info = {}
	times_info = {}

	basic = ["Name", "Age", "Specialty", "Season", "Goal"]

	for line in handle:
		if any(map(line.startswith, basic)):
			nline = re.split(": |\n", line)
			basic_info[nline[0]] = nline[1]

		elif line.startswith("#"):
			nline = re.split(": |; |\n", line)
			practice_info[nline[0]] = [nline[1],nline[2]]

		elif line.startswith("->"):
			event = re.split("->|:", line)[1]
			all_times = []

		elif line.startswith("("):
			time = line[4:].rstrip()
			all_times.append(time)
			times_info[event] = all_times

	return [basic_info, practice_info, times_info]

"""
Checks if the distance passed as argument it's in the correct format.
Ex.: 1200m or 1450yds
"""
def check_distance(distance):
	answer = True

	if "m" or "yds" in distance:
		distance_number = distance.strip("m|yds")
		try:
			int(distance_number)
		except:
			answer = False

	else: answer = False

	return answer

"""
This function calculate the total distance by adding all the distances(first values of the keys).
It also convert meters to yards and vice-versa.
"""
def total_distance(practice_info):
	total_m = 0

	for train in practice_info.keys():
		current = practice_info[train][0]
		if "m" in current:
			current_int = int(current.strip("m"))
		else:
			current_int = int(current.strip("yds"))
			current_int *= 0.9144

		total_m += int(current_int)

	total_yds = int(total_m * 1.0936)

	return (total_m,total_yds)

"""
This function is responsible to update the dictionary "practice_info" with new practices.
It also uses other functions like "check_distance" to be certain there won't be distances in invalid formats.
The steps of updating are:
-> Get the distance and the respective unit
-> Be certain that the format is correct by using a "while loop" with "check_distance" as the condition
-> Get te practice number and a summary about the same
-> Repeat the whole process until the user is done 
"""
def new_practice(practice_info):
	new_op = input("\nDo you want to record a new practice?[Yes/No]\n")
	control = check_answer(new_op)

	while(control):
		valid_distance = False
		while(not valid_distance):
			distance = input("\nWhat is the total distance in this practice?(m/yds)\n")
			valid_distance = check_distance(distance)
			if not valid_distance: print("\nNot the correct format\n")

		practice_number = 1
		for i in practice_info.keys(): practice_number += 1
		
		summary = input("\nWrite a summary about the practice\n")
		
		current_practice = "#" + str(practice_number)
		practice_info[current_practice] = [distance,summary]

		new_op = input("\nDo you want to record a new practice?[Yes/No]\n")
		control = check_answer(new_op)
"""
This fuction checks if the time is in the correct format.
Ex.: 12.98 (seconds), 01:23.98 (minutes) or 02:34:45.67(hours)
"""
def check_time(time):
	
	if len(time) == 5:
		answer = bool(re.match("[0-5][0-9][.][0-9][0-9]",time))
	
	elif len(time) == 8:
		answer = bool(re.match("[0-5][0-9][:][0-5][0-9][.][0-9][0-9]",time))
	
	elif len(time) == 11:
		answer = bool(re.match("[0-9][0-9][:][0-5][0-9][:][0-5][0-9][.][0-9][0-9]",time))
	
	else: answer = False

	return answer

"""
Function responsible to update the dictionary "times_info"
Just like "check_distance" in "new_practice", "check_time" is being used here to be sure the time's format is correct
The steps in this one are:
-> Get the event which time will be recorded
-> Loop with "check_time" as condition to guarantee the correct format
-> Creates a list with the times of the event and put them in order (fastest to slowest)
-> Repeat until the user stops
"""
def new_time(times_info):
	new_op = input("\nDo you want to record a new time?[Yes/No]\n")
	control = check_answer(new_op)
	
	while(control):
		event = input("\nWhich event is going to be recorded?\n")
		valid_time = False
		while(not valid_time):
			time = input("\nWhat is the time?\n")
			valid_time = check_time(time)
			if not valid_time: print("\nNot the correct format\n")
		
		all_times = times_info.get(event, [])
		all_times.append(time)

		times_info[event] = all_times
		times_info[event].sort(key = lambda time: (len(time), time))
		
		new_op = input("\nDo you want to record a new time?[Yes/No]\n")
		control = check_answer(new_op)
"""
It writes the information in "basic_info" in the file
"""
def write_basic_info(handle, basic_info):
	handle.write("Name: %s\n" % basic_info["Name"])
	handle.write("Age: %s\n" % basic_info["Age"])
	handle.write("Specialty: %s\n" % basic_info["Specialty"])
	handle.write("\nSeason: %s\n" % basic_info["Season"])
	handle.write("\nGoal: %s\n" % basic_info["Goal"])
"""
It writes the information in "practice_info" in the file
"""
def write_practice_info(handle, practice_info):
	handle.write("\nPractices:\n\n")

	for prac_number, prac_info in practice_info.items():
		sentence = prac_number+": "+prac_info[0]+"; "+prac_info[1]+"\n"
		handle.write(sentence)

	(total_m, total_yds) = total_distance(practice_info)
	sentence = str(total_m)+"m or "+str(total_yds)+"yds\n"
	handle.write("\nTotal distance: "+sentence)
"""
It writes the information in "times_info" in the file
"""
def write_times_info(handle, times_info):
	handle.write("\nTimes:\n\n")

	for event, times in times_info.items():
		handle.write("->"+event+":\n")
		count = 1
		
		for i in times:
			sentence ="("+str(count)+") "+i+"\n"
			handle.write(sentence)
			count += 1

		handle.write("\n")
"""
This is the main function in "aux_proto_2"
It's responsible to call the other functions in order to update the whole file
In order to update the file these steps are taken:
-> Open the file to read and save the information using "saving_info"
-> Call the fucntions "new_practice" and "new_time" to update them
-> Reopen the file but to rewrite the information this time
-> Call the functions that write in the file
-> Close the file 
"""
def update_season():
	control = True

	while(control):
		season_name = input("\nWhich season should we update?\n")
		try:
			season_handle = open(season_name+".txt")
			control = False
		except:
			print("\nThere is no season named", sname)

	(basic_info, practice_info, times_info) = save_info(season_handle)
	season_handle.close()

	new_practice(practice_info)
	new_time(times_info)

	new_season_handle = open(season_name+".txt", "w")
	write_basic_info(new_season_handle, basic_info)
	write_practice_info(new_season_handle, practice_info)
	write_times_info(new_season_handle, times_info)
	logo_proto_file(new_season_handle)
	new_season_handle.close()
