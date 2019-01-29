from flask import Flask, render_template,url_for,request
import pymongo
import json
import bson


app = Flask(__name__)

aws_regions = { 
		"Asia Pasific (Mumbai)":"ap-south-1", 
		"Asia Pasific (Seoul)":"ap-northeast-2",
		"Asia Pasific (Singapore)":"ap-southeast-1",
		"Asia Pacific (Sydney)":"ap-southeast-2",
		"Asia Pacific (Tokyo)":"ap-northeast-1", 
		"Canada (Central)":"ca-central-1",
		"EU (Frankfurt)":"eu-central-1",
		"EU (Ireland)":"eu-west-1", 
		"EU (London)":"eu-west-2", 
		"EU (Paris)":"eu-west-3", 
		"EU (Stockholm)":"eu-north-1",
		"South America (Sao Paulo)":"sa-east-1", 
		"US East (N.Virginia)":"us-east-1",
		"US East (Ohio)":"us-east-2", 
		"US West (N.California)":"us-west-1", 
		"Oregon":"us-west-2"
				}

locations = [ 'Oregon', 'California', 'Virginia', 'S.California', 'Illinois', 'Ohio',
			'Iowa', 'India', 'Tokyo', 'S.Korea', 'Sigapore', 'Sydney', 'Ireland', 'London',
			'Frankfurt', 'Netherland', 'France','Finland','Canada','China','Brazil' ]

def connect_to_mongodb(collection_name):
	client = pymongo.MongoClient()
	db = client['test-database']
	col = db['{}'.format(collection_name)]
	return col

def query_to_list(results):
	result_list = []
	for result in results:
		result_list.append({'zone':result['zone'],
			'type':result['type'],
			'purpose': result['purpose'],
			'onDemandPrice':result['onDemandPrice'],
			'cpusPerVm':result['cpusPerVm'],
			'memPerVm':result['memPerVm'],
			'gpusPerVm':result['gpusPerVm'],
			'ntwPerf':result['ntwPerf'],
			'ntwPerfCategory':result['ntwPerfCategory']
			})
	return result_list

def find_location(regions,location):
	for key,value in regions.items():
		if key == location:
			return value
		else:
			pass

def aws_search_by_location(location):
	client = pymongo.MongoClient()
	db = client['test-database']
	col = db['aws']

	places = col.find({'zone':location}).sort('cpusPerVm', 1)
	return places

_list = query_to_list(aws_search_by_location('ap-northeast-2'))


@app.route("/", methods = ['GET', 'POST'])
@app.route("/index",methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
def homepage():
	

		return render_template('home.html', locations=locations)

@app.route("/<location>", methods = ['GET', 'POST'])
def home_loc(location):
	
	print(location)
	region = find_location(aws_regions,location)
	results = query_to_list(aws_search_by_location(region))

	return render_template('home.html', locations=locations, results = results)


@app.route('/result')
def result():
	return render_template('result.html')









if __name__ == '__main__':
	app.run(debug=True)