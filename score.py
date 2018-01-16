import numpy as np
import pandas as pd
import time
from random import randint

from TriviaBot import TriviaBot

df = pd.read_csv('questions.csv')
df = df.iloc[32:44,:].copy()

hqbot = TriviaBot()
res_count = 0
fp_count  = 0
tot_count = 0
nlp_count = 0
final_count = 0

for index, row in df.iterrows():
  index -= 32
  q = row.question
  a = [row.answer1, row.answer2, row.answer3]
  res = hqbot.query(q, a)

  res_guess = np.argmax(res['total_res']) +1
  fp_guess  = np.argmax(res['front_page'])+1
  nlp_guess = np.argmax(res['nlp_res'])   +1

  if "not" in q.lower():
    res_guess = np.argmin(res['total_res']) +1
    fp_guess  = np.argmin(res['front_page'])+1
    nlp_guess = np.argmin(res['nlp_res'])   +1

  print(res['total_res'])
  print(res_guess)

  if len(set(res['front_page'])) == 1:
    final_guess = nlp_guess
  elif len(set(res['nlp_res'])) == 1:
    final_guess = res_guess
  elif len(set(res['total_res'])) == 1:
    final_guess = randint(1,3)
  else:
    final_guess = fp_guess

  if res_guess == int(row.correct): res_count += 1
  if fp_guess  == int(row.correct): fp_count  += 1
  if (res_guess==int(row.correct)) or (fp_guess==int(row.correct)):
    tot_count += 1
  if nlp_guess   == int(row.correct): nlp_count  += 1
  if final_guess == int(row.correct): final_count += 1

  print('='*30)
  print('Question: {}'.format(q))
  print('\n')
  print('Total Results: {}/{} -- {}%'.format(res_count,index+1,round((res_count/(index+1))*100)))
  print('Front Page: {}/{} -- {}%'.format(fp_count,index+1,round((fp_count/(index+1))*100)))
  print('Both Methods: {}/{} -- {}%'.format(tot_count,index+1,round((tot_count/(index+1))*100)))
  print('NLP Results: {}/{} -- {}%'.format(nlp_count,index+1,round((nlp_count/(index+1))*100)))
  print('Finalized Method: {}/{} -- {}%'.format(final_count,index+1,round((final_count/(index+1))*100)))
  print('\n')

  time.sleep(randint(12,22))