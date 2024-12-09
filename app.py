from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import requests, datetime
import serpapi
import json
app = Flask(__name__)

sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", max_length=300, min_length=30)


with open('/Users/jainamshah/PycharmProjects/Financial sentiment analyzer/keys.json', 'r') as file:
    secrets = json.load(file)


def fetch_link(stock_ticker):
    url_list = []
    params = {
        "engine": "google_news",
        "q": stock_ticker,
        "gl": "us",
        "hl": "en",
        "no_cache": False,
        "api_key": secrets["serp"]
    }
    search = serpapi.search(params)
    counter = 0 #counts number of items in url_list
    index = 0 #parses through search results.
    while (counter!=3):
        try:
            url_list.append(search["news_results"][index]['link'])
            counter+=1
        except IndexError:
            break
        except KeyError:
            continue
        finally:
            index+=1
    return url_list


def get_text(url_list):
    final_text_per_art =[]
    api_token = secrets["diff_bot"]

    for url_2 in url_list:
        try:
            url = f"https://api.diffbot.com/v3/analyze?url={url_2}&token={api_token}"
            #headers = {"accept": "application/json"}
            response = requests.get(url)
            data = response.json().get('objects', [])
            final_text_per_art.append(data[0]['text'])
        except:
            continue
    return final_text_per_art


def generate_summary(texts): #tests is a list
    # Truncate text to 512 tokens for BART model
    article_summs = []
    for text in texts:
        max_length = 512
        truncated_text = text[:max_length * 4]  # Rough approximation of tokens to characters
        try:
            summary = summarizer(truncated_text, max_length=300, min_length=30, do_sample=False)
            # print(summary[0]["summary_text"])
            article_summs.append(summary[0]["summary_text"])

        except Exception as e:
            # print(f"Summarization error: {str(e)}")
            return "Unable to generate summary due to text length."

    joined_text = " ".join(article_summs)

    try:
        final_summary = summarizer(joined_text, max_length=300, min_length=50, do_sample=False)
        # print(final_summary[0]["summary_text"])
    except Exception as e:
        # print(f"Error summarizing the combined summary: {str(e)}")
        return "Unable to generate final summary."

    return article_summs, joined_text


def analyze_sentiment(text):

    all_results = []
    results = sentiment_analyzer(text)
    all_results.extend(results)

    print(all_results)

    # Count sentiments across all chunks
    positive_count = sum(1 for r in all_results if r['label'] == 'positive')
    neutral_count = sum(1 for r in all_results if r['label'] == 'neutral')
    negative_count = sum(1 for r in all_results if r['label'] == 'negative')

    if positive_count > negative_count and positive_count > neutral_count:
        recommendation = "Buy"
    elif negative_count > positive_count and negative_count > neutral_count:
        recommendation = "Sell"
    else:
        recommendation = "Hold"

    return recommendation, all_results


@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')


@app.route("/analyze", methods=["POST"])
def analyze_stock():
    data = request.json
    stock_ticker = data.get("ticker")

    news_links = fetch_link(stock_ticker)  # this should get url's
    news_text = get_text(news_links)#theres a repeates list thing happening here, idk why. look into this.

    summaries, joined_text = generate_summary(news_text)  # list of summaries and total summaries.
    recommendation, sentiment_results = analyze_sentiment(joined_text)

    # Create a list of article summaries with links
    article_summaries = [{"link": link, "summary": summary} for link, summary in zip(news_links, summaries)]

    response = {
        "ticker": stock_ticker,
        "recommendation": recommendation,
        "summary": joined_text,
        "article_summaries": article_summaries
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(port = 5001, debug=True)