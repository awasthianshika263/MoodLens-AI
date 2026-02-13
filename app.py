from flask import Flask, render_template, request
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Load Azure credentials from environment
key = os.getenv("AZURE_KEY")
endpoint = os.getenv("AZURE_ENDPOINT")

if not key or not endpoint:
    print("WARNING: Azure credentials not found. Check environment variables.")

credential = AzureKeyCredential(key) if key else None
client = TextAnalyticsClient(endpoint=endpoint, credential=credential) if key and endpoint else None

history = []

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    sentences = []
    confidence = None

    if request.method == "POST":
        user_input = request.form.get("feedback")

        if user_input and client:
            try:
                response = client.analyze_sentiment(
                    [user_input],
                    show_opinion_mining=True
                )

                doc = response[0]

                positive = round(doc.confidence_scores.positive * 100, 2)
                neutral = round(doc.confidence_scores.neutral * 100, 2)
                negative = round(doc.confidence_scores.negative * 100, 2)

                result = {
                    "sentiment": doc.sentiment.upper(),
                    "positive": positive,
                    "neutral": neutral,
                    "negative": negative
                }

                confidence = max(positive, neutral, negative)

                for sentence in doc.sentences:
                    sentences.append({
                        "text": sentence.text,
                        "sentiment": sentence.sentiment.upper()
                    })

                history.append({
                    "text": user_input,
                    "sentiment": doc.sentiment.upper()
                })

            except Exception as e:
                print("Azure Error:", e)

    return render_template(
        "index.html",
        result=result,
        sentences=sentences,
        history=history,
        confidence=confidence
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
