import json
import requests
import os
from urllib.request import urlopen, quote
import pprint
import urllib.request

#iknow的key
key ="4d9c629bc16c4f98b2c6dbbfe9ed7316"

def getlocation(lat,lng):
    #31.809928, 102.537467, 3019.300
    #lat = '31.809928'
    #lng = '102.537467'
    url = 'http://api.map.baidu.com/geocoder?location=' + str(lat) + ',' + str(lng) + '&output=json&pois=1&ak=oWI2Uudm3mEupfMr51X4eqUF3814L73n'
    req = urllib.request.urlopen(url)  # json格式的返回数据
    res = req.read().decode("utf-8")  # 将其他编码的字符串解码成unicode
    return json.loads(res)

def jsonFormat(lat,lng):
    str = getlocation(lat,lng)
    dictjson={}#声明一个字典
    #get()获取json里面的数据
    jsonResult = str.get('result')
    address = jsonResult.get('addressComponent')
    #国家
    #country = address.get('country')
    #国家编号（0：中国）
    #country_code = address.get('country_code')
    #省
    province = address.get('province')
    #城市
    city = address.get('city')
    #城市等级
    #city_level = address.get('city_level')
    #县级
    #district = address.get('district')
    #街道
    street = address.get('street')
    #街道号
    street_number = address.get('street_number')
    #方向
    direction = address.get('direction')
    #距离
    distance = address.get('distance')
    #把获取到的值，添加到字典里（添加）
    #dictjson['country']=country
    #dictjson['country_code'] = country_code
    dictjson['province'] = province
    dictjson['city'] = city
    dictjson['street'] = street
    dictjson['street_number']=street_number
    dictjson['direction']=direction
    dictjson['distance']=distance
    return dictjson

#检索指定ip历史记录
def gethistory():
    #https://api.antitor.com/history/peer?ip=111.205.14.47&days=14&contents=100&language=en&key=4d9c629bc16c4f98b2c6dbbfe9ed7316
    url = "https://api.antitor.com/history/peer"
    ip_find = input("请输入要查找的ip：")
    max_days = input("请输入历史回溯天数：")
    contents = input("请输入最大检索数：")
    new_url = url+"?ip="+ip_find+"&days="+max_days+"&contents="+contents+"&language=en&key=4d9c629bc16c4f98b2c6dbbfe9ed7316"
    res = requests.get(new_url)
    if res.content != 0:
        json_data = json.loads(res.text)
        local_name = jsonFormat(json_data['geoData']['latitude'],json_data['geoData']['longitude'])
        print("国家：",json_data['geoData']['country'],"地址:",local_name['province']+local_name['city']+local_name['street']+local_name['street_number']+local_name['direction']+local_name['distance'], "纬度：", json_data['geoData']['latitude'], "经度：", json_data['geoData']['longitude'])
        j = 1
        for i in json_data['contents']:
            if j <= int(contents)-1:
                print("序号=",j,i['name'],"hash:",i['torrent']['infohash'])
            else:
                break
            j = j+1


 #通过hash查询种子被下载的ip地址以及所在国家
def getipinfobyhash():
    #https://api.antitor.com/torrent/downloads/
    url = "https://api.antitor.com/torrent/downloads/"
    day_data = input("请输入查询日期：")
    info_hash = input("请输入种子hash：")
    new_url = url+info_hash+"?key="+key+"&day="+day_data+"&days=11&short=false"
    res = requests.get(new_url)
    json_data = json.loads(res.text)
    if len(json_data) == 2:
        print("获取失败！",json_data['message'])
    else:
        for i in json_data['peers']:
            print("ip地址：",i['ip'],  "国家/地区",i['countryCode'])


#根据imdb获取相关信息
def getinfobyimdb():
    imdb = input("请输入imdb：")
    url = "https://api.antitor.com/torrent/list/"
    new_url = url + "imdb/"+ imdb + "?key="+ key
    res = requests.get(new_url)
    json_data = json.loads(res.text)
    for i in json_data['torrents']:
        print(i['name'])

if __name__ == '__main__':
    print("1:根据imdb的id获取电影名称")
    print("2:根据种子hash获取下载者ip和所在国家")
    print("3:检索ip种子下载历史")
    print("最大回溯天数16，最大检索数100")
    while(True):
        choice = input("请输入选择：")
        if int(choice) == 1:
            getinfobyimdb()
        if int(choice) == 2:
            getipinfobyhash()
        if int(choice) == 3:
            gethistory()


