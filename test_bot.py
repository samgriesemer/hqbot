from TriviaBot import TriviaBot
import time
import numpy as np

hqbot = TriviaBot()

while True:
  hqbot.ocr(998,160,1424,580,200)

  if hqbot.is_valid_q is False:
    print('No question in screenshot.')
    continue
  else:
    print('='*10+' Official Question '+'='*10)
    res = hqbot.query(hqbot.q, hqbot.a)

    res_guess = np.argmax(res['total_res'])
    fp_guess  = np.argmax(res['front_page'])
    #nlp_guess = np.argmax(res['nlp_res'])

    if "not" in hqbot.q.lower():
      res_guess = np.argmin(res['total_res'])
      fp_guess  = np.argmin(res['front_page'])
      #nlp_guess = np.argmin(res['nlp_res'])

    if len(set(res['front_page'])) == 1:
      final_guess = res_guess
    #elif len(set(res['nlp_res'])) == 1:
      #final_guess = res_list
    elif len(set(res['total_res'])) == 1:
      final_guess = randint(1,3)
    else:
      final_guess = fp_guess

    print("*** Best Answer: {} ***".format(hqbot.a[final_guess]))
    time.sleep(10)