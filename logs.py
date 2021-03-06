from prettytable import PrettyTable
import xlsxwriter
import json
import requests
import datetime

# key and base url
key="YOUR_KEY"
baseURL="https://api.mailgun.net/v3/YOUR_DOMAIN/"

# some variables
openedSum=0
clickedSum=0
deliveredSum=0
failedSum=0
firstTagSum=0
secondTagSum=0
thirdTagSum=0
fourthTagSum=0
logNum=0

# tags
tag = input("Please enter a tag: ")
tagA = tag + "a"
tagB = tag + "b"
tagC = tag + "c"
tags = [tag,tagA,tagB,tagC]

logType = input("What type of email was this? (Legislative Connection/Top Story): ")
date = input("What date did it go out? Use the format 11.07.2017: ")

# open excel workbooks
logsWorkbook = xlsxwriter.Workbook('./results/Consolidated Logs ' + logType + ' ' + tag + ' ' + date + '.xlsx')

# add a sheet
logsSheet = logsWorkbook.add_worksheet()

# add headers
bold = logsWorkbook.add_format({'bold': True})
logsSheet.write('A1',"Tag",bold)
logsSheet.write('B1',"Event",bold)
logsSheet.write('C1',"Email Address",bold)
logsSheet.write('D1',"City",bold)
logsSheet.write('E1',"State",bold)
logsSheet.write('F1',"Client",bold)
logsSheet.write('G1',"OS",bold)
logsSheet.write('H1',"Device",bold)
logsSheet.write('I1',"Date",bold)

z=1 # list incrementor

# increment through tags a-c
for i in tags:
	lastPage = True
	# original URL
	page = baseURL + "events"

	zz=0

	while lastPage: # each number in this range gets 300 list items
		#table format
		t = PrettyTable(['Tag', 'Event', 'Email', 'City', 'OS', 'Device', 'Date'])

		# api call
		request = requests.get(page, auth=("api", key), params={"limit": 300, "tags":[i]})
		data = request.json()

		# exit loop if it's the page
		if len(data['items']) == 0 and logNum == 0:
			lastPage = False
			firstTagSum = str(zz)
			logNum+=1
			continue

		if len(data['items']) == 0 and logNum == 1:
			lastPage = False
			secondTagSum = str(zz)
			logNum+=1
			continue

		if len(data['items']) == 0 and logNum == 2:
			lastPage = False
			thirdTagSum = str(zz)
			logNum+=1
			continue

		if len(data['items']) == 0 and logNum == 3:
			lastPage = False
			fourthTagSum = str(zz)
			continue

		for j in range(len(data['items'])):
			# reset all the variables
			emailAddress=""
			city=""
			state=""
			tag=""
			event=""
			client=""
			os=""
			device=""

			# next page URL
			page = data['paging']['next']

			# parse data
			try:
				emailAddress=data['items'][j]['recipient']
			except KeyError:
				pass
			try:
				city = data['items'][j]['geolocation']['city']
			except KeyError:
				pass
			try:
				state = data['items'][j]['geolocation']['region']
			except KeyError:
				pass
			try:
				tag = data['items'][j]['tags'][0]
			except KeyError:
				pass
			try:
				event = data['items'][j]['event']
			except KeyError:
				pass
			try:
				client = data['items'][j]['client-info']['client-name']
			except KeyError:
				pass
			try:
				os = data['items'][j]['client-info']['client-os']
			except KeyError:
				pass
			try:
				device = data['items'][j]['client-info']['device-type']
			except KeyError:
				pass
			try:
				time = data['items'][j]['timestamp']
			except KeyError:
				pass

			# sums of totals
			if event == "delivered":
				deliveredSum+=1
			if event == "opened":
				openedSum+=1
			if event == "clicked":
				clickedSum+=1
			if event == "failed":
				failedSum+=1

			# format the time
			formattedTime = datetime.datetime.fromtimestamp(time).strftime('%m/%d/%Y %H:%M:%S')

			# format the city
			cityState = city + ", " + state

			# add a row to the table
			t.add_row([tag,event,emailAddress,cityState,os,device,formattedTime])

			# write to the logs
			logsSheet.write(z,0,tag)
			logsSheet.write(z,1,event)
			logsSheet.write(z,2,emailAddress)
			logsSheet.write(z,3,city)
			logsSheet.write(z,4,state)
			logsSheet.write(z,5,client)
			logsSheet.write(z,6,os)
			logsSheet.write(z,7,device)
			logsSheet.write(z,8,formattedTime)
			z+=1
			zz+=1

		# output during download
		print(t)
		print()
		if logNum == 0:
			print(tags[0] + ": " + str(zz) + " logs downloaded so far...")
		if logNum == 1:
			print(tags[0] + ": " + firstTagSum + " logs downloaded.")
			print(tags[1] + ": " + str(zz) + " logs downloaded so far...")
		if logNum == 2:
			print(tags[0] + ": " + firstTagSum + " logs downloaded.")
			print(tags[1] + ": " + secondTagSum + " logs downloaded.")
			print(tags[2] + ": " + str(zz) + " logs downloaded so far...")
		if logNum == 3:
			print(tags[0] + ": " + firstTagSum + " logs downloaded.")
			print(tags[1] + ": " + secondTagSum + " logs downloaded.")
			print(tags[2] + ": " + thirdTagSum + " logs downloaded.")
			print(tags[3] + ": " + str(zz) + " logs downloaded so far...")


print()
print("Results: ")
print(tags[0] + ": " + firstTagSum + " logs downloaded.")
print(tags[1] + ": " + secondTagSum + " logs downloaded.")
print(tags[2] + ": " + thirdTagSum + " logs downloaded.")
print(tags[3] + ": " + fourthTagSum + " logs downloaded.")
print()
print("Success!")
print(str(z-1) + " logs downloaded!")
print()

# list sums in the excel file
logsSheet.write('K1', 'Delivered',bold)
logsSheet.write('L1', 'Opened',bold)
logsSheet.write('M1', 'Clicked',bold)
logsSheet.write('N1', 'Failed',bold)
logsSheet.write('K2', deliveredSum)
logsSheet.write('L2', openedSum)
logsSheet.write('M2', clickedSum)
logsSheet.write('N2', failedSum)

# close the workbook
logsWorkbook.close()
