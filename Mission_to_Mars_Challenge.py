#!/usr/bin/env python
# coding: utf-8

# In[25]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[26]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find & Click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_="fancybox-image").get('src')


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'


# ## Get Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# ## Hemispheres

# In[47]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[48]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
main_url = 'https://marshemispheres.com/'

# Parse the data
html = browser.html
hemi_url_soup = soup(html, 'html.parser')



# In[49]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
divs = hemi_url_soup.find("div", class_='downloads')
link_div = hemi_url_soup.find_all("div", class_="description")

anchors = browser.links.find_by_partial_text('Hemisphere')
relative_urls = set([anchor['href'] for anchor in anchors])

hemispheres = {}

for relative_url in relative_urls:
    
    full_url = f'{relative_url}'
    browser.visit(full_url)
    
    html = browser.html
    urls_soup = soup(html, 'html.parser')
    
    hemi_title = browser.find_by_tag('h2').text
    print(f'--> title: {hemi_title}')
    
    downloads_div = urls_soup.find('div', class_='downloads')
    img_anchor = downloads_div.find('a', text=('Sample'))
    img_url = img_anchor['href']
    full_img_url = f'{main_url}{img_url}'
    print(f'--> url: {main_url}{img_url}')
    
    hemispheres = {
           'img_url': full_img_url,
           'title': hemi_title,
    }
    
    browser.back()
        
    hemisphere_image_urls.append(hemispheres)
    
  
    


# In[50]:


# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)


# In[19]:


# 5. Quit the browser
browser.quit()


# In[ ]:




