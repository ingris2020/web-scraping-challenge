from splinter import Browser
from bs4 import BeautifulSoup as bs
import datetime as dt
import pandas as pd
import re 
import requests

#mars_data = {}

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    mars_data = {}
    # Latest News
    browser = init_browser()
    news_url = "https://mars.nasa.gov/news"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")

    news_results = soup.find('div', class_='list_text')
    title = news_results.find('a').get_text()
    desc = news_results.find('div', class_='article_teaser_body').get_text()
    mars_data['News_Title']=title
    mars_data['News_Description']=desc

    
    #Feature Image Full Size
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    response = requests.get(image_url)
    soup = bs(response.text, 'html.parser')
    feature_i = soup.find('article', class_="carousel_item")["style"].strip("background-image: url(' .jpg' );")
    feature_img = (f'https://www.jpl.nasa.gov{feature_i}.jpg')

    mars_data['feature_img']= feature_img

    #Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(weather_url)
    soup = bs(response.text, 'html.parser')
    mars_weather = soup.find('div', class_="js-tweet-text-container").text.strip()
    
    mars_data['mars_weather']= mars_weather


    #Mars Fact Table
    fact_url = 'https://space-facts.com/mars/'
    mars_fact = pd.read_html(fact_url)
    mars_fact_df = mars_fact[1]
    mars_fact_df= mars_fact_df.drop(columns=['Earth'])
    mars_fact_df.rename(columns ={"Mars - Earth Comparison":'Description',"Mars":'Value'}, inplace=True)

    mars_fact_table = mars_fact_df.to_html(index=False, justify='center')

    mars_data['Facts_Table'] = mars_fact_table


    #Hemisphere image & link
    #Go into the main page for the Mars Hemisphere's
    hem_url = 'https://www.planetary.org/blogs/guest-blogs/bill-dunford/20140203-the-faces-of-mars.html'
    browser.visit(hem_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    hemispheres = soup.find_all('img', class_='img840')

    hemisphere_image_urls =[]

    for hemisphere in hemispheres:
        hem_title = hemisphere.get('alt')
        hem_url = hemisphere.get('src')
        hemisphere_image_urls.append({'title':hem_title,'img_url':hem_url})
        
    mars_data['hem_img']= hemisphere_image_urls     
    

    # Stop webdriver and return results
    browser.quit()
    return mars_data