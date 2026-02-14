# MoodLens AI 🚀

**Real-time Sentiment Analysis Web App** built with **Flask** and powered by **Azure Text Analytics**.  
Type any feedback or text → Instantly get sentiment (Positive, Negative, Neutral), confidence score, visualizations (pie chart & progress bars), sentence-level breakdown, and analysis history.

**Live Demo:** [https://moodlensai-anshika263.azurewebsites.net](https://moodlensai-anshika263.azurewebsites.net)  
**GitHub Repository:** [https://github.com/awasthianshika263/MoodLens-AI](https://github.com/awasthianshika263/MoodLens-AI)

---

## Features

- Real-time sentiment detection (POSITIVE, NEGATIVE, NEUTRAL)  
- Confidence percentage & dominant sentiment display  
- Progress bars for Positive / Neutral / Negative distribution  
- Interactive pie chart using Chart.js  
- Sentence-by-sentence sentiment breakdown (opinion mining)  
- Analysis history (current session)  
- One-click **Copy Result** feature  
- Modern dark theme with glassmorphism UI  

---

## Tech Stack

**Frontend**  
- HTML5, CSS3 (Poppins font, gradient background, glassmorphism)  
- JavaScript + Chart.js  

**Backend**  
- Python 3.12  
- Flask (web framework)  
- Azure AI Text Analytics (sentiment & opinion mining API)  

**Deployment**  
- Azure App Service (Linux, Python 3.12 runtime, F1 free tier)  
- Gunicorn (WSGI server)  
- Deployed in Central India region  

**Python Libraries**  
- `flask`  
- `azure-ai-textanalytics`  
- `azure-core`  
- `python-dotenv`  
- `gunicorn`  

---

## Local Setup Instructions

1. **Clone the repository:**
```bash
  git clone https://github.com/awasthianshika263/MoodLens-AI.git
  cd MoodLens-AI

2. **Create and activate a virtual environment:**

  python -m venv venv

  # Windows
  venv\Scripts\activate

  # Linux / Mac
  # source venv/bin/activate


3. **Install dependencies:**

  pip install -r requirements.txt


4. **Create a .env file in the root directory:**

  AZURE_KEY=your-azure-text-analytics-key
  AZURE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/


5. **Run the application locally:**

  python app.py


6. **Open in browser:**

  http://localhost:8000



Azure Deployment Steps:

1. Install Azure CLI and login:
   az login

2. Deploy from project folder (Central India region used for student subscription):
   az webapp up --name moodlensai-anshika263 --runtime "PYTHON|3.12" --sku F1 --logs --location centralindia

3. In Azure Portal → App Services → moodlensai-anshika263 → Configuration → Application settings:
   Add: AZURE_KEY = [your key]
   Add: AZURE_ENDPOINT = [your endpoint]
   Add: SCM_DO_BUILD_DURING_DEPLOYMENT = true

4. In General settings / Stack settings:
   Startup Command:
     gunicorn --bind=0.0.0.0:$PORT app:app

5. Save and Restart the app.


Challenges & Solutions:
  Azure for Students subscription had region restrictions → Used centralindia (allowed region)
  Startup command not working initially → Set gunicorn --bind=0.0.0.0:$PORT app:app
  History resets on app restart → Currently in-memory (future enhancement: add database)


Future Enhancements:
  Persistent history using SQLite or Azure Cosmos DB
  User authentication and personal history
  Multi-language sentiment analysis
  Emotion detection (happy, sad, angry, etc.)
  Mobile app version
  Custom domain integration
