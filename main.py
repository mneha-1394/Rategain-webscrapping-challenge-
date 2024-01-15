import streamlit as st
import cloudscraper
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd    

def scrape(url):
    try: 

        blog_data = {
            'Title': [],
            'Date': [],
            'Image URL': [],
            'Likes Count': []
        }
        for page in tqdm(range(1,47)):
            link= f'{url}page/{page}/'
            scraper=cloudscraper.create_scraper()
            res=scraper.get(link)
            soup=BeautifulSoup(res.text,'html.parser')
        # Getting the division where all the blog posts are present
            blogs_div = soup.find('div', class_='blog-items')

        # Check if blog posts are present
            if blogs_div is None:
                print("No blog posts found.")
                print(url)
            else:
                blog_posts = blogs_div.find_all('article', class_='blog-item')
                print(f"Found {len(blog_posts)} blog posts.")
                for post in blog_posts:
                    title = post.find('h6').find('a').text
                    date = post.find('div', class_='bd-item').find('span').text
                    Image_URL = post.find('div', class_='img')
                    if Image_URL:
                        Image_URL = Image_URL.find('a')['data-bg']
                    else:
                        Image_URL = ""

                    Likes_Count_text = post.find('a', class_='zilla-likes').find('span').text
                    Likes_Count = int(''.join(filter(str.isdigit, Likes_Count_text)))
                    blog_data['Title'].append(title)
                    blog_data['Date'].append(date)
                    blog_data['Image URL'].append(Image_URL)
                    blog_data['Likes Count'].append(Likes_Count)
    finally:
        print('Completed')
    return blog_data

st.title("Blog Data Extraction")

# User input: URL
url = st.text_input("Enter Blog URL:")

if st.button("Extract Data"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        # Extract blog data from the provided URL
        extracted_data = scrape(url)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(extracted_data)

        # Display the extracted data in the Streamlit app
        st.dataframe(df)

        # Save the DataFrame to an Excel file
        df.to_csv('blog_data.csv', index=False)
        st.success("Data extraction and Excel file creation complete.")