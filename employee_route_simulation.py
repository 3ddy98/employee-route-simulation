import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import googlemaps
import random
import pprint
import json
import logging 
import sys 
import math

min_time_in_store = 3600 #in seconds
max_time_in_store = 3600+1800 #in seconds
max_time_on_clock = 28800#in seconds
lunch_time = 1800 #in seconds

max_distance_to_next_location = 100 #in miles
gmaps = googlemaps.Client(key='')


class PrintCaptureFilter(logging.Filter):
    def filter(self, record):
        return record.msg == sys.stdout.write.__doc__
class Employee:
	def __init__(self,id):
		self.id = id
		self.time_driving = 0
		self.time_in_store = 0
		self.miles_driven = 0
		self.pay_rate = 25/3600
		self.mile_rate = .67
		self.on_clock_time = 0
		self.labor_payroll = 0
		self.miles_payroll = 0
		self.payroll = 0
		self.stores_visited	= []
		self.stops = 0

	def __iter__(self):
		return iter([self.id,self.time_driving,self.time_in_store,self.miles_driven,self.pay_rate,self.mile_rate,self.on_clock_time,self.labor_payroll,self.miles_payroll,self.stops])

	def calculatePayroll(self):
		self.labor_payroll = (self.pay_rate*(self.time_driving+self.time_in_store))
		self.miles_payroll = (self.mile_rate*self.miles_driven)
		self.payroll = self.labor_payroll + self.miles_payroll

	def printReport(self):
		original_stdout = sys.stdout
		with open('output.txt', 'a') as f:
			sys.stdout = f
			print("ID: ",self.id)
			print("Hours Driving: ",self.time_driving/3600) #conversion sec to Hr
			print("Hours in Store: ",self.time_in_store/3600) #conversion sec to Hr
			print("Total Hours on Clock: ",self.on_clock_time/3600) #conversion sec to Hr
			print("Miles Driven: ",self.miles_driven) #conversion m to Mi
			print("Miles Paid: $",self.miles_payroll)
			print("Labor Paid: $",self.labor_payroll)
			print("Total Paid: $", self.payroll)
			print("Total Stops: ",self.stops)
			print("Stores Visited:\n ",self.stores_visited.to_string())
			print(3*'\n')
		sys.stdout = original_stdout

	def updateOnClockTime(self):
		self.on_clock_time = self.time_driving + self.time_in_store - lunch_time

	def addDrivetime(self,time_driven):
		self.time_driving = self.time_driving + time_driven
		self.updateOnClockTime()
		self.calculatePayroll()

	def addStoretime(self,time_in_store):
		self.time_in_store = self.time_in_store + time_in_store
		self.updateOnClockTime()
		self.calculatePayroll()

	def logMiles(self,miles_driven):
		miles_driven = miles_driven/1609 #m to miles
		self.miles_driven = self.miles_driven + miles_driven
		self.updateOnClockTime()
		self.calculatePayroll()

def findNextNearest(cal_locations,orig_lat,orig_lng,org_index):
	cal_locations_cp = cal_locations.copy()
	cal_locations_cp = cal_locations_cp.drop(index=int(org_index))
	cal_locations_cp['del_lat'] = cal_locations_cp['lat'] - orig_lat
	cal_locations_cp['del_lon'] = cal_locations_cp['lon'] - orig_lng
	cal_locations_cp['dist'] = (cal_locations_cp['del_lat']**2 + cal_locations_cp['del_lon']**2)**.5
	min_row = cal_locations_cp.loc[cal_locations_cp['dist'] == cal_locations_cp['dist'].min()]
	dest_index = min_row.index[0]
	
	return dest_index
	
def main():
	total_payroll = 0
	'''#logger setup
	logger = logging.getLogger()
	logger.addFilter(PrintCaptureFilter())
	# Set up logging to a file
	logging.basicConfig(filename='report.txt', level=logging.INFO)'''

	#start program
	data = pd.read_csv('geocoded_by_geoapify-9_24_2024, 10_22_41 AM.csv')
	cal_locations = data[data['state']=='California']
	fig,ax = plt.subplots(1,1)
	ax.scatter(cal_locations['lon'],cal_locations['lat'])

	cal_locations = cal_locations.sort_values(by='lon')
	locations_shape = cal_locations.shape

	emp_id = 1
	temp_emp = Employee(emp_id)
	employees = []
	stores_visited = {'lat':[],'lon':[],'Start':[],'End':[]}
	df_stores = []
	x = 0
	stops = 0
	org_index = cal_locations.iloc[0].name
	while cal_locations.shape[0] > 1:
		start_row = cal_locations.loc[org_index]
		start_address = start_row['original_address']
		orig_lat = start_row['lat']
		orig_lng = start_row['lon']

		dest_index = findNextNearest(cal_locations,orig_lat,orig_lng,org_index)
		end_row = cal_locations.loc[dest_index]
		end_address = end_row['original_address']
		stores_visited['lat'].append(orig_lat)
		stores_visited['lon'].append(orig_lng)
		stores_visited['Start'].append(start_address)
		stores_visited['End'].append(end_address)

		cal_locations = cal_locations.drop(org_index)
		org_index = dest_index

		print(cal_locations.shape)

		distance_matrix=gmaps.distance_matrix(start_address,end_address,mode="driving")
		driving_time = distance_matrix['rows'][0]['elements'][0]['duration']['value']
		distance_driven = distance_matrix['rows'][0]['elements'][0]['distance']['value']
		
		time_spent_in_store = random.randrange(min_time_in_store,max_time_in_store)
		time_for_next_site = driving_time + time_spent_in_store
		

		if temp_emp.on_clock_time + time_for_next_site > max_time_on_clock or cal_locations.shape[0] == 1:
			if stops == 0:
				temp_emp.addStoretime(time_spent_in_store)
				stores_visited['lat'].append(orig_lat)
				stores_visited['lon'].append(orig_lng)
				stores_visited['Start'].append(start_address)
				stores_visited['End'].append('N/A')
			else:
				stores_visited['lat'].append(orig_lat)
				stores_visited['lon'].append(orig_lng)
				stores_visited['Start'].append(start_address)
				stores_visited['End'].append('NONE')

			temp_emp.stores_visited = pd.DataFrame(data=stores_visited)
			temp_emp.stops = stops + 1
			ax.plot(temp_emp.stores_visited['lon'],temp_emp.stores_visited['lat'])
			employees.append(temp_emp)
			temp_emp.printReport()
			emp_id = emp_id + 1
			temp_emp = Employee(emp_id)
			stores_visited = {'lat':[],'lon':[],'Start':[],'End':[]}
			stops = 0
			x = x + 1

		else:
			stores_visited['lat'].append(orig_lat)
			stores_visited['lon'].append(orig_lng)
			stores_visited['Start'].append(start_address)
			stores_visited['End'].append(end_address)
			

			temp_emp.addStoretime(time_spent_in_store)
			temp_emp.addDrivetime(driving_time) #30 mins place holder
			temp_emp.logMiles(distance_driven) # 60 miles place holder
			stops = stops + 1
			x = x + 1

	employee_data = []
	ids = [e.id for e in employees]
	ids.insert(0,0)
	print(ids)
	ax.legend(ids)
	for employee in employees:
		total_payroll = total_payroll + employee.payroll
	    # Extract relevant data from the employee object
		employee_data.append([employee.id,
		employee.time_driving / 3600,
		employee.time_in_store / 3600,
		employee.on_clock_time /3600,
		employee.miles_driven,
		employee.labor_payroll,
		employee.miles_payroll,
		employee.payroll,
		employee.stops,
		employee.stores_visited.to_json()
		    ])
	print("Total Payroll: $", total_payroll)
	plt.show()


	# Create a DataFrame from the employee data list
	df = pd.DataFrame(employee_data, columns=[
	    'Employee ID', 'Hours Driving', 'Hours in Store','Total Paid Hours', 'Miles Driven', 'Labor Payroll', 'Miles Payroll', 'Total Payroll',
	    'Stops', 'Stores Visited'
	])

	# Save the DataFrame to a CSV file
	df.to_csv('routes.csv', index=False)


if __name__ == "__main__":
	main()