import json
import requests
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as bs


def crawler():
    result_list = []
    for i in range(1, 10):
        #Get chromedriver, set path for it and put url for driver.
        options = webdriver.ChromeOptions()
        url = 'https://www.jimms.fi/fi/Product/List/000-00P/komponentit--naytonohjaimet?ob=6'
        if i > 1:
            url = 'https://www.jimms.fi/fi/Product/List/000-00P/komponentit--naytonohjaimet?p=' + str(i) +'&ob=6'
        driver = webdriver.Chrome('/Program Files (x86)/chromedriver/chromedriver.exe', options=options)
        driver.get(url)
        elements = driver.find_elements_by_class_name('p_listTmpl1')

        for a in range(0, len(elements)):
            parsed_text = {}

            title = elements[a].find_element_by_class_name('p_name').text
            price = elements[a].find_element_by_class_name('p_price').text
            link = elements[a].find_element_by_link_text(title).get_attribute('href')
 
            page = requests.get(link).content
            soup = bs(page, 'lxml')
            features = soup.find('div', attrs={'itemprop':'description'}).text        
                      
            parsed_text['Title'] = title
            parsed_text['Price'] = price + '€'
            parsed_text['Features'] = features
            parsed_text['link'] = link

            result_list.append(parsed_text)

            parsed_text = {}
            

    return result_list

if __name__ == '__main__':
    print(json.dumps(crawler()))