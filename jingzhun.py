# import requests
# import config
# from fake_useragent import UserAgent 
# from multiprocessing.pool import Pool 
# from multiprocessing.dummy import Pool as ThreadPool

# useragent = UserAgent()
# base_url = 'http://192.168.10.222:5002/36kr/api/v1.0/company?name='
# header = {'User-Agent': useragent.random}

# def companyPersonInfo(companys):
# 	data = []
# 	companyInfo = {}
# 	for item in companys:
# 		url = base_url + item['company']
# 		rsp = requests.get(url, headers=header, timeout=60)
# 		print(rsp)
# 		doc = eval(rsp.text)
# 		team_info = {}
# 		basic_info = {}
# 		try:
# 			team_info['founding_team'] = doc['founding_team']
# 		except:
# 			team_info['founding_team'] = 'null'
# 		try:
# 			basic_info['investParts'] = doc['investParts']
# 		except:
# 			basic_info['investParts'] = 'null'
# 		companyInfo['index_info'] = item
# 		companyInfo['team_info'] = team_info
# 		companyInfo['basic_info'] = basic_info
# 		# print(companyInfo)
# 		data.append(companyInfo)
# 	print(data)
# 	config.saveToMongo(data)
# 		# data = []


# def main():
# 	companys = config.main()
# 	companyPersonInfo(companys[:3])
# 	# pool = Pool()
# 	# pool.map(companyPersonInfo, companys)
# 	# pool.close()
# 	# pool.join()


# if __name__ == '__main__':
# 	main()


import pymongo
import requests
from config import db
from fake_useragent import UserAgent 
from multiprocessing.pool import Pool 
from multiprocessing.dummy import Pool as ThreadPool

useragent = UserAgent()
base_url = 'http://192.168.10.222:5002/36kr/api/v1.0/company?name='
header = {'User-Agent': useragent.random}

client = pymongo.MongoClient('localhost')
dbl = client.bihu_project
collection = dbl.app_companyInfo_jingzhun

def companyPersonInfo(companys):
	data = []
	companyInfo = {}
	for item in companys:
		url = base_url + item['company']
		rsp = requests.get(url, headers=header, timeout=60)
		print(rsp)
		doc = eval(rsp.text)
		team_info = {}
		basic_info = {}
		try:
			team_info['founding_team'] = doc['founding_team'][0]
		except:
			team_info['founding_team'] = {'null'}
		try:
			basic_info['investParts'] = doc['investParts'][0]
		except:
			basic_info['investParts'] = {'null'}
		companyInfo['index_info'] = item
		companyInfo['team_info'] = team_info
		companyInfo['basic_info'] = basic_info
		data.append(companyInfo)
		db.saveToMongo(companyInfo)
		print('Saving data to MongoDB...')
		try:
			if dbl.app_companyInfo_jingzhun.insert(companyInfo):
				print('\t' + 'Save successfully...')
		except:
			print('\t' + 'Save Failed...')


def main():
	companys = db.main()
	companyPersonInfo(companys)


if __name__ == '__main__':
	main()




# import requests
# import config
# import re
# import time
# import random
# from fake_useragent import UserAgent 
# from multiprocessing import Pool 
# from lxml import etree
# from selenium import webdriver 


# ua = UserAgent()
# browser = webdriver.Chrome()

# def getCookie():
# 	# url = 'https://account.36kr.com/?ok_url=https%3A%2F%2F36kr.com%2F#/login?pos=header' 
# 	# browser.get(url)
# 	# time.sleep(15)
# 	# browser.find_element_by_xpath('//input[@id="kr-shield-username"]').send_keys('18252755277')
# 	# time.sleep(random.random() * 10)
# 	# browser.find_element_by_xpath('//input[@type="password"]').send_keys('pb940912')
# 	# time.sleep(random.random() * 10)
# 	# browser.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
# 	# cookies = browser.get_cookies()
# 	# print(type(cookies))

# 	# time.sleep(5)
# 	# # html = browser.page_source
# 	# # print(html)
# 	# # # cookie = {}
# 	# cookie = 'acw_tc='+cookies[3]['value']+'; ' + 'kr_stat_uuid='+cookies[1]['value']+'; ' + 'Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3='+'1537153436,1537520101,1537544137; ' + 'download_animation=1; ' + 'Hm_lpvt_e8ec47088ed7458ec32cde3617b23ee3='+str(time.time())[:10]+'; ' + '_kr_p_se='+cookies[2]['value']+'; ' + 'krid_user_id=1355437827; krid_user_version=2; kr_plus_id=1355437827; kr_plus_token=ClrIEWjZ1jqMj7tjY3BS6TRwczNdw572293_____; kr_plus_utype=0'
# 	# print(cookie)
# 	# with open('cookie.txt', 'a', encoding='utf8') as f:
# 	# 	f.write(cookie)
# 	# # return cookie

# 	browser.get('https://rong.36kr.com/landing/detail?type=company&sortField=MATCH_RATE&kw=%E7%99%BE%E5%BA%A6')
# 	browser.add_cookie({'name':'Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3', 'value':'1537153436,1537520101,1537544137'})
# 	browser.get('https://rong.36kr.com/landing/detail?type=company&sortField=MATCH_RATE&kw=%E7%99%BE%E5%BA%A6')
	 
# 	# browser.add_cookie({'name':cookies[4]['name'], 'value':cookies[4]['value']})

# 	time.sleep(5)
# 	html = browser.page_source
# 	print(html)
# 	# companyID = re.findall(r'data-stat-click="company\.(.*?)"', html, re.S)[0]
# 	# print(companyID)
# 	# return companyID, cookie
# 	# browser.quit()
	
# def getPages(companyID, cookie):
# 	company_info = {}
# 	company_url = 'https://rong.36kr.com/n/api/company/' + companyID
# 	finance_url = 'https://rong.36kr.com/n/api/company/' + companyID + '/finance'
# 	member_url = 'https://rong.36kr.com/n/api/company/' + companyID + '/member'
# 	header = {
# 		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
# 		'Cookie': cookie,
# 	}
# 	company_text = requests.get(company_url, headers=header).text
# 	finance_text = requests.get(finance_url, headers=header).text
# 	member_text = requests.get(member_url, headers=header).text
# 	print('company_text:', company_text)
# 	print('finance_text:', finance_text)
# 	print('member_text:', member_text)

# 	team_info = []
# 	team_person = {}
# 	print(member_text)
# 	for team in eval(member_text)['data']['members']:
# 		try:
# 			team_person['intro'] = team['intro']
# 		except:
# 			team_person['intro'] = 'null'
# 		try:
# 			team_person['name'] = team['name']
# 		except:
# 			team_person['name'] = 'null'
# 		try:
# 			team_person['position'] = team['position']
# 		except:
# 			team_person['position'] = 'null'
# 		team_info.append(team)
# 	company_info['index_info'] = item
# 	company_info['team_info'] = team_info 
# 	print('company_info: ', company_info)


# def main(): 
# 	# companys = config.main()
# 	# cookie, companyID = getCookie()
# 	# time.sleep(random.random())
# 	# getPages(companyID, cookie)
# 	getCookie()

# main()




# acw_tc=b65cfd2415371533972436492e356ab3c035ff3dd23a154f7572c915b04d32; kr_stat_uuid=TN5QH25626680; 
# Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3=1537153436,1537520101,1537544137; 
# Hm_lpvt_e8ec47088ed7458ec32cde3617b23ee3=1537600814; 
# download_animation=1; 
# _kr_p_se=13093f90-5b30-4361-9aac-b49ef90e8350; 
# krid_user_id=1355437827; krid_user_version=2; 
# kr_plus_id=1355437827; 
# kr_plus_token=ClrIEWjZ1jqMj7tjY3BS6TRwczNdw572293_____; 
# kr_plus_utype=0

# cookie = 'acw_tc='+cookies[3]['value']+'; ' + 'kr_stat_uuid='+cookies[1]['value']+'; ' + 'Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3='+'1537153436,1537520101,1537544137; ' + 
# 'download_animation=1; ' + 'Hm_lpvt_e8ec47088ed7458ec32cde3617b23ee3='+str(time.time())[:10]+'; ' + '_kr_p_se='+cookies[2]['value']+'; ' + 'krid_user_id=1355437827; krid_user_version=2; kr_plus_id=1355437827; kr_plus_token=ClrIEWjZ1jqMj7tjY3BS6TRwczNdw572293_____; kr_plus_utype=0'
# print(cookie)

# # b65cfd2315376000951443808e49d92ab65e6161f0a0bbca53d9fa0fc80461
# acw_tc=b65cfd2415371533972436492e356ab3c035ff3dd23a154f7572c915b04d32; kr_stat_uuid=Z7TFa25625735; 
# Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3=1537153436,1537520101,1537544137; 
# download_animation=1; 
# Hm_lpvt_e8ec47088ed7458ec32cde3617b23ee3=1537596566; 
# _kr_p_se=ed8b3403-ff6e-4d99-967d-b53b8ef9713c; 
# krid_user_id=1355437827; 
# krid_user_version=2; 
# kr_plus_id=1355437827; 
# kr_plus_token=ClrIEWjZ1jqMj7tjY3BS6TRwczNdw572293_____; 
# kr_plus_utype=0; 

# acw_tc=b65cfd2415371533972436492e356ab3c035ff3dd23a154f7572c915b04d32; kr_stat_uuid=TN5QH25626680; 
# Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3=1537153436,1537520101,1537544137; 
# Hm_lpvt_e8ec47088ed7458ec32cde3617b23ee3=1537600814; 
# download_animation=1; 
# _kr_p_se=13093f90-5b30-4361-9aac-b49ef90e8350; 
# krid_user_id=1355437827; 
# krid_user_version=2; 
# kr_plus_id=1355437827; 
# kr_plus_token=ClrIEWjZ1jqMj7tjY3BS6TRwczNdw572293_____; kr_plus_utype=0

# [{'domain': '.36kr.com', 'httpOnly': False, 'name': 'Hm_lpvt_e8ec47088ed7458ec32cde3617b23ee3', 'path': '/', 'secure': False, 'value': '1537600097'}, 
# {'domain': '.36kr.com', 'expiry': 2168752090, 'httpOnly': False, 'name': 'kr_stat_uuid', 'path': '/', 'secure': False, 'value': 'YKPFm25626668'}, 
# {'domain': 'passport.36kr.com', 'httpOnly': False, 'name': 'TY_SESSION_ID', 'path': '/pages', 'secure': False, 'value': 'cc58bc0b-5634-470c-bae0-ccc57e1046c0'}, 
# {'domain': 'passport.36kr.com', 'expiry': 1540278496.298032, 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'secure': False, 'value': 'b65cfd2315376000951443808e49d92ab65e6161f0a0bbca53d9fa0fc80461'}, 
# {'domain': '.36kr.com', 'expiry': 1569136097, 'httpOnly': False, 'name': 'Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3', 'path': '/', 'secure': False, 'value': '1537600097'}, 
# {'domain': '.36kr.com', 'expiry': 1569136101, 'httpOnly': False, 'name': 'download_animation', 'path': '/', 'secure': False, 'value': '1'}]



