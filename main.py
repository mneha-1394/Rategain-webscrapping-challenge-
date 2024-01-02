import cloudscraper
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd    

def scrape():
    data_list=[]
    try: 
        for page in tqdm(range(47)):
            blogtitle=''
            blogimage=''
            blogdate=''
            bloglikes=''
            link='https://rategain.com/blog/page/'+ str(page)+'/'
            scraper=cloudscraper.create_scraper()
            res=scraper.get(link)
            soup = BeautifulSoup(res.text,'html.parser')
            for blog in soup.find_all('div',class_='wrap'):
                if blog.find('div', class_='img'):
                    image = blog.find('div', class_='img')
                    if image.find('a').get('href'):
                       blogimage = image.find('a').get('href')
                if blog.find('div', class_='content'):
                    blogtitledate = blog.find('div', class_='content')
                    if blogtitledate.find('h6'):
                        blogtitle = blogtitledate.find('h6').text
                    if blogtitledate.find('span'):
                        blogdate = blogtitledate.find('span').text

                if blog.find('a', class_='zilla-likes'):
                    likes = blog.find('a', class_='zilla-likes')
                    if likes.find('span'):
                        bloglikes = likes.find('span').text
                data_list.append([blogtitle,blogimage,blogdate,bloglikes])
    finally:
        print('Completed')
    return data_list 

data_list= scrape()
df=pd.DataFrame(data_list,columns=['Blog Title','Blog Image URL','Blog Date','Blog Likes'])
df.to_csv("BlogData.csv",index=False)



