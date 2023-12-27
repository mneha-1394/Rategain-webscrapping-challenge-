
import cloudscraper
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import os
    
try: 
    list=[]
    for page in tqdm(range(1,2)):
        link='https://rategain.com/blog/page/'+ str(page)+'/'
        scraper=cloudscraper.create_scraper()
        res=scraper.get(link)
        soup = BeautifulSoup(res.text,'html.parser')
        list=[]
        for blog in soup.find_all('div',class_='wrap'):
            image=blog.find('div',class_='img')
            blogimage=image.find('a').get('href')
            blogtd=blog.find('div',class_='content')
            blogtitle=blogtd.find('h6').text
            blogdate=blogtd.find('span').text
            likes=blog.find('a',class_='zilla-likes')
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
except:
    print('Failed to retrieve page')


