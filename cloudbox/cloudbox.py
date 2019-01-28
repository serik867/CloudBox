from flask import Flask, render_template
import pymongo
import json
import bson


app = Flask(__name__)



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

def aws_search_by_location(location):
	client = pymongo.MongoClient()
	db = client['test-database']
	col = db['aws']
	places = col.find({'zone':location}).sort('cpusPerVm', 1)
	return places

_list = query_to_list(aws_search_by_location('ap-northeast-2'))


@app.route("/")
@app.route("/index")
@app.route("/home")
def homepage():
	return render_template('home.html', results = _list)


@app.route('/result')
def result():
	return render_template('result.html')









if __name__ == '__main__':
	app.run(debug=True)