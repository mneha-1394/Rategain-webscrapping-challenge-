
import cloudscraper
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import os
    
try: 
    list=[]
    for page in tqdm(range(1,48)):
        link='https://rategain.com/blog/page/'+ str(page)+'/'
        scraper=cloudscraper.create_scraper()
        res=scraper.get(link)
        soup = BeautifulSoup(res.text,'html.parser')
        list=[]
        for blog in soup.find_all('div',class_='wrap'):
            if blog.find('div',class_='img'):
                image=blog.find('div',class_='img')
            if image.find('a').get('href'):
                blogimage=image.find('a').get('href')
            if blog.find('div',class_='content'):
                blogtd=blog.find('div',class_='content')
            if blogtd.find('h6').text:
                blogtitle=blogtd.find('h6').text
            if blogtd.find('span').text:
                blogdate=blogtd.find('span').text
            if blog.find('a',class_='zilla-likes'):
                likes=blog.find('a',class_='zilla-likes')
            if likes.find('span').text:
                bloglikes=likes.find('span').text
            list.append([blogtitle,blogimage,blogdate,bloglikes])
    df=pd.DataFrame(list,columns=['Blog Title','Blog Image URL','Blog Date','Blog Likes'])
    
    # Delete existing file
    filename= 'Blog Data.csv'
    try:
        os.remove(filename)
    except OSError:
        pass
    df.to_csv(filename,index=False)
finally:
    print('Completed')


