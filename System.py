import os
import argparse
import base64
import fnmatch

import requests
import tensorflow as tf
from elasticsearch import Elasticsearch, helpers
from nltk.sentiment import SentimentIntensityAnalyzer

import config

GITHUB_TOKEN = config.GITHUB_ACCESS_TOKEN
ES_INDEX = "knowledge_base"

sia = SentimentIntensityAnalyzer()

def parse_github_url(url):
    parts = url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo

def get_files_from_github_repo(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        return content["tree"]
    else:
        raise ValueError(f"Error fetching repo contents: {response.status_code}")

def fetch_md_contents(files):
    md_contents = []
    for file in files:
        if file["type"] == "blob" and fnmatch.fnmatch(file["path"], "*.md"):
            response = requests.get(file["url"])
            if response.status_code == 200:
                content = response.json()["content"]
                decoded_content = base64.b64decode(content).decode("utf-8")
                md_contents.append(decoded_content)
            else:
                print(f"Error downloading file {file['path']}: {response.status_code}")
    return md_contents

def summarize_content_with_tensorflow(contents):
    # This is a placeholder. Ideally, you'd use a TensorFlow-based model for summarization.
    summarized_contents = [content[:min(500, len(content))] for content in contents]
    return summarized_contents

def analyze_sentiment_with_nltk(contents):
    sentiment_scores = [sia.polarity_scores(content) for content in contents]
    return sentiment_scores

def index_to_elasticsearch(contents, sentiments):
    es = Elasticsearch()
    if not es.indices.exists(ES_INDEX):
        es.indices.create(index=ES_INDEX)

    actions = [
        {
            "_index": ES_INDEX,
            "_source": {
                "content": content,
                "sentiment": sentiment
            }
        }
        for content, sentiment in zip(contents, sentiments)
    ]
    helpers.bulk(es, actions)

def main():
    parser = argparse.ArgumentParser(description="Fetch all *.md files from a GitHub repository.")
    parser.add_argument("repo_url", help="GitHub repository URL")

    args = parser.parse_args()

    GITHUB_OWNER, GITHUB_REPO = parse_github_url(args.repo_url)

    all_files = get_files_from_github_repo(GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)

    md_contents = fetch_md_contents(all_files)
    summarized_contents = summarize_content_with_tensorflow(md_contents)
    sentiments = analyze_sentiment_with_nltk(md_contents)
    index_to_elasticsearch(summarized_contents, sentiments)

    print("Successfully indexed content to Elasticsearch.")

if __name__ == "__main__":
    main()
