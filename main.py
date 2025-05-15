import praw
import sqlite3
import time
from tqdm import tqdm
from dotenv import load_dotenv
import os

# === LOAD ENVIRONMENT VARIABLES ===
load_dotenv()

# === CONFIGURATION ===
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
USER_AGENT = os.getenv("USER_AGENT")

SEARCH_TERMS = [
    "Tesla FSD",
    "Full Self Driving",
    "FSD Beta",
    "FSD update",
    "Tesla Autopilot",
    "Navigate on Autopilot",
    "Tesla Vision",
    "Autonomous Tesla",
    "Self-driving Tesla",
    "Tesla Level 5",
    "Autopilot crash",
    "Autopilot disengagement",
    "Elon FSD",
    "Tesla robotaxi",
    "Tesla self-driving",
    "Tesla AI Day",
    "FSD subscription"
]
SUBREDDITS = ["TeslaModel3", "TeslaLounge", "teslamotors", "TeslaModelY", "teslamotors", "SelfDrivingCars"]
POST_LIMIT = 1000

# === RATE LIMIT SETTINGS ===
MAX_REQUESTS_PER_MINUTE = 95
DELAY_BETWEEN_REQUESTS = 60 / MAX_REQUESTS_PER_MINUTE  # ~0.63 seconds

# === SETUP DATABASE ===
conn = sqlite3.connect("reddit_posts.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS reddit_posts (
    id TEXT PRIMARY KEY,
    title TEXT,
    selftext TEXT,
    author TEXT,
    created_utc INTEGER,
    subreddit TEXT,
    url TEXT,
    score INTEGER,
    num_comments INTEGER
)
''')
conn.commit()

# === SETUP REDDIT API ===
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

# === FUNCTION TO SAVE POSTS ===
def save_post(post):
    try:
        cursor.execute('''
        INSERT OR IGNORE INTO reddit_posts (id, title, selftext, author, created_utc, subreddit, url, score, num_comments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            post.id,
            post.title,
            post.selftext,
            str(post.author),
            int(post.created_utc),
            post.subreddit.display_name,
            post.url,
            post.score,
            post.num_comments
        ))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] Failed to insert post {post.id}: {e}")

# === SCRAPER ===
def scrape():
    for subreddit in SUBREDDITS:
        for term in SEARCH_TERMS:
            print(f"\n🔍 Searching '{term}' in r/{subreddit}...")
            sub = reddit.subreddit(subreddit)
            try:
                for post in tqdm(sub.search(term, sort="new", limit=POST_LIMIT)):
                    save_post(post)
                    time.sleep(DELAY_BETWEEN_REQUESTS)
            except Exception as e:
                print(f"[ERROR] Skipping due to: {e}")
                time.sleep(10)

if __name__ == "__main__":
        # Check if environment variables are loaded correctly
    if not all([REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, USER_AGENT]):
        print("ERROR: Missing environment variables. Please check your .env file.")
        exit(1)
        
    scrape()
    conn.close()
    print("\n✅ Done! Posts saved to reddit_posts.db.")
