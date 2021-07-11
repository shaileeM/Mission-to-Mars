# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    hemis_url_title=hemis_data(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemis_url_title":hemis_url_title
     
     
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data
    
#executable_path = {'executable_path':'C:\\Users\shail\.wdm\drivers\chromedriver\win32\91.0.4472.101\chromedriver.exe'}


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #convert the browser html to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')  #means class="list_text"
        slide_elem.find('div',class_="content_title").get_text()
        slide_elem.find('div', class_='article_teaser_body').get_text()

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p
    except AttributeError:
        return None,None
    
    return news_title,news_p


def featured_image(browser):
    
    # ### Featured Images from https://spaceimages-mars.com/
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #print(img_soup)
    
    # Find the relative image url
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    
        # Use the base URL to create an absolute URL
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
        #img_url
    except AttributeError:
        return None
    
    return img_url

def mars_facts():
    try:
        #Get the facts table from https://galaxyfacts-mars.com/
        df = pd.read_html("https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html")[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    df
    #Putting back df into html
    return df.to_html(classes="table table-striped")

def hemis_data(browser):
    #hemisphere links and titles from 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/'
    url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/'
    browser.visit(url)
    html=browser.html
    hemis_soup=soup(html,'html.parser')
    
    #list to hold image links and titles
    hemisphere_image_urls =[]
    result=hemis_soup.find_all("div",class_="item")
    
    for r in result:
        result_dict={}
        find_div=r.find("div",class_="description")
        #print(find_div)
        title=find_div.find('a').text
        #print(title)
        find_button=r.find('a',href=True)
        
        #print(find_button)
        link=find_button['href']
    #     link=link.rstrip(".html")
        #print(link)
        static_link="https://astrogeology.usgs.gov/"
        final_link=static_link+link
        #print(final_link)
        browser.visit(final_link)
        #Now in new page
        html=browser.html
        new_soup=soup(html,'html.parser')
        
        result_downloads=new_soup.find("div",class_="downloads")
        #print(result_downloads)
        #url= result.find('a')['href'].text
        sample_image=result_downloads.find('a')
        final_url=sample_image['href']
        #find_button.click()
        #print(final_url)
        
        result_dict.update({'img_url':final_url})
        result_dict.update({'title':title})
        #print(result_dict)
        hemisphere_image_urls.append(result_dict)
        
        return hemisphere_image_urls
        
    
        
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




