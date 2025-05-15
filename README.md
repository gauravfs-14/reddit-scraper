# Reddit Scraper

This project is a Python-based scraper for Reddit posts using the PRAW (Python Reddit API Wrapper) library. It allows users to search for specific terms in designated subreddits and saves the relevant posts to a SQLite database.

## Project Structure

```
reddit-scraper
├── main.py            # Main logic for scraping Reddit posts
├── environment.yml    # Conda environment configuration
├── .env               # Environment variables (API keys and secrets)
├── README.md          # Project documentation
└── .gitignore         # Files and directories to ignore in Git
```

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/gauravfs-14/reddit-scrapper.git
   cd reddit-scraper
   ```

2. **Create the conda environment:**
   Make sure you have Conda installed. Then run:

   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the environment:**

   ```bash
   conda activate reddit-scraper
   ```

4. **Set up your environment variables:**
   Create a `.env` file in the project root and add your Reddit API credentials:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_SECRET=your_client_secret
   REDDIT_USERNAME=your_username
   REDDIT_PASSWORD=your_password
   USER_AGENT=RedditScraper by u/your_username
   ```

## Usage

Run the scraper by executing the following command:

```bash
python main.py
```

The scraper will search for the specified terms in the defined subreddits and save the posts to a SQLite database named `reddit_posts.db`.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
