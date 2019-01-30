from flask import Flask, render_template,url_for,request
import pymongo
import json
import bson


app = Flask(__name__)

results=[]

aws_regions = { 
		"India":"ap-south-1", 
		"S.Korea":"ap-northeast-2",
		"Singapore":"ap-southeast-1",
		"Sydney":"ap-southeast-2",
		"Tokyo":"ap-northeast-1", 
		"Canada":"ca-central-1",
		"Frankfurt":"eu-central-1",
		"Ireland":"eu-west-1", 
		"London":"eu-west-2", 
		"France":"eu-west-3", 
		"Finland":"eu-north-1",
		"Brazil":"sa-east-1", 
		"Virginia":"us-east-1",
		"Ohio":"us-east-2", 
		"California":"us-west-1", 
		"Oregon":"us-west-2"
				}
azure_regions = {
	"Sydney": "australiaeast",
	#"Sydney": "australiasoutheast",
	"Brazil": "brazilsouth",
	"Canada": "canadacentral",
	"Canada": "canadaeast",
	"India": "centralindia",
	"Iowa": "centralus",
	"China": "eastasia",
	"Virginia": "eastus",
	"S.Carolina": "eastus2",
	"France": "francecentral",
	"Tokyo": "japaneast",
	#"Tokyo": "japanwest",
	"S.Korea": "koreacentral",
	#"S.Korea": "koreasouth",
	"Ohio": "northcentralus",
	"Ireland": "northeurope",
	#"Ohio": "southcentralus",
	#"India": "southindia",
	"Singapore": "southeastasia",
	"London": "uksouth",
	#"London": "ukwest",
	#"Iowa": "westcentralus",
	"Frankfurt": "westeurope",
	#"India": "westindia",
	"Oregon": "westus",
	"California": "westus2"
		}
google_regions = {
	"China": "asia-east2",
	"Mumbai": "asia-south1",
	"Singapore": "asia-southeast1",
	"Sydney": "australia-southeast1",
	"Taiwan": "asia-east1",
	"Tokyo": "asia-northeast1",
	"Canada":"northamerica-northeast1",
	"Belgium":"europe-west1",
	"Finland":"europe-north1",
	"Frankfurt":"europe-west3",
	"London":"europe-west2",
	"Netherlands":"europe-west4",
	"Brazil":"southamerica-east1",
	"Iowa":"us-central1",
	"Virginia":"us-east4",
	"S.Carolina":"us-east1",
	"California":"us-west2",
	"Oregon":"us-west1"
		}

locations = [ 'Oregon', 'California', 'Virginia', 'S.Carolina', 'Ohio',
			'Iowa', 'India', 'Tokyo', 'S.Korea', 'Sigapore', 'Sydney', 'Ireland', 'London',
			'Frankfurt', 'Netherlands', 'France','Finland','Canada','China','Brazil' ]
purposes = ['general', 'computer_opt','memory_opt', 'accelerated_comp','storage_opt']

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
			'provider':result['provider']
			})
	return result_list

#find zone from list
def find_location(regions,location): 
    if location in regions.keys(): 
        return regions[location] 
    else: 
        return None

def aws_search_by_location(location):
	client = pymongo.MongoClient()
	db = client['test-database']
	col = db['aws']
	places = col.find({'zone':location})
	return places

def azure_search_by_location(location):
	client = pymongo.MongoClient()
	db = client['test-database']
	col = db['azure']
	places = col.find({'zone':location})
	return places

def google_search_by_location(location):
	client = pymongo.MongoClient()
	db = client['test-database']
	col = db['google']
	places = col.find({'zone':location})
	return places

def query_to_cpu_ordered_list(_query,name):
	_list = []

	for item in _query:
		number = int(item[name])

		if number not in _list:
			_list.append(number)
		else:
			pass
	_list.sort()
	return _list




@app.route("/", methods = ['GET', 'POST'])
@app.route("/index",methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
def homepage():
	return render_template('home.html', locations=locations, purposes = purposes)

@app.route("/<location>", methods = ['GET','POST'])
def home_loc(location):
	results.clear()

	if location != None:
		region_aws = find_location(aws_regions,location)
		region_azure = find_location(azure_regions,location)
		region_google = find_location(google_regions,location)
		
		if region_aws:
			results.extend(query_to_list(aws_search_by_location(region_aws)))
		if region_azure:
			results.extend(query_to_list(azure_search_by_location(region_azure)))
		if region_google:
			results.extend(query_to_list(google_search_by_location(region_google)))

	
	cpu_list = query_to_cpu_ordered_list(results,'cpusPerVm')
	mem_list = query_to_cpu_ordered_list(results,'memPerVm')	
	gpu_list = query_to_cpu_ordered_list(results,'gpusPerVm')
	
	return render_template('home.html', locations=locations, results = results, purposes=purposes,
	cpu_list=cpu_list, mem_list = mem_list, gpu_list=gpu_list, 	message=location)

@app.route("/<location>/<purpose>")
def location_purpose(location,purpose):

	#print("{}, {} ".format(location,purpose))
	return "{}, {}".format(location,purpose)




# @app.route("/providers",methods =['GET','POST'])
# def get_button_data():
	
# 	if request.method == 'POST':
		
# 		if request.form['submit_button'] == 'AWS':
# 			#print(global_location)
# 			print('aws')
# 			print(results)
# 		elif request.form['submit_button'] == 'AZURE':
# 			print('azure')
# 		elif request.form['submit_button'] == 'GOOGLE':
# 			print('google')
# 		else:
# 			pass

# 		return "DONE"
# 	else:
# 		return "Something Wrong"
	
	

	

@app.route('/result')
def result():

	return render_template('result.html')









if __name__ == '__main__':
	app.run(debug=True)