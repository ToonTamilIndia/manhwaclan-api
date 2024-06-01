# Manhwaclan API

Welcome to the manhwaclan API! This API provides comprehensive access to information about Manga, Manhwa, and Manhua. Data is meticulously scraped from  manhwaclan, with the capability to gather data from multiple manga websites utilizing the madara themes in Wordpress.

## Features

- **Manga Data**: Access detailed information about manga, including chapter lists, release dates, and more.
- **Search Functionality**: Search for specific manga titles and retrieve detailed information.
- **Genre Details**: Explore manga genres and retrieve relevant details.
- **Chapter Data**: Obtain images and related data for specific chapters.
- **Support**: Visit our [Telegram Support Channel](https://telegram.me/toontamilindia) for assistance and questions.

## The other Website compatible with this api

- **[harimanga](https://harimanga.com/)**
- **[kunmanga](https://kunmanga.com/)**
- **[harimanga.io](https://harimanga.io/)**

## Routes

- **`/manga` or `/manga?pages={page_number}`**: Retrieve the home page of the manhwaclan.
- **`/search/{query}` or `/search/{query}?page={page_number}`**: Search for manga titles and receive detailed information.
- **`/manga/{id}`**: Access information about a specific manga, including chapter lists, release dates, etc.
- **`/manga/{id}/{chapter_id}`**: Retrieve images and related data for a specific chapter.
- **`/genre/{id}` or `/genre/{id}?page={page_number}`**: Explore manga genres and retrieve relevant details.

## Examples

### Example 1: Search for Manga

```http
GET /search/one piece
```

### Example 2: Retrieve Manga Information

```http
GET /manga/imprisoned-one-million-years-my-disciples-are-all-over-the-world
```
### Example 3: Retrieve Chapter Data

```http
GET /manga/one-day-i-found-a-husband/chapter-1
```
## Deployment Guide

### Local Deployment

1. Clone the repository: `git clone https://github.com/ToonTamilIndia/manhwaclan-api.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

### Vercel Deployment (Using CLI)

1. Install Vercel CLI: `npm install -g vercel`
2. Navigate to the project directory: `cd <project_directory>`
3. Deploy to Vercel: `vercel --prod`

Visit the deployed example at [manhwaclan.vercel.app](https://manhwaclan.vercel.app/).

## Support and Contact

For any further assistance, inquiries, don't hesitate to reach out to us through our [Telegram Support Channel](https://telegram.me/toontamilindia).

## Credits

This project is built with [Flask](https://flask.palletsprojects.com/) for the backend and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for web scraping.






