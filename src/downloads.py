import json
import requests
import os

folder = "images"
file = "featured_images"

def read_file():
  # Opening JSON file
  f = open(f'{file}.json')
    
  # returns JSON object as 
  # a dictionary
  data = json.load(f)
    
  # Closing file
  f.close()

  return data

if __name__ == "__main__":

  # Crea la carpeta "imágenes" si no existe
  if not os.path.exists(folder):
    os.makedirs(folder)


  data = read_file()
  
  for v in data:
    response = requests.get(v)
    open(folder + "/"+v.split("/")[-1], "wb").write(response.content)