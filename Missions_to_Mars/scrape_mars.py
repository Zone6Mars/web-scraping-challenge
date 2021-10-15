from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time as tm
import requests
import re
import pymongo
import numpy as np
import pandas as pd
from selenium import webdriver as sl


# ## NASA Mars News
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com'

    browser.visit(url)
    tm.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')


    # results are returned as an iterable list
    results = soup.find_all('div', class_="slide")
    titles = soup.find_all('div', class_='content_title')
    latest_title = titles[0].text.strip()
    para = soup.find_all('div', class_='article_teaser_body')
    latest_para = para[0].text.strip()
  
    # ## JPL Mars Space Images

    url2 = 'https://spaceimages-mars.com/'

    browser.visit(url2)
    tm.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    all_images = soup.find_all('img')
    featured_url = soup.find("img", class_ = "headerimage fade-in")['src']
    featured_image_url = url2 + featured_url
    featured_image_url
    

    # ## Mars Facts

    url3 = 'https://galaxyfacts-mars.com/'

    browser.visit(url3)
    tm.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    tables = pd.read_html(url3)
    comp_table = pd.DataFrame(tables[0])
    comp_table = comp_table.drop([0,0])
    comp_table.columns = ['','Mars', 'Earth']
    comp_table = comp_table.set_index('')
    comp_table_html = comp_table.to_html().replace('\n', '')
    print(comp_table_html)


    # ## Mars Hemispheres

    url4 = 'https://marshemispheres.com/'

    browser.visit(url4)
    html = browser.html
    soup = bs(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    titles = []
    for i in items:
        titles.append(i.find('h3').text.strip())


    stopwords = ['thumbnail']
    for word in list(titles):  # iterating on a copy since removing will mess things up
        if word in stopwords:
            word.remove(word)
    
    items2 = soup.find_all('a', class_='itemLink product-item')

    srcs_all = []

    for i in items2: 
        srcs_all.append(url4 + i['href'])
    
    srcs_unique = np.unique(srcs_all)
    srcs_unique_list = srcs_unique.tolist()
    del srcs_unique_list[0]

    srcs = []

    for i in srcs_unique_list:
        browser.visit(i)
        tm.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        high_def = url4 + soup.find('img', class_='wide-image')['src']
        srcs.append(high_def)  




    Hemi_Dict = []
    for i in range(len(titles)):
        Hemi_Dict.append({'title':titles[i],'img_url':srcs[i]})


    for i in range(len(Hemi_Dict)):
        print(Hemi_Dict[i]['title'])
        print(Hemi_Dict[i]['img_url'] + '\n')

    mars_data = {
    "latest_title": latest_title,
    "latest_para": latest_para,
    "featured_image_url": featured_image_url,
    "comp_table_html": comp_table_html,
    "Hemi_Dict" : Hemi_Dict
    }

    browser.quit
    return mars_data

    

    