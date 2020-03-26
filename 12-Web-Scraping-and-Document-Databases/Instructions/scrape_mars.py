def scrape():    
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import requests
    import pymongo
    from splinter import Browser
    full_info=[]
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    news_title = soup.find("div", class_= "content_title").text
    full_info["news_title"]= news_title
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text("FULL IMAGE")
    browser.click_link_by_partial_text("more info")
    img_html = browser.html
    soup= bs(img_html, "html.parser")
    img = soup.find("figure").find("a")["href"]
    full_url = url + img
    full_info["full_url"]=full_url
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    tweet = soup.find("div", class_="js-tweet-text-container").text
    full_info["tweet"]= tweet
    mars = pd.read_html("https://space-facts.com/mars/")
    mars_facts = mars[0]
    mars_html = mars_facts.to_html().strip()
    full_info["mars_html"] = mars_html
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    page_html = browser.html
    soup= bs(page_html, "html.parser")
    astro_list= []
    hems = soup.find_all("div", class_= "description")

    for hem in hems:
        title = hem.find("h3").text
        page = hem.find("a")["href"]
        browser.visit(f"https://astrogeology.usgs.gov{page}")
        page_html = browser.html
        soup = bs(page_html, "html.parser")
        img = soup.find("div", class_="downloads").find("a")["href"]
        astro_list.append({"title": title, "image_url": img})
    full_info["astro_list"]= astro_list
    return full_info
    


