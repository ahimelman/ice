import urllib2
import sys
import requests

netid = sys.argv[1]
desired_sem = sys.argv[2]
url_string = "http://ice.tigerapps.org/php/load.php?q=timetable&id=" + netid + "&key=1417658896989"

r = requests.get(url_string)
res = r.json()
sems = res['data']

id_to_delete = 0
for s in sems:
	if s['term'] == desired_sem:
		id_to_delete = s['id']
		for c in s['courses']:
			print c['dept'], c['num']
