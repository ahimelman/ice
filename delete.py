# This script belongs to Samuel Jerome and Aaron Himelman, and should not be 
# used without this disclaimer commented on top. We really like our script,
# and feel we deserve credit for the bounds checking at the very least.

import urllib2
import sys
import requests
import re
import random

p = re.compile('[SF](10-11|11-12|12-13|13-14|14-15)')

def delete_course(tid, course):
	course = course.lstrip()
	delete_url = "http://ice.tigerapps.org/php/store.php?q=t_course&remove=true&tid=" + tid + "&data=" + course.replace(' ', '%20')
	requests.get(delete_url)

def add_course(tid, course):
	course = course.lstrip()
	add_url = "http://ice.tigerapps.org/php/store.php?q=t_course&tid=" + tid + "&data=" + course.replace(' ', '%20') + "&indices=0%20&color="+ str(int(random.random()*14))
	requests.get(add_url)

def add_semester(username, semester):
	username = username.lstrip()
	semester = semester.lstrip()
	add_url = "http://ice.tigerapps.org/php/store.php?q=timetable&id=" + username + "&data=Timetable&term=" + semester
	requests.get(add_url)

def delete_semester(username, tid, semester):
	username = username.lstrip()
	semester = semester.lstrip()

	delete_url = "http://ice.tigerapps.org/php/store.php?q=timetable&id=" + username + "&remove=true&tid="+ str(tid)

	requests.get(delete_url)

while True:
	netid = raw_input("Please enter netid: ")
	if netid:
		break

while True:
	inp = raw_input("Would you like to add a semester? [yes|no]: ")
	if inp != 'yes':
		break
	semester_to_add = raw_input("Please enter semester to add or blank if not (e.g. S14-15, F13-14): ")
	if semester_to_add == '':
		break
	if p.match(semester_to_add):
		add_semester(netid, semester_to_add)
		break

while True:
	desired_sem = raw_input("Please enter semester to view (e.g. S14-15, F13-14): ")
	if desired_sem == '':
		desired_sem = 'S14-15'
		break

	if p.match(desired_sem):
		break

url_string = "http://ice.tigerapps.org/php/load.php?q=timetable&id=" + netid

r = requests.get(url_string)
res = r.json()
sems = res['data']

semesters = []

for s in sems:
	if s['term'] == desired_sem:
		id_to_delete = s['id']
		semesters.append(id_to_delete)
		for c in s['courses']:
			print c['dept'], c['num']

		delete = raw_input("Would you like to delete this semester? [yes|no]: ")
		if delete == "yes":
			delete_semester(netid, id_to_delete, desired_sem)
			continue

		choose_course = raw_input("Please enter comma separated courses to delete (e.g: COS 448, ECO 100): ")
		if choose_course == '*':
			for c in s['courses']:
				delete_course(id_to_delete, c['dept'] + " " + c['num'])
		else:
			for c in choose_course.split(','):
				delete_course(id_to_delete, c)

courses = raw_input("Please enter comma separated courses to add (e.g: COS 448, ECO 100): ")

for tid in  semesters:
	for c in courses.split(','):
		add_course(tid, c)

