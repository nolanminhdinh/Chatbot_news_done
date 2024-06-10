import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy as np
import joblib
import json
import random
from flask import Flask, render_template, request
import mtranslate

# Load dữ liệu tin tức
with open('news_scrap_data.json', encoding='utf-8') as file:
    news_scrap_data = json.load(file)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def chatbot_response(msg):
    if 'tin tức' in msg.lower():
        random.shuffle(news_scrap_data['intents'])  # Xáo trộn danh sách tin tức
        news_responses = []
        for news in news_scrap_data['intents']:
            title = news['title']
            summary = news['summary']
            category= news['category']
            link = news['news_link']
            news_responses.append(f"<strong>Tiêu đề:</strong>{title}<br> \n <strong>Nội dung:</strong> {summary}<br> \n <strong>Chủ đề:</strong> {category}<br> \n <a href='{link}' target='_blank'>Xem thêm</a><br><br>")
            break 
        return "".join(news_responses)




app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

if __name__ == "__main__":
    app.run(debug=True)

