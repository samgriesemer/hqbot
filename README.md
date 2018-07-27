# HQbot

HQbot is a bot that attempts to retrieve the best answer to a given trivia question from the live HQ Trivia game show.

## Details

The script utilizes Pytesseract to perform OCR on live screenshots of HQ trivia. The script continually runs until it recognizes a question in the screenshot, at which point it seeds three types of search heuristics to Google. The results of these searches are parsed and weighted, and used in conjunction with word saliency estimates from Google's NLP API. The script then returns the best of the three answers according to the above metrics.

## Pipeline 

1. The script takes a screenshot of the player's phone while HQTrivia is live
2. The image is passed to Pytesseract OCR to recognize text in the image
3. If the text is recognized as the proper question answer format, it moves to step 4, else back to step 1
4. The question and three answers are parsed and used to stage a variety of search heuristics
5. The searches are sent to Google and raw HTML is returned
6. BeautifulSoup is used to strip out relevant information from the search results
7. These results are analyzed and weighted according to the search heuristic
8. The search results are combined with word saliency estimates from Google's NLP API to better refine predictions
9. The best answer is determined and displayed to the user via the terminal

This process takes ~4 seconds to complete, leaving a few seconds to tap the answer on the screen.

## Usage
