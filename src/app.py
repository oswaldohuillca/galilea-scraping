import requests
from bs4 import BeautifulSoup
import json
import re
# import time

from tqdm import tqdm,trange
# from time import sleep
# from progress.bar import Bar



class Post:
  title = ""
  excerpt = ""
  categories = []
  post_date = ""
  body = ""
  featured_image = {}

  def __init__(self, title,excerpt, categories, post_date, body, featured_image):
    self.title = title
    self.excerpt = excerpt
    self.categories = categories
    self.post_date = post_date
    self.body = body
    self.featured_image = featured_image

  def to_json(self):
    return json.dumps(self.__dict__)


def read_sitemap_json() :
  # Opening JSON file
  f = open('sitemap.json')

  # returns JSON object as 
  # a dictionary
  data = json.load(f)

  # Iterating through the json
  # list
  return data['url']


def visite_site(url, cb):
  html = requests.get(url)
  soup = BeautifulSoup(html.text, 'html.parser')

  body = soup.find("body")
  wrapper = body.find("div",{"class":"content-wrapper"})
  grid = wrapper.find("div", {"class":"content"})

  title = grid.find("h1").get_text()
  content_html = grid.find("div", {"class":"text-widget-content"}).find_all("p")
  content = []
  for v in content_html:
    content.append(str(v))

  excerpt = get_excerpt(content_html)

  post_date = get_post_date(grid)
  post_featured = get_post_featured(grid)
  categories_html = grid.find("aside", {"class":"post-sidebar"}).find_all("a",{"class":"theme-button"})
  categories = []
  for v in categories_html:
    categories.append(v.get_text().strip())
  tags = get_post_tags(grid)

  # post = Post(title,excerpt,categories,post_date.get_text(),"\n".join(content),post_featured)
  post = {
    "title": title,
    "excerpt": excerpt,
    "categories": categories,
    "post_date": post_date.get_text(),
    "body": "\n".join(content),
    "featured":post_featured,
    "tags": tags
  }

  cb(post, post_featured)



def get_post_date(html):
  post_date = html.find("span",{"class":"post-meta"}).find_all("span")[-1]
  # print(post_date)s
  return post_date.find("p")

def get_post_featured(html):
  image_container = html.find("div",{"class":"post-featured"})

  if image_container :
    post_featured = html.find("div",{"class":"post-featured"}).find("img")
    return {
      "src": post_featured["src"],
      "alt": post_featured["alt"]
    }

  image_container = html.find("div",{"class":"blog-post-header", "style": True})
  
  if image_container:
    style = image_container["style"]
    url = re.search(r"url\((.+?)\)", style).group(1)
    return {
      "src": url,
    }

  return None


def get_post_tags(html):
  tags_html = html.find_all("a",{"class":"highlightBg"})#.find_all("a",{"class":"highlightBg"})
  tags = []
  if tags_html :
    for v in tags_html:
      tags.append(v.get_text())

  return tags


def get_excerpt(data):
  for v in data:
    if v.get_text() != "":
      return v.get_text()

if __name__ == "__main__":
  results = []
  list_images = []
  data = read_sitemap_json()

  def callback(r, image):
    results.append(r)
    # if image.url :
      #  list_images.append(image.url)

  for v in data:
    visite_site(v["loc"], callback)


  # print(results)
  # Writing to sample.json
  with open("data/output.json", "w",encoding='utf-8') as outfile:
    json.dump(results, outfile, indent=4,ensure_ascii=False)
  






