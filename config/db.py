import pymongo
import pymysql
import re
from collections import OrderedDict

# mongodb配置
Client = pymongo.MongoClient('mongodb://testhzbihurw:hzbihutest456@192.168.10.222:27017/testscrapyBiHu')
dbm = Client.testscrapyBiHu
client = pymongo.MongoClient('localhost')
dbl = client.appstore_copy
collection = dbm.appstore_processed_data
# mysql配置
db_host = '192.168.10.222'
db_port = 3306
db_name = 'bihu'
db_user = 'bihurw'
db_passwd = 'bihu123456'
db = pymysql.connect(host=db_host, user=db_user, password=db_passwd, port=db_port)
cursor = db.cursor()

# 获取mongodb中appstore数据
def readAppstoreData():
	data = []
	d = {}
	for item in dbm.appstore_processed_data.find(): 
	# for item in dbl.items.find(): 
		d = {}
		d['app'] = item['trackName']
		d['company'] = item['artistName']
		data.append(d)
	print('Appstore总数据：', len(data))
	return data 

def parseAppstoreData(data):
	company1 = []
	for item in data:
		if re.findall(r'[\u4e00-\u9fa5]', item['company']):
			company1.append(item)
	print('Appstore中文数据：', len(company1))
	return company1

# 获取mysql中googleplay数据
def readGoogleplayData():
	sql = 'SELECT * FROM bihu.final_google_play;'
	try:
		data = []
		cursor.execute(sql)
		print('Googleplay总数据：', cursor.rowcount)
		for item in cursor:
			data.append(item)
		return data
	except:
		print('Error')

def parseGoogleplayData(datas):
	item = {}
	items = []
	for data in datas:
		item = {}
		item['app'] = data[0]
		item['company'] = data[1]
		items.append(item)
	company2 = []
	for item in items:
		if re.findall(r'[\u4e00-\u9fa5]', item['company']):
			company2.append(item)
	print('Googleplay中文数据：', len(company2))
	return company2

def saveToMongo(companyInfo):
	print('Saving data to MongoDB...')
	try:
		if dbm.companyPerson_ITjuzi.insert(companyInfo):
			print('\t' + 'Save successfully...')
	except:
		print('\t' + 'Save Failed...')

def readIncompletedata():
	data = []
	for item in dbl.app_companyInfo.find():
		data.append(item)
	# print(data)
	return data 

def removeDuplication(companys):
	o = OrderedDict()
	for item in companys:
		o.setdefault(item['app'], {**item,})
	o = list(o.values())
	return o
	# print(len(o))

		
def main():	
	data1 = readAppstoreData()
	company1 = parseAppstoreData(data1)
	data2 = readGoogleplayData()
	company2 = parseGoogleplayData(data2)
	companys = removeDuplication(company1 + company2)
	# incompleteData = readIncompletedata()

	# for i in range(len(incompleteData)):
	# 	companys.pop(i)
	print('中文总数据：', len(companys))
	return companys



if __name__ == '__main__':
	main()
