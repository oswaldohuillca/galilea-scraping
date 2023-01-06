import json
from bs4 import BeautifulSoup

def find_img(body, cb):
  soup = BeautifulSoup(body, 'html.parser')
  images = soup.find_all("img")
  if len(images) != 0:
    for v in images:
      src = v["src"]
      src = "https:"+src
      cb(src)



if __name__ == "__main__":
  results = []

  # Opening JSON file
  f = open('output.json')
    
  # returns JSON object as 
  # a dictionary
  data = json.load(f)

  def callback(src):
    results.append(src)
    
  # Iterating through the json
  # list
  for i in data:
    body = i["body"]
    find_img(body,callback)
    
  # Closing file
  f.close()

  # Writing to sample.json
  with open("body_images.json", "w", encoding='utf-8') as outfile:
    json.dump(results, outfile, indent=4)