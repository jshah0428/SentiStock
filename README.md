# SentiStock - Stock Market Sentiment Analyzer

## Background

SentiStock was inspired by my long-standing interest in the stock market and my experiences as a high school senior, when I started investing heavily. I observed that many people lacked the resources to make informed investment decisions. This gap inspired me to create SentiStock—a tool designed to empower investors with actionable insights into stock sentiment.

---

## Motivation

The project was driven by the realization that accurate, reliable sentiment analysis is critical for informed stock market decisions. Many available tools offered vague recommendations without context or relied on incomplete data sources. SentiStock was developed to address these challenges by providing clear, data-driven buy/hold/sell recommendations with supporting summaries and source links.

---

## Technologies Used

- **Python Libraries**
  - `Flask`: Backend framework for API and UI integration.
  - `Transformers` (Hugging Face): 
    - `ProsusAI/finbert`: Sentiment analysis model tailored for financial data.
    - `facebook/bart-large-cnn`: Summarization model for condensing article content.
  - `Requests`: For API calls and data retrieval.
  - `JSON`: Configuration and key storage.

- **APIs**
  - `SerpAPI`: Fetches relevant article links from Google News.
  - `DiffBot API`: Extracts full text from the fetched articles.

- **Frontend**
  - HTML, CSS, and JavaScript: User interface for stock ticker input and results display.

---

## Features

1. **Dynamic News Retrieval**  
   - Fetches the top 3 recent, relevant news articles for a given stock ticker using SerpAPI(Only 3 due to API limits).  

2. **Article Summarization**  
   - Summarizes articles with the `facebook/bart-large-cnn` model to extract key points.  

3. **Sentiment Analysis**  
   - Processes summarized text with `ProsusAI/finbert` to generate a buy/hold/sell recommendation.  

4. **User Interface**  
   - Provides an intuitive web interface for users to input stock tickers and receive:
     - A recommendation.
     - A detailed summary of the analysis.
     - Links to the original articles.

5. **Comprehensive Feedback**  
   - Combines summarized content with sentiment results to ensure transparent decision-making.

---

## Ultimate Goal

The ultimate goal of SentiStock is to provide beginner investors with a powerful tool for making informed stock market decisions. By offering transparent recommendations backed by detailed analysis and source information, SentiStock seeks to bridge the knowledge gap and make financial insights accessible to everyone. Future enhancements aim to optimize speed, improve accuracy, and add features like user accounts, watchlists, and a mock stock market dashboard.

---
