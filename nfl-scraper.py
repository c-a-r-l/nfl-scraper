import time
import requests
import urllib.request
import pickle
import csv

def openURL(string):
	url = 'http://' + string
	cur = urllib.request.urlopen(url)
	return cur

class Log:
	def __init__(self):
		self.list = []

	def log(self, string):
		self.list.append(string)
		print(string + 'logged!')

	def returnList(self):
		return self.list



log = []
coachURL = []
coachDATA = []

#for football coaching
cur = openURL('www.pro-football-reference.com/coaches/')
for line in cur:
	line = line.decode('utf-8')
	n = line.find('><a href="/coach')
	if n != -1:
		if line[n+30] == '"':
			coachURL.append(line[n+10:n+30])

#coach URL list of filled with strings of this form: "/coaches/FoxxJo0.htm"
#All 485 coaching records since 1920

for coach in coachURL:
	indiv = []
	print('opening' + coach)
	cur = openURL('www.pro-football-reference.com' + coach)
	count = 1
	for line in cur:
		line = line.decode('utf-8')
		if line.find('"keywords"') != -1:
			m = line.find('"keywords"') + 20
			n = line.find('">')
			name = line[m:n]

		#populating the actual data
		if line.find('"year_id" ><a href="/years/') != -1:
			datapoint = []
			n = line.find('/years/') + 7
			datapoint.append(line[n:n+4])

			n = line.find('"age"') + 7
			datapoint.append(line[n:n+2])

			n = line.find('"wins"') + 8
			m = line[n:n+4].find('<')
			datapoint.append(line[n:n+m])

			n = line.find('"losses"') + 10
			m = line[n:n+4].find('<')
			datapoint.append(line[n:n+m])
			datapoint.append(name)
			datapoint.append(count)
			count += 1

			indiv.append(datapoint)

		if line.find('Team ranks') != -1:
			coachDATA.append(indiv)
			break

#coachDATA[i] <- the individual coach list
#coachDATA[i][j][0] <- coach age in a specific year
#coachDATA[i][j][1] <- wins in a specific year
#coachDATA[i][j][2] <- losses in a specific year
#coachDATA[i][j][3] <- name of coach
#coachDATA[i][j][4] <- years of coach


print(coachDATA[0][0])
print(coachDATA[0][1])

#with open("store.txt", "wb") as fp:
#	pickle.dump(coachDATA, fp)


with open('test3.csv', 'w') as f:
	writer = csv.writer(f)
	for i in coachDATA:
		writer.writerows(j for j in i)