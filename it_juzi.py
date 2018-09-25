import requests 
import time
import random
from lxml import etree
from fake_useragent import UserAgent
from config import db

ua = UserAgent()
def getPage(company):
	invalid_company = []
	for item in company:
		url = 'https://www.itjuzi.com/search?word=' + item['company']
		header1 = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
		}
		time.sleep(random.random() * 40)
		rsp = requests.get(url, headers=header1)
		print(rsp)
		doc = etree.HTML(rsp.text)

		header2 = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Cookie': '_ga=GA1.2.1435066329.1535266872; gr_user_id=6237d1b7-3e75-4804-854d-e2c3b121de54; acw_tc=76b20f4815371527785525755e43957e81593da1fb05f428db5c0e3c9816a0; MEIQIA_EXTRA_TRACK_ID=1A0G8XTQ9Gq1KgtBhMe3xldHXjy; _gid=GA1.2.534193698.1537354264; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1537152785,1537354264,1537354295,1537435703; MEIQIA_VISIT_ID=1AT1JWQ0jejNHDN1RgHfUEo6OwM; identity=18252755277%40test.com; remember_code=xjIXOqvOT%2F; unique_token=637559; paidtype=vip; gr_session_id_eee5a46c52000d401f969f4535bdaa78=97f70052-727c-4a75-939e-1fbdc7faf4be; gr_session_id_eee5a46c52000d401f969f4535bdaa78_97f70052-727c-4a75-939e-1fbdc7faf4be=true; session=c61862a2340a3019db76912ea66261c26534e9b4; _gat=1; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=' + str(time.time())[:10],
			'Host': 'www.itjuzi.com',
			# 'If-Modified-Since': Fri, 21 Sep 2018 06:06:18 GMT,
			'Referer': 'https://www.itjuzi.com/',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
		}
		try:
			href = doc.xpath('//ul[@id="the_search_list"]/li/a/@href')[0]
		except:
			invalid_company.append(item)
		time.sleep(random.random() * 20)
		print(href)
		rsp = requests.get(href, headers=header2)
		print(rsp)
		parsePage(rsp.text, item)

def parsePage(text, item):
	company_info = {}
	team_info = {}
	data = []
	doc = etree.HTML(text)
	try:
		team_info['name'] = doc.xpath('//div[@class="sec"]/ul/li/div/a/text()')[0]
	except:
		team_info['name'] = 'null'
	try:
		team_info['position'] = doc.xpath('//div[@class="sec"]/ul/li/div[2]/text()')[0]
	except:
		team_info['position'] = 'null'
	try:
		team_info['description'] = doc.xpath('//div[@class="sec"]/ul/li/div[3]//div/@title')[0]
	except:
		team_info['description'] = 'null'
	# print(team_info)

	basic_info = {}
	try:
		basic_info['注册资本'] = doc.xpath('//div[@class="essential"]/table/tbody/tr/td[1]/span[2]')[0].xpath('string(.)').replace('\t','').replace('\n','')
	except:
		basic_info['注册资本'] = 'null'	
	try:
		basic_info['成立时间'] = doc.xpath('//div[@class="essential"]/table/tbody/tr/td[2]/span[2]')[0].xpath('string(.)').replace('\t','').replace('\n','')
	except:
		basic_info['成立时间'] = 'null'
	try:
		basic_info['法人代表'] = doc.xpath('//div[@class="essential"]/table/tbody/tr[2]/td[1]/span[2]')[0].xpath('string(.)').replace('\t','').replace('\n','')
	except:
		basic_info['法人代表'] = 'null'
	try:
		basic_info['公司类型'] = doc.xpath('//div[@class="essential"]/table/tbody/tr[2]/td[2]/span[2]')[0].xpath('string(.)').replace('\t','').replace('\n','')
	except:
		basic_info['公司类型'] = 'null'
	try:
		basic_info['地址'] = doc.xpath('//div[@class="essential"]/table/tbody/tr[3]/td[2]/span[2]')[0].xpath('string(.)').replace('\t','').replace('\n','')
	except:
		basic_info['地址'] = 'null'
	company_info['index_info'] = item
	company_info['team_info'] = team_info 
	company_info['basic_info'] = basic_info 
	data.append(company_info)
	print(data)
	db.saveToMongo(data)


def main():
	companys = db.main()
	getPage(companys)
	

if __name__ == '__main__':
	main()




#主页cookie
# '_ga=GA1.2.1435066329.1535266872; gr_user_id=6237d1b7-3e75-4804-854d-e2c3b121de54; acw_tc=76b20f4815371527785525755e43957e81593da1fb05f428db5c0e3c9816a0; MEIQIA_EXTRA_TRACK_ID=1A0G8XTQ9Gq1KgtBhMe3xldHXjy; _gid=GA1.2.534193698.1537354264; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1537152785,1537354264,1537354295,1537435703; MEIQIA_VISIT_ID=1AT1JWQ0jejNHDN1RgHfUEo6OwM; identity=18252755277%40test.com; remember_code=xjIXOqvOT%2F; unique_token=637559; paidtype=vip; gr_session_id_eee5a46c52000d401f969f4535bdaa78=613a5bf4-61d9-40bf-ac8e-0dbaafbdc63e; gr_session_id_eee5a46c52000d401f969f4535bdaa78_613a5bf4-61d9-40bf-ac8e-0dbaafbdc63e=true; session=32680af8c18340f7c03265bd38b9880afa5aa3de; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1537496310'
# '_ga=GA1.2.1435066329.1535266872; gr_user_id=6237d1b7-3e75-4804-854d-e2c3b121de54; acw_tc=76b20f4815371527785525755e43957e81593da1fb05f428db5c0e3c9816a0; MEIQIA_EXTRA_TRACK_ID=1A0G8XTQ9Gq1KgtBhMe3xldHXjy; _gid=GA1.2.534193698.1537354264; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1537152785,1537354264,1537354295,1537435703; MEIQIA_VISIT_ID=1AT1JWQ0jejNHDN1RgHfUEo6OwM; identity=18252755277%40test.com; remember_code=xjIXOqvOT%2F; unique_token=637559; paidtype=vip; gr_session_id_eee5a46c52000d401f969f4535bdaa78=613a5bf4-61d9-40bf-ac8e-0dbaafbdc63e; gr_session_id_eee5a46c52000d401f969f4535bdaa78_613a5bf4-61d9-40bf-ac8e-0dbaafbdc63e=true; session=32680af8c18340f7c03265bd38b9880afa5aa3de; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1537497393'
# '_ga=GA1.2.1435066329.1535266872; gr_user_id=6237d1b7-3e75-4804-854d-e2c3b121de54; acw_tc=76b20f4815371527785525755e43957e81593da1fb05f428db5c0e3c9816a0; MEIQIA_EXTRA_TRACK_ID=1A0G8XTQ9Gq1KgtBhMe3xldHXjy; _gid=GA1.2.534193698.1537354264; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1537152785,1537354264,1537354295,1537435703; MEIQIA_VISIT_ID=1AT1JWQ0jejNHDN1RgHfUEo6OwM; identity=18252755277%40test.com; remember_code=xjIXOqvOT%2F; unique_token=637559; paidtype=vip; gr_session_id_eee5a46c52000d401f969f4535bdaa78=613a5bf4-61d9-40bf-ac8e-0dbaafbdc63e; gr_session_id_eee5a46c52000d401f969f4535bdaa78_613a5bf4-61d9-40bf-ac8e-0dbaafbdc63e=true; session=32680af8c18340f7c03265bd38b9880afa5aa3de; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1537497456'

#详情页cookie
# _ga=GA1.2.1435066329.1535266872; gr_user_id=6237d1b7-3e75-4804-854d-e2c3b121de54; acw_tc=76b20f4815371527785525755e43957e81593da1fb05f428db5c0e3c9816a0; MEIQIA_EXTRA_TRACK_ID=1A0G8XTQ9Gq1KgtBhMe3xldHXjy; _gid=GA1.2.534193698.1537354264; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1537152785,1537354264,1537354295,1537435703; MEIQIA_VISIT_ID=1AT1JWQ0jejNHDN1RgHfUEo6OwM; identity=18252755277%40test.com; remember_code=xjIXOqvOT%2F; unique_token=637559; paidtype=vip; gr_session_id_eee5a46c52000d401f969f4535bdaa78=97f70052-727c-4a75-939e-1fbdc7faf4be; gr_session_id_eee5a46c52000d401f969f4535bdaa78_97f70052-727c-4a75-939e-1fbdc7faf4be=true; session=c61862a2340a3019db76912ea66261c26534e9b4; _gat=1; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1537509881
# _ga=GA1.2.1435066329.1535266872; gr_user_id=6237d1b7-3e75-4804-854d-e2c3b121de54; acw_tc=76b20f4815371527785525755e43957e81593da1fb05f428db5c0e3c9816a0; MEIQIA_EXTRA_TRACK_ID=1A0G8XTQ9Gq1KgtBhMe3xldHXjy; _gid=GA1.2.534193698.1537354264; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1537152785,1537354264,1537354295,1537435703; MEIQIA_VISIT_ID=1AT1JWQ0jejNHDN1RgHfUEo6OwM; identity=18252755277%40test.com; remember_code=xjIXOqvOT%2F; unique_token=637559; paidtype=vip; gr_session_id_eee5a46c52000d401f969f4535bdaa78=97f70052-727c-4a75-939e-1fbdc7faf4be; gr_session_id_eee5a46c52000d401f969f4535bdaa78_97f70052-727c-4a75-939e-1fbdc7faf4be=true; session=c61862a2340a3019db76912ea66261c26534e9b4; _gat=1; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1537509900

# _ga=GA1.2.1435066329.1535266872; gr_user_id=6237d1b7-3e75-4804-854d-e2c3b121de54; acw_tc=76b20f4815371527785525755e43957e81593da1fb05f428db5c0e3c9816a0; MEIQIA_EXTRA_TRACK_ID=1A0G8XTQ9Gq1KgtBhMe3xldHXjy; _gid=GA1.2.534193698.1537354264; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1537152785,1537354264,1537354295,1537435703; MEIQIA_VISIT_ID=1AT1JWQ0jejNHDN1RgHfUEo6OwM; identity=18252755277%40test.com; remember_code=xjIXOqvOT%2F; unique_token=637559; paidtype=vip; gr_session_id_eee5a46c52000d401f969f4535bdaa78=97f70052-727c-4a75-939e-1fbdc7faf4be; gr_session_id_eee5a46c52000d401f969f4535bdaa78_97f70052-727c-4a75-939e-1fbdc7faf4be=true; session=c61862a2340a3019db76912ea66261c26534e9b4; _gat=1; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1537509979
# _ga=GA1.2.1435066329.1535266872; gr_user_id=6237d1b7-3e75-4804-854d-e2c3b121de54; acw_tc=76b20f4815371527785525755e43957e81593da1fb05f428db5c0e3c9816a0; MEIQIA_EXTRA_TRACK_ID=1A0G8XTQ9Gq1KgtBhMe3xldHXjy; _gid=GA1.2.534193698.1537354264; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1537152785,1537354264,1537354295,1537435703; MEIQIA_VISIT_ID=1AT1JWQ0jejNHDN1RgHfUEo6OwM; identity=18252755277%40test.com; remember_code=xjIXOqvOT%2F; unique_token=637559; paidtype=vip; gr_session_id_eee5a46c52000d401f969f4535bdaa78=97f70052-727c-4a75-939e-1fbdc7faf4be; gr_session_id_eee5a46c52000d401f969f4535bdaa78_97f70052-727c-4a75-939e-1fbdc7faf4be=true; session=c61862a2340a3019db76912ea66261c26534e9b4; _gat=1; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1537509984