#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time

def get_title(soup):
    try:
        title = soup.find("a",attrs={'class' : 'wjcEIp'})
        title_value = title.text
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

def get_mrp(soup):

    try:
        mrp_info = soup.find('div', {'class': 'yRaY8j'})
        mrp = mrp_info.text.strip()

    except AttributeError:
        mrp = ""
        
    return mrp


def get_price(soup):
    
    try:
        price_element = soup.find("div", attrs={'class':'Nx9bqj'})
        price = price_element.text.strip()
        
    except AttributeError:
        price = ""

    return price

def get_discount(soup):

    try:
        discount_info = soup.find('div', {'class': 'UkUFwK'})
        discount = discount_info.text.strip()
        
    except AttributeError:
        discount = ""
        
    return discount

def get_rating(soup):

    try:
        rating = soup.find("div", attrs={'class':'XQDdHH'}).text.strip()

    except AttributeError:
        rating = ""
    
    return rating

def get_reviews(soup):
    try:
        reviews = soup.find("span", attrs={'class':'Wphh3N'}).text.strip()

    except AttributeError:
        reviews = ""

    return reviews

if __name__ == '__main__':
    URL = "https://www.flipkart.com/search?q=headphones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    
    links = soup.find_all("a", attrs={"class": "VJA3rP"})
    links_list = []
    for link in links:
        links_list.append(link.get('href'))
        
    d = {"title": [], "mrp":[], "price": [], "discount": [], "rating": [], "reviews": []}

    for link in links_list:
        new_webpage = requests.get("https://www.flipkart.com" + link)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        d["title"].append(get_title(new_soup))
        d["mrp"].append(get_mrp(new_soup))        
        d["price"].append(get_price(new_soup))
        d["discount"].append(get_discount(new_soup))
        d["rating"].append(get_rating(new_soup))
        d["reviews"].append(get_reviews(new_soup))        

df = pd.DataFrame.from_dict(d)
df['title'].replace('', np.nan, inplace = True)
df = df.dropna(subset = ['title'])
df.to_csv("flip_data4.csv", header = True, index = False)


# In[2]:


df = pd.read_csv("flip_data4.csv")
print(df)


# In[ ]:




