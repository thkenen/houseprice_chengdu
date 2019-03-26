#coding=utf-8
'''
目标为爬取成都各区房屋均价
区分二手房和新房'''
import requests
import time
from bs4 import BeautifulSoup
import pygal 

def get_response(url):
    '''获取页面'''
    req_header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    f=requests.post(url,headers=req_header)
    #print f.status_code
    soup=BeautifulSoup(f.text,'html.parser')
    return soup
def get_prices(soup,price_list):
    '''获取价格列表'''
    price_list=[]
    sell_list=soup.select("li['class'='clear LOGCLICKDATA']")
    for sell_house in sell_list:
        price=sell_house.select('div["class"="info clear"]')[0].select('div["class"="priceInfo"]')[0].select("div['class'='unitPrice']")[0]['data-price']
        price_list.append(int(price))
    return price_list
def turn_page(state_url,page=1):
    '''翻页'''
    url=''.join([state_url,'pa%i/'%page])
    return url
def turn_state(state):
    '''更换区'''
    url="http://cd.lianjia.com"
    state_url=''.join([url,'%s'%state])
    #print state_url
    return state_url
def get_states():
    '''获取区列表'''
    url="https://cd.lianjia.com/ershoufang/"
    soup=get_response(url)
    state_list=[]
    state_a_list=soup.select("div['data-role'='ershoufang']")[0].select('div > a')
    for state in state_a_list:
        state_list.append(state['href'])
    return state_list
def main():
    state_list=get_states()
    #print state_list
    dict_of_state={}
    for state in state_list:
        #print state
        state_url=turn_state(state)
        print 'turn state..'
        #print state_url
        state_name=state.split('/')[2]
        i=1
        price_list=[]
        while i <= 50:
            page_url=turn_page(state_url,i)
            #print page_url
            soup=get_response(page_url)
            price_list=get_prices(soup,price_list)
            i+=1
            time.sleep(3)
            print 'turn page..'
        total_price=0
        for price in price_list:
            total_price+=int(price)
        average_price=total_price/len(price_list)
        dict_of_state[state_name]=average_price
        
    print 'average price :',dict_of_state
    average_price_bar=pygal.Bar()
    average_price_bar.title='average house price in chengdu'
    average_price_bar.x_labels=[k for k in dict_of_state.keys()]
    average_price_bar.add('average price',[v for v in dict_of_state.values()])
    average_price_bar.render_to_file('average_price.svg')
main()            
