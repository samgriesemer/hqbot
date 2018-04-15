# hqbot
an experimental (only) bot for the live HQ Trivia game

### How it works
The script utilizes Pytesseract to perform OCR on live screenshots of HQ trivia. The script continually runs until it recognizes a question in the screenshot, at which point it seeds three types of search heuristics to Google. The results of these searches are parsed and weighted, and used in conjunction with word saliency estimates from Google's NLP API. The script then returns the best of the three answers according to the above metrics.

### How to use
to be detailed
