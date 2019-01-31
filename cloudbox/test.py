import pymongo



	
client = pymongo.MongoClient()
db = client['test-database']
col = db['aws']
places = col.find({ "$and":[{'zone':'us-west-1'},{'purpose': 'general' },{'cpusPerVm': 2}]}).sort('memPerVm',1)


for place in places:
	print(place)

