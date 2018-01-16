from PIL import Image
from pytesseract import image_to_string

import requests
from bs4 import BeautifulSoup

import pyscreenshot as ImageGrab

import time

#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
while True:
  img = ImageGrab.grab(bbox=(998,160,1424,580)) # X1,Y1,X2,Y2
  img = img.convert('LA').point(lambda p: p > 200 and 255)
  img_string = image_to_string(img.convert('RGB'), config='-psm 4')
  text_list = img_string.split("\n\n")

  # handle second answer bunching
  if len(text_list) == 3: 
    a_split = text_list[1].split("\n")
    if len(a_split) == 2:
      text_list[1] = a_split[0]
      text_list.insert(2, a_split[1])

  # restart loop if proper format not detected
  if (len(text_list) != 4) or ('?' not in text_list[0]):
    print('No question in screenshot.')
    print(text_list)
    continue
  else:
    print('='*10+'Official Question'+'='*10)

  q_text = text_list[0].replace('\n', " ")
  a_list = text_list[1:4]

  for a in a_list:
    query = '{} "{}"'.format(q_text, a)
    r = requests.get('https://www.google.com/search?q={}'.format(query))
    soup = BeautifulSoup(r.text, 'html.parser')
    num_results = soup.find('div',{'id':'resultStats'}).text
    print('{} : {}'.format(a, num_results))

  time.sleep(10)
