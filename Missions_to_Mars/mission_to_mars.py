#!/usr/bin/env python
# coding: utf-8

import selenium
import requests
import os
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info( ):

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    website_url = "https://redplanetscience.com/"
    browser.visit(website_url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #response=requests.get(website_url)
    html=browser.html
    soup=bs(html,'html.parser')



    result_title=soup.find("div",class_="content_title").get_text()
    result_para=soup.find("div",class_="article_teaser_body").get_text()




    jpg_url="https://spaceimages-mars.com/"
    browser.visit(jpg_url)




    html2=browser.html
    soup_jpg=bs(html2,'html.parser')
    print(soup_jpg.prettify())




    partial_url=soup_jpg.find('img',class_='headerimage')['src']
    featured_image_url=jpg_url+partial_url




    #result_jpg=soup_jpg.find_by_partial_href('headerimage')




    # jpgs=soup_jpg.find_all('a',class_="fancybox-thumbs")




    # for jpg in jpgs:
    #     try:
            
    #         link=jpg.img['src']
    #         raw_jpg_url=(jpg_url+"/"+link)
    #         jpg_url=raw_jpg_url.replace(" ","%20")
    #     except:
    #         link=""



    html_table="https://galaxyfacts-mars.com/"
    # browser.visit(html_table)
    # browser.is_element_present_by_css('table.table', wait_time=1)
    # html_table=browser.html
    # soup_table=bs(html_table,'html.parser')
    # result_table=soup_table.find("tbody")
    # print(soup_table.prettify())




    tables = pd.read_html(html_table)
    tables




    df = tables[0]
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    df.set_index('Mars - Earth Comparison',inplace=True)




    table_mars=df.to_html()




    html_hemi="https://marshemispheres.com/"
    browser.visit(html_hemi)
    #browser.is_element_present_by_css('collapsible results', wait_time=1)


    html_hemi=browser.html
    soup_hemi=bs(html_hemi,'html.parser')
    hemi=soup_hemi.find_all('a',class_='itemLink product-item')
    hemisphere_image_urls=[]

    for h in hemi:
        try:
            
            title = h.img['alt']
            hemi_url = "https://marshemispheres.com/" + h.img['src']
            h_dict = {}
            h_dict['title'] = title
            h_dict['img_url'] = hemi_url
            hemisphere_image_urls.append(h_dict)
        except:
            print("--")

    mars={"news_title":result_title,
             "news_para":result_para,
             "feature_img":featured_image_url,
             #"table":table_mars,#
             "hemi1_title":hemisphere_image_urls[0]['title'],
             "hemi1_img":hemisphere_image_urls[0]['img_url'],
             "hemi2_title":hemisphere_image_urls[1]['title'],
             "hemi2_img":hemisphere_image_urls[1]['img_url'],
             "hemi3_title":hemisphere_image_urls[2]['title'],
             "hemi3_img":hemisphere_image_urls[2]['img_url'],
             "hemi4_title":hemisphere_image_urls[3]['title'],
             "hemi4_img":hemisphere_image_urls[3]['img_url']    
    }
    browser.quit()
    return mars

