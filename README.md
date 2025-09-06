# 🐦 TechieTweeter – Daily Tech News Bot 🚀  

> Bringing you the hottest **Tech News** straight to **Twitter (X)** – every single day! 💻⚡  

---

## ✨ What is TechieTweeter?  
TechieTweeter is a funky little Python bot that:  
- 📰 Fetches **top tech headlines** from [NewsAPI](https://newsapi.org)  
- 🐦 Posts them automatically to your **Twitter (X)** account  
- ⏰ Can be scheduled with Windows Task Scheduler / Cron to run **daily**  
- 💾 Logs everything to a file so you never miss a beat  

---

## 🔧 Tech Stack  
- 🐍 **Python 3.10+**  
- 🌐 **Requests** – grab news from APIs  
- 🐦 **Tweepy** – post tweets like a pro  
- 🔑 **python-dotenv** – keep your API keys safe  
- 📜 **Task Scheduler** – automate the daily magic  

---

## ⚡ Setup  

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/autochirp.git
   cd autochirp
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API keys**  
   Create a `.env` file in the project root:  
   ```env
   NEWS_API_KEY=your_newsapi_key_here
   X_API_KEY=your_twitter_api_key
   X_API_KEY_SECRET=your_twitter_api_key_secret
   X_ACCESS_TOKEN=your_access_token
   X_ACCESS_TOKEN_SECRET=your_access_token_secret
   X_BEARER_TOKEN=your_bearer_token
   ```

4. **Run the bot** manually:  
   ```bash
   python daily_tech_news.py
   ```

5. **Automate it**  
   - On Windows → use **Task Scheduler**  
   - On Linux/Mac → use **cron jobs**  

---

## 📝 Example Tweet  

```
Daily Tech News:
1. AI chatbots are not your friends – Computerworld
https://computerworld.com/article/405070...

#TechNews (via NewsAPI.org)
```

---

## 🚀 Roadmap (Future Ideas)  
- 🎨 Add images/thumbnails to tweets  
- 🔥 Hot Takes mode: add spicy commentary with the headlines  
- 📊 Analytics tracking (likes, retweets, impressions)  

---

## 💡 Inspiration  
Because why scroll endlessly when a bot can do the job for you? 😉  

---

## 📜 License  
MIT – Free to use, hack, and share.  

---

Made with ❤️ and ☕ by [Rakshit](https://github.com/Rakshit05code)  
