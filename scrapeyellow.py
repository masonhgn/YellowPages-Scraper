import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
driver = webdriver.Chrome(r"C:\Users\Mason\Desktop\driver\chromedriver")

main_list = []





def yellowSearch(trade, location, x):
    driver.get('https://www.yellowpages.com/')
    searchbox = driver.find_element_by_xpath('//*[@id="query"]')
    searchbox.send_keys(trade)
    searchlocation = driver.find_element_by_xpath('//*[@id="location"]')
    searchlocation.clear()
    searchlocation.send_keys(location)
    searchbutton = driver.find_element_by_xpath('//*[@id="search-form"]/button')
    searchbutton.click()
    paged_url = (driver.current_url + "&page=" + str(x))
    driver.get(paged_url)

    def extract(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

        r = requests.get(url, headers = headers)

        soup = BeautifulSoup(r.content, 'html.parser')

        return soup.find_all('div', class_ = 'result')


    results = extract(paged_url)

    def transform(results):
        for item in results:
            name = item.find('a', class_ = 'business-name').text
            phone = item.find('div', class_ = 'phones phone primary').text.strip()
            try:
                website = item.find('a', class_ = 'track-visit-website')['href']
            except: 
                website = 'NO WEBSITE!!!!!!!!!!!!!!!!!!!!!!!!!!!'

            business = {
                'name': name,
                'phone': phone,
                'website': website,
            }
            if not ("starbucks" in item.name) and not ("miller's" in item.name) and not ("brooks" in item.name):
                main_list.append(business)

        return
    
    def load():
        df = pd.DataFrame(main_list)
        df.to_csv('businesses.csv', index=False)
    
    for z in range(1,x+1):
        print(f'getting page {z}')
        transform(results)
        time.sleep(5)

    load()

    print('saved to csv')


#main func    
yellowSearch('auto', 'naples',2)

