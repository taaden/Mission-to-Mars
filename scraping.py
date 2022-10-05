

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
from selenium  import webdriver

def scrape_all():
# Set the executable path and initialize Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)


    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres":  mars_hemispheres(browser)
    }
     # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # ### Visit the NASA Mars News Site
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')
    
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # ### JPL Space Images Featured Image
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:

        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # ### Mars Facts
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=False)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_hemispheres(browser):
    # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    #### Hemispheres
    
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    hemispheres_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles
    mars_hemispheres = hemispheres_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
     # Iterate through each hemisphere data
    for x in mars_hemispheres :
        # Collect Title
        hemisphere = x.find('div', class_="description")
        title = hemisphere.h3.text
        # Collect image link by browsing to hemisphere page
        image_link = x.find('img', class_='thumb').get('src')
        complete_url= url + image_link  
        #    create empty dictionary
        hemispheres = {}
        hemispheres["img_url"] = complete_url
        hemispheres["title"] = title
    
        hemisphere_image_urls.append(hemispheres)
        
        # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":
   
     # If running as script, print scraped data
   print(scrape_all())
 



