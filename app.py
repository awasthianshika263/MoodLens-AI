from flask import Flask, render_template, request, session
from flask_session import Session  # new import
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Session setup (very important - har user ke liye alag data)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')  # random strong key daal
app.config['SESSION_TYPE'] = 'filesystem'  # simple file-based session
Session(app)

# Azure setup (same as before)
key = os.getenv("AZURE_KEY")
endpoint = os.getenv("AZURE_ENDPOINT")
credential = AzureKeyCredential(key) if key else None
client = TextAnalyticsClient(endpoint=endpoint, credential=credential) if key and endpoint else None

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    sentences = []
    confidence = None

    # Har user ke liye alag history (session se)
    if 'history' not in session:
        session['history'] = []

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

                # History session mein add karo (global nahi)
                session['history'].append({
                    "text": user_input,
                    "sentiment": doc.sentiment.upper()
                })
                session.modified = True  # important - session update ho

            except Exception as e:
                print("Azure Error:", e)

    return render_template(
        "index.html",
        result=result,
        sentences=sentences,
        history=session.get('history', []),  # session se history bhej
        confidence=confidence
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)