import numpy as np
import pandas as pd
import time

from TriviaBot import TriviaBot

df = pd.read_csv('questions.csv')
hqbot = TriviaBot()

while True:
  hqbot.ocr(998,160,1424,580,200)
  if hqbot.is_valid_q:
    print('='*10+' Official Question '+'='*10)
    print('Question: ' + repr(hqbot.q))
    for ans in hqbot.a:
      print('Answer: ' + ans)

    entry = [hqbot.q, hqbot.a[0], hqbot.a[1], hqbot.a[2], None, None]
    new_df = pd.DataFrame([entry], columns=df.columns)
    df = df.append(new_df, ignore_index=True)
    df.to_csv('questions.csv', index=False)
    time.sleep(20)
  else:
    print('Is not valid question.')