import cv2
import matplotlib.pyplot as plt
import numpy
import pytesseract
import nltk
import re

def ocr_operation(input_file):
    image = cv2.imread(input_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mser = cv2.MSER_create()
    regions, _ = mser.detectRegions(gray)
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

    sentences = []
    for i, region in enumerate(regions):
        x, y, w, h = cv2.boundingRect(region)
        if w>2 and h>50:
            cropped_img = gray[y:y+h, x:x+w] 
            sentence = pytesseract.image_to_string(cropped_img, lang='eng')
            sentence = sentence.strip()
            if sentence:  
                sentences.append(sentence)


    sentence = ' '.join(sentences) 
    cleaned_content = re.sub(r'[^\.\?\!\w\d\s]','',sentence)
    cleaned_content = cleaned_content.lower()
    word_tokens = nltk.word_tokenize(cleaned_content)
    print(word_tokens)
    
    return sentence



