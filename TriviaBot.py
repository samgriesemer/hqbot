from PIL import Image
from pytesseract import image_to_string
import requests
from bs4 import BeautifulSoup
import pyscreenshot as ImageGrab
from fake_useragent import UserAgent
import webbrowser
import time

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

class TriviaBot:
  
  def __init__(self):
    self.q  = ''
    self.a = []
    self.is_valid_q = False

  def ocr(self, x1, y1, x2, y2, threshold):

    # grab screenshot and get text
    img = ImageGrab.grab(bbox=(x1,y1,x2,y2))
    img = img.convert('LA').point(lambda p: p > threshold and 255)
    img_string = image_to_string(img.convert('RGB'), config="-c tessedit_char_blacklist=ﬁﬂ")
    text_list = img_string.split("\n\n")

    # handle split question issues
    seen_q_end = False
    total_q = []
    for i in reversed(range(len(text_list))):
      if '?' in text_list[i]:
        seen_q_end = True
      if seen_q_end:
        total_q.append(text_list[i])
        text_list.pop(i)
    text_list.insert(0, " ".join(total_q[::-1]))
    text_list[0] = text_list[0].replace('\n', " ")

    # handle ocr answer bunching
    if len(text_list) == 3: 
      a_split = text_list[1].split("\n")
      if len(a_split) == 2:
        text_list[1] = a_split[0]
        text_list.insert(2, a_split[1])

    print(text_list)

    # check for proper format
    if (len(text_list) != 4) or ('?' not in text_list[0]):
      self.q = ''
      self.a = []
      self.is_valid_q = False
    else:
      self.q = text_list[0]   # current question text
      self.a = text_list[1:4] # current answer options
      self.is_valid_q = True  # validity of question
    return

  def query(self, q, a):
    t0 = time.time()
    ua = UserAgent()
    #header = {'User-Agent':str(ua.random)}

    s = requests.Session()
    url = 'https://www.google.com/search?q={}'.format(q)

    fpage_list = []
    total_res_list = []
    nlp_list = []
    #webbrowser.open(url)

    front_page = s.get(url)
    front_soup = BeautifulSoup(front_page.text, 'html.parser')

    for script in front_soup(["script", "style"]):
      script.extract()

    front_soup = front_soup.get_text().lower()

    for ans in a:
      # naive question + answer
      query = '{} "{}"'.format(q, ans)
      url = 'https://www.google.com/search?q={}'.format(query)
      r = s.get(url)

      soup = BeautifulSoup(r.text, 'html.parser')
      '''
      entities = self.nlp(q)

      nlp_query = " ".join(['"{}"'.format(entities[i].name) for i in range(len(entities))])
      nlp_query += '" {}"'.format(ans)
      url = 'https://www.google.com/search?q={}'.format(nlp_query)
      nlp_r = s.get(url)

      nlp_soup = BeautifulSoup(nlp_r.text, 'html.parser')
      for script in nlp_soup(["script", "style"]):
        script.extract()

      nlp_soup = nlp_soup.get_text().lower()
  '''
      page_count = front_soup.count(ans.lower())
      num_results = soup.find('div',{'id':'resultStats'}).text

      num_results = [el for el in num_results.split(" ") if el[0].isdigit()]
      #num_results = "".join([c for c in num_results if c.isdigit()])

      num_results = 0 if num_results==[] else int(num_results[0].replace(",",""))

      #nlp_count = nlp_soup.count(ans.lower())
      print('{} -- {} -- {}'.format(ans, num_results, page_count))
        #nlp_count))

      fpage_list.append(page_count)
      total_res_list.append(num_results)
      #nlp_list.append(nlp_count)

    t1 = time.time()
    print('Time: {}'.format(t1-t0))
    return {'total_res':total_res_list, 'front_page':fpage_list}
    #'nlp_res':nlp_list}

  def nlp(self, q):
    client = language.LanguageServiceClient()
      #credentials='Users/samgriesemer/Downloads/hq-bot-f37d1dc0cc6b.json'

    document = types.Document(
      content=q,
      type=enums.Document.Type.PLAIN_TEXT)

    entities = client.analyze_entities(document=document)
    return entities.entities
