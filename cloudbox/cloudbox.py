from flask import Flask, render_template,url_for,request, make_response
import pymongo
import json
import bson
import pdfkit


app = Flask(__name__)

#results=[]

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
			'Iowa', 'India', 'Tokyo', 'S.Korea', 'Sydney', 'Ireland', 'London',
			'Frankfurt', 'Netherlands', 'France','Finland','Canada','China','Brazil' ]
purposes = ['General', 'Computer Opt','Memory Opt', 'Accelerated Comp','Storage Opt']

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
	places = col.find({'zone':location}).sort('cpusPerVm',1)
	return places

def azure_search_by_location(location):
	client = pymongo.MongoClient()
	db = client['test-database']
	col = db['azure']
	places = col.find({'zone':location}).sort('cpusPerVm',1)
	return places

def google_search_by_location(location):
	client = pymongo.MongoClient()
	db = client['test-database']
	col = db['google']
	places = col.find({'zone':location}).sort('cpusPerVm',1)
	return places

def query_to_ordered_list(_query,name):
	_list = []

	for item in _query:
		

		if item[name] not in _list:
			_list.append(item[name])
		else:
			pass
	_list.sort()
	return _list

def query_location_purpose(location,purpose):
	result=[]
	
	if purpose == 'General':
		aws_location = find_location(aws_regions,location)
		aws_connect = connect_to_mongodb('aws')
		aws_result = aws_connect.find({ "$and":[{'zone':aws_location},{'purpose':'general'}]}).sort('cpusPerVm',1)
		result.extend(aws_result)

		azure_location = find_location(azure_regions,location)
		azure_connect = connect_to_mongodb('azure')
		azure_result = azure_connect.find({ "$and":[{'zone':azure_location},{'purpose':'general'}]}).sort('cpusPerVm',1)
		result.extend(azure_result)

		google_location = find_location(google_regions,location)
		google_connect = connect_to_mongodb('google')
		google_result = google_connect.find({ "$and":[{'zone':google_location},{'purpose':'general'}]}).sort('cpusPerVm',1)
		result.extend(google_result)
		return result
	elif purpose == 'Computer Opt':
		aws_location = find_location(aws_regions,location)
		aws_connect = connect_to_mongodb('aws')
		aws_result = aws_connect.find({ "$and":[{'zone':aws_location},{'purpose':'computer_opt'}]}).sort('cpusPerVm',1)
		result.extend(aws_result)

		azure_location = find_location(azure_regions,location)
		azure_connect = connect_to_mongodb('azure')
		azure_result = azure_connect.find({ "$and":[{'zone':azure_location},{'purpose':'computer_opt'}]}).sort('cpusPerVm',1)
		result.extend(azure_result)

		google_location = find_location(google_regions,location)
		google_connect = connect_to_mongodb('google')
		google_result = google_connect.find({ "$and":[{'zone':google_location},{'purpose':'computer_opt'}]}).sort('cpusPerVm',1)
		result.extend(google_result)
		return result
	elif purpose =='Memory Opt':
		aws_location = find_location(aws_regions,location)
		aws_connect = connect_to_mongodb('aws')
		aws_result = aws_connect.find({ "$and":[{'zone':aws_location},{'purpose':'memory_opt'}]}).sort('cpusPerVm',1)
		result.extend(aws_result)

		azure_location = find_location(azure_regions,location)
		azure_connect = connect_to_mongodb('azure')
		azure_result = azure_connect.find({ "$and":[{'zone':azure_location},{'purpose':'memory_opt'}]}).sort('cpusPerVm',1)
		result.extend(azure_result)

		google_location = find_location(google_regions,location)
		google_connect = connect_to_mongodb('google')
		google_result = google_connect.find({ "$and":[{'zone':google_location},{'purpose':'memory_opt'}]}).sort('cpusPerVm',1)
		result.extend(google_result)
		return result
	elif purpose =='Accelerated Comp':
		aws_location = find_location(aws_regions,location)
		aws_connect = connect_to_mongodb('aws')
		aws_result = aws_connect.find({ "$and":[{'zone':aws_location},{'purpose':'accelerated_comp'}]}).sort('cpusPerVm',1)
		result.extend(aws_result)

		azure_location = find_location(azure_regions,location)
		azure_connect = connect_to_mongodb('azure')
		azure_result = azure_connect.find({ "$and":[{'zone':azure_location},{'purpose':'accelerated_comp'}]}).sort('cpusPerVm',1)
		result.extend(azure_result)

		google_location = find_location(google_regions,location)
		google_connect = connect_to_mongodb('google')
		google_result = google_connect.find({ "$and":[{'zone':google_location},{'purpose':'accelerated_comp'}]}).sort('cpusPerVm',1)
		result.extend(google_result)
		return result
	elif purpose == 'Storage Opt':
		aws_location = find_location(aws_regions,location)
		aws_connect = connect_to_mongodb('aws')
		aws_result = aws_connect.find({ "$and":[{'zone':aws_location},{'purpose':'storage_opt'}]}).sort('cpusPerVm',1)
		result.extend(aws_result)

		azure_location = find_location(azure_regions,location)
		azure_connect = connect_to_mongodb('azure')
		azure_result = azure_connect.find({ "$and":[{'zone':azure_location},{'purpose':'storage_opt'}]}).sort('cpusPerVm',1)
		result.extend(azure_result)

		google_location = find_location(google_regions,location)
		google_connect = connect_to_mongodb('google')
		google_result = google_connect.find({ "$and":[{'zone':google_location},{'purpose':'storage_opt'}]}).sort('cpusPerVm',1)
		result.extend(google_result)
		return result

def qeury_location_cpu(location,cpu):
	result =[]
	
	aws_location = find_location(aws_regions,location)
	aws_connect = connect_to_mongodb('aws')
	aws_result = aws_connect.find({ "$and":[{'zone':aws_location},{'cpusPerVm': int(cpu)}]}).sort('memPerVm',1)
	result.extend(aws_result)
	
	azure_location = find_location(azure_regions,location)
	azure_connect = connect_to_mongodb('azure')
	azure_result = azure_connect.find({ "$and":[{'zone':azure_location},{'cpusPerVm': int(cpu)}]}).sort('memPerVm',1)
	result.extend(azure_result)

	google_location = find_location(google_regions,location)
	google_connect = connect_to_mongodb('google')
	google_result = google_connect.find({ "$and":[{'zone':google_location},{'cpusPerVm': int(cpu)}]}).sort('memPerVm',1)
	result.extend(google_result)
	return result

def query_location_cpu_mem(location,cpu,mem):
	result =[]
	
	aws_location = find_location(aws_regions,location)
	aws_connect = connect_to_mongodb('aws')
	aws_result = aws_connect.find({ "$and":[{'zone':aws_location},{'cpusPerVm': int(cpu)},{'memPerVm': float(mem)}]})
	result.extend(aws_result)
	
	azure_location = find_location(azure_regions,location)
	azure_connect = connect_to_mongodb('azure')
	azure_result = azure_connect.find({ "$and":[{'zone':azure_location},{'cpusPerVm': int(cpu)},{'memPerVm': float(mem)}]})
	result.extend(azure_result)

	google_location = find_location(google_regions,location)
	google_connect = connect_to_mongodb('google')
	google_result = google_connect.find({ "$and":[{'zone':google_location},{'cpusPerVm': int(cpu)},{'memPerVm': float(mem)}]})
	result.extend(google_result)
	return result

	

def find_purpose(purpose):
	if purpose == 'General':
		return 'general'
	elif purpose == 'Computer Opt':
		return 'computer_opt'
	elif purpose == 'Memory Opt':
		return 'memory_opt'
	elif purpose == 'Accelerated Comp':
		return 'accelerated_comp'
	elif purpose == 'Storage Opt':
		return 'storage_opt'

def query_location_purpose_cpu(location,purpose,cpu):
	result =[]
	n_purpose = find_purpose(purpose)
	
	aws_location = find_location(aws_regions,location)
	aws_connect = connect_to_mongodb('aws')
	aws_result = aws_connect.find({ "$and":[{'zone':aws_location},{'purpose': n_purpose },{'cpusPerVm': int(cpu)}]}).sort('memPerVm',1)
	result.extend(aws_result)
	
	azure_location = find_location(azure_regions,location)
	azure_connect = connect_to_mongodb('azure')
	azure_result = azure_connect.find({ "$and":[{'zone':azure_location},{'purpose': n_purpose},{'cpusPerVm': int(cpu)}]}).sort('memPerVm',1)
	result.extend(azure_result)

	google_location = find_location(google_regions,location)
	google_connect = connect_to_mongodb('google')
	google_result = google_connect.find({ "$and":[{'zone':google_location},{'purpose': n_purpose},{'cpusPerVm': int(cpu)}]}).sort('memPerVm',1)
	result.extend(google_result)
	return result

def query_location_purpose_cpu_mem(location,purpose,cpu,mem):
	result =[]
	
	n_purpose = find_purpose(purpose)
	
	aws_location = find_location(aws_regions,location)
	aws_connect = connect_to_mongodb('aws')
	aws_result = aws_connect.find({ "$and":[{'zone':aws_location},{'purpose': n_purpose },{'cpusPerVm': int(cpu)},{'memPerVm': float(mem)}]})
	result.extend(aws_result)
	
	azure_location = find_location(azure_regions,location)
	azure_connect = connect_to_mongodb('azure')
	azure_result = azure_connect.find({ "$and":[{'zone':azure_location},{'purpose': n_purpose},{'cpusPerVm': int(cpu)},{'memPerVm': float(mem)}]})
	result.extend(azure_result)

	google_location = find_location(google_regions,location)
	google_connect = connect_to_mongodb('google')
	google_result = google_connect.find({ "$and":[{'zone':google_location},{'purpose': n_purpose},{'cpusPerVm': int(cpu)},{'memPerVm': float(mem)}]})
	result.extend(google_result)
	return result

@app.route("/", methods = ['GET', 'POST'])
@app.route("/index",methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
def homepage():
	return render_template('index.html', locations=locations, purposes = purposes)

# @app.route('/test')
# def test():
# 	return render_template('index.html')

@app.route("/<location>", methods = ['GET','POST'])
def home_loc(location):
	results = []

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

	cpu_list = query_to_ordered_list(results,'cpusPerVm')
	mem_list = query_to_ordered_list(results,'memPerVm')	
	gpu_list = query_to_ordered_list(results,'gpusPerVm')
	
	return render_template('second.html', locations=locations, results = results, purposes=purposes,
	cpu_list=cpu_list, mem_list = mem_list, gpu_list=gpu_list, 	message=location,)

@app.route("/<location>/<purpose>")
def location_purpose(location,purpose):
	results = []
	results.extend(query_to_list(query_location_purpose(location,purpose)))
	#print(results)
	cpu_list = query_to_ordered_list(results,'cpusPerVm')
	mem_list = query_to_ordered_list(results,'memPerVm')	
	gpu_list = query_to_ordered_list(results,'gpusPerVm')

	return render_template('second.html', locations=locations, results = results, purposes=purposes,
	cpu_list=cpu_list, mem_list = mem_list, gpu_list=gpu_list, 	message=location, 
	message_purpose= purpose)


# @app.route("/<location>/<int:cpu>/<int:mem>")
# def location_cpu(location,cpu,mem):
# 	return "Done"

@app.route("/<location>/<purpose>/<cpu>")
def location_purpose_cpu(location,purpose,cpu):
	results =[]
	results = query_to_list(query_location_purpose_cpu(location,purpose,cpu))
	
	cpu_list = query_to_ordered_list(results,'cpusPerVm')
	mem_list = query_to_ordered_list(results,'memPerVm')	

	return render_template('second.html', locations=locations, results = results, purposes=purposes,
	cpu_list=cpu_list, mem_list = mem_list, message=location,message_purpose =purpose, message_cpu=cpu)

@app.route("/<location>/<cpu>/<float:mem>")
@app.route("/<location>/<int:cpu>", defaults={'mem': None})
@app.route("/<location>", defaults={'cpu': None,'mem': None})
def location_cpu_mem(location,cpu,mem):

	purpose = None
	results =[]

	if mem != None:
		results = query_to_list(query_location_cpu_mem(location,cpu,mem))
		cpu_list = query_to_ordered_list(results,'cpusPerVm')
		mem_list = query_to_ordered_list(results,'memPerVm')	

		return render_template('second.html', locations=locations, results = results, purposes=purposes,
		cpu_list=cpu_list, mem_list = mem_list, message=location, 
		message_purpose= purpose, message_cpu=cpu, message_mem = mem)
	else:
		results = query_to_list(qeury_location_cpu(location,cpu))
		cpu_list = query_to_ordered_list(results,'cpusPerVm')
		mem_list = query_to_ordered_list(results,'memPerVm')
		return render_template('second.html', locations=locations, results = results, purposes=purposes,
		cpu_list=cpu_list, mem_list = mem_list, message=location, 
		message_purpose= purpose, message_cpu=cpu, message_mem = mem)

@app.route("/<location>/<purpose>/<cpu>/<mem>")
def location_purpose_cpu_mem(location,purpose,cpu,mem):
	results =[]
	results = query_to_list(query_location_purpose_cpu_mem(location,purpose,cpu,mem))
	cpu_list = query_to_ordered_list(results,'cpusPerVm')
	mem_list = query_to_ordered_list(results,'memPerVm')	
	#gpu_list = query_to_ordered_list(results,'gpusPerVm')

	return render_template('second.html', locations=locations, results = results, purposes=purposes,
	cpu_list=cpu_list, mem_list = mem_list, message=location, 
	message_purpose= purpose, message_cpu=cpu,message_mem = mem)




@app.route("/pdf/<location>/<purpose>/<cpu>/<mem>")
@app.route("/pdf/<location>/<purpose>/<int:cpu>", defaults={'mem': None})
@app.route("/pdf/<location>/<purpose>", defaults={'cpu': None, 'mem': None})
@app.route("/pdf/<location>/<int:cpu>/<mem>", defaults={'purpose':None})
@app.route("/pdf/<location>/<int:cpu>", defaults={'purpose':None,'mem': None})
@app.route("/pdf/<location>", defaults={'purpose':None,'cpu':None,'mem': None})
def pdf_template(location,purpose,cpu,mem):


	results =[]
	if purpose == None and mem == None:
		results = query_to_list(qeury_location_cpu(location,cpu))
		cpu_list = query_to_ordered_list(results,'cpusPerVm')
		rendered =render_template('download_pdf.html', location=location,purpose=purpose,cpu=cpu_list,mem=mem,results=results)
		pdf = pdfkit.from_string(rendered,False)
	elif purpose == None:
		results = query_to_list(query_location_cpu_mem(location,cpu,mem))
		cpu_list = query_to_ordered_list(results,'cpusPerVm')
		rendered =render_template('download_pdf.html', location=location,purpose=purpose,cpu=cpu_list,mem=mem,results=results)
		pdf = pdfkit.from_string(rendered,False)
	elif cpu == None and mem == None:
		results = query_to_list(query_location_purpose(location,purpose))
		cpu_list = query_to_ordered_list(results,'cpusPerVm')
		mem_list = query_to_ordered_list(results,'memPerVm')
		rendered =render_template('download_pdf.html', location=location,purpose=purpose,cpu=cpu_list,mem=mem_list,results=results)
		pdf = pdfkit.from_string(rendered,False)

	elif mem == None:
		results = query_to_list(query_location_purpose_cpu(location,purpose,cpu))
		mem_list = query_to_ordered_list(results,'memPerVm')
		rendered =render_template('download_pdf.html', location=location,purpose=purpose,cpu=cpu,mem=mem_list,results=results)
		pdf = pdfkit.from_string(rendered,False)
	else:
		results = query_to_list(query_location_purpose_cpu_mem(location,purpose,cpu,mem))
		rendered =render_template('download_pdf.html', location=location,purpose=purpose,cpu=cpu,mem=mem,results=results)
		pdf = pdfkit.from_string(rendered,False)

	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

	return response

# @app.route('/result')
# def result():

# 	return render_template('result.html')









if __name__ == '__main__':
	app.run(debug=True)




	