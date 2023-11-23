import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve content from {url}")
        return None

def extract_blog_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract blog details (modify as per the actual HTML structure)
    blog_titles = [title.text.strip() for title in soup.select('#post-3301 > div > div.clearfix.post-content > div:nth-child(3) > div > div > div > div.blog-items.row.blog-type-horizontal.blog-5dccfdae54fca.isotope > article:nth-child(1) > div > div.content > h6 > a')]
    blog_dates = [date.text.strip() for date in soup.select('#post-3301 > div > div.clearfix.post-content > div:nth-child(3) > div > div > div > div.blog-items.row.blog-type-horizontal.blog-5dccfdae54fca.isotope > article:nth-child(1) > div > div.content > div.blog-detail > div:nth-child(1) > span')]
    blog_image_urls = [image['src'] for image in soup.select('#post-3301 > div > div.clearfix.post-content > div:nth-child(3) > div > div > div > div.blog-items.row.blog-type-horizontal.blog-5dccfdae54fca.isotope > article:nth-child(1) > div > div.img > a')]
    blog_likes_count = [likes.text.strip() for likes in soup.select('#zilla-likes-25730 > i')]

    # Create a DataFrame to organize the data
    data = {
        'Blog Title': blog_titles,
        'Blog Date': blog_dates,
        'Blog Image URL': blog_image_urls,
        'Blog Likes Count': blog_likes_count
    }

    df = pd.DataFrame(data)
    return df

def scrape_and_save_data(url):
    html_content = get_page_content(url)

    if html_content:
        blog_data = extract_blog_data(html_content)

        # Save the data to CSV
        blog_data.to_csv('blog_data.csv', index=False)

if __name__ == "__main__":
    target_url = "https://rategain.com/blog"
      # You may adjust this based on the number of pages to scrape

    scrape_and_save_data(target_url)
