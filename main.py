from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

base_url = 'https://manhuatop.org/'

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        return None

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Manhwaclan API</title>
        <style>
            body {
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f8f9fa;
                color: #495057;
                line-height: 1.6;
            }

            header {
                background-color: #343a40;
                color: #fff;
                text-align: center;
                padding: 1.5em 0;
                margin-bottom: 1em;
            }

            h1 {
                margin-bottom: .5em;
                font-size: 2em;
                color: #17a2b8;
            }

            p {
                color: #6c757d;
                margin-bottom: 1.5em;
            }

            code {
                background-color: #f3f4f7;
                padding: .2em .4em;
                border-radius: 4px;
                font-family: "Courier New", Courier, monospace;
                color: #495057;
            }

            .container {
                margin: 1em;
                padding: 1em;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, .1);
            }

            li, ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }

            li {
                margin-bottom: .5em;
            }

            li code {
                background-color: #e5e7eb;
                color: #495057;
            }

            a {
                color: #17a2b8;
                text-decoration: none;
            }

            a:hover {
                text-decoration: underline;
            }

            footer {
                background-color: #343a40;
                color: #fff;
                padding: 1em 0;
                text-align: center;
            }

            .sample-request {
                margin-top: 1em;
            }

            .toggle-response {
                cursor: pointer;
                color: #17a2b8;
                text-decoration: underline;
            }

            .sample-response {
                display: none;
                margin-top: 1em;
            }

            pre {
                background-color: #f3f4f7;
                padding: 1em;
                border-radius: 4px;
                overflow-x: auto;
            }
        </style>
    </head>
    <body>
    <header>
        <h1>API Dashboard</h1>
        <p>This API provides access to a information of Manga data.</p>
        <p class="support">For support, visit our <a href="https://telegram.me/toontamilindia" target="_blank" rel="noopener">Telegram</a>.</p>
    </header>
    <div class="container">
        <h2>API Description:</h2>
        <p>This API provides access to a information of Manga, Manhwa, Manhua data, Data is scraped from manhwaclan but it's also able to scrap data from lot of manga websites which are all used madara themes in wordpress.</p>
    </div>
    <div class="container">
        <h2>Routes:</h2>
        <ul>
            <li><code>/manga or /manga?pages={page_number}</code> - The home page of the manhwaclan</li>
            <li><code>/search/{quary} or /search/{quary}?page={page_number}</code> - it return the searched manga details</li>
            <li><code>/manga/{id}</code> - The information about manga and chapter list, release date etc</li>
            <li><code>/manga/{id}/{chapter_id}</code>  - it return images data and next_chapter ,previous_chapter data </li>
            <li><code>/genre/{id} or /genre/{id}?page={page_number}</code> - it return the genre details</li>

        </ul>
    </div>
    <div class="container">
        <h2>Support and Contact:</h2>
        <p>For support and questions, visit our <a href="https://telegram.me/toontamilindia" target="_blank" rel="noopener">Telegram Support Channel</a>.</p>
    </div>
    <footer>
        <p>© 2024 ToonTamilIndia. All rights reserved.</p>
    </footer>
    </body>
    </html>
    '''

@app.route("/search/<search_query>", methods=["GET"])
def search_manga(search_query):
    page = request.args.get('page', 1)
    url = f"{base_url}page/{page}/?s={search_query}&post_type=wp-manga"
    soup = fetch_page(url)
    if not soup:
        return jsonify({"message": "Failed to retrieve data"}), 500
    
    manga_list = []
    manga_container = soup.find_all('div', class_='row c-tabs-item__content')
    for manga in manga_container:
        title_tag = manga.find('h3', class_='h4')
        if title_tag:
            title = title_tag.text.strip()
            manga_url = title_tag.find('a')['href']
            manga_id_parts = manga_url.split('/')
            manga_id = manga_id_parts[-2]
            # Extracting other details
            cover_url = manga.find('img')['src']
            latest_chapter = manga.find('span', class_='chapter').text.strip()
            rating = manga.find('span', class_='score').text.strip()

            manga_list.append({
                'title': title,
                'manga_id': manga_id,
                'manga_url': manga_url,
                'cover_url': cover_url,
                'latest_chapter': latest_chapter,
                'rating': rating
            })
    
    return jsonify(manga_list)


    
@app.route("/manga", methods=["GET"])
def get_manga_list():
    page = request.args.get('page', 1)
    url = f"{base_url}page/{page}/"
    soup = fetch_page(url)
    if not soup:
        return jsonify({"message": "Failed to retrieve data"}), 500
    
    manga_list = []
    manga_container = soup.find_all('div', class_='page-item-detail')
    for manga in manga_container:
        cover_tag = manga.find('img')
        title_tag = manga.find('a', title=True)
        if title_tag and cover_tag:
            title = title_tag['title']
            manga_id = title_tag['href'].split('/')[-2]
            cover_url = cover_tag['src']
            manga_list.append({'id': manga_id, 'title': title, 'cover': cover_url})
    
    return jsonify(manga_list)

@app.route("/manga/<id>", methods=["GET"])
def get_manga_details(id): # Replace with your base URL
    url = f"{base_url}manga/{id}"
    soup = fetch_page(url)
    if not soup:
        return jsonify({"message": "Failed to retrieve data"}), 500
    
    details = {'id': id}

    # Extract title
    title_tag = soup.find('div', class_='post-title')
    details['title'] = title_tag.h1.text.strip() if title_tag and title_tag.h1 else "N/A"

    # Extract author and release year
    details['author'] = "N/A"
    details['release_year'] = "N/A"
    genre_list = []
    for genre_tag in soup.find_all('a', rel='tag'):
        genre_text = genre_tag.text.strip()
        if any(char.isdigit() for char in genre_text):
            details['release_year'] = genre_text
        elif " - " in genre_text:
            details['author'] = genre_text
        else:
            genre_list.append(genre_text)
    details['genres'] = genre_list

    # Extract alternative titles
    alt_titles_tag = soup.find('div', class_='summary-content')
    details['alternative'] = alt_titles_tag.text.strip() if alt_titles_tag else "N/A"

    # Extract status
    status_tag = soup.find('div', class_='post-content_item', string="Status")
    if status_tag:
        status = status_tag.find_next('div', class_='summary-content')
        details['status'] = status.text.strip() if status else "N/A"
    else: 
        details['status'] = "N/A"

    # Extract summary
    summary_tag = soup.find('div', class_='description-summary')
    summary_content = summary_tag.find('div', class_='summary__content') if summary_tag else None
    if summary_content:
        # Extract only the text within the summary__content div
        summary_text = summary_content.text.strip()
        details['summary'] = summary_text
    else:
        details['summary'] = "N/A"

    # Extract chapters and their release dates
    chapters = []
    chapter_list = soup.find('div', class_='listing-chapters_wrap')
    chapter_items = chapter_list.find_all('li', class_='wp-manga-chapter') if chapter_list else []
    for chapter in chapter_items:
        chapter_title = chapter.a.text.strip()
        chapter_url = chapter.a['href']
        chapter_id = chapter_url.split('/')[-2]
        release_date = chapter.find('span', class_='chapter-release-date').text.strip()
        chapters.append({
            'title': chapter_title,
            'release_date': release_date,
            'chapter_id': chapter_id
        })

    details['chapters'] = chapters

    # Additional details like rating, rank, first and last chapters
    rating_tag = soup.find('span', class_='score')
    details['rating'] = rating_tag.text.strip() if rating_tag else "N/A"

    rank_tag = soup.find('span', class_='rank')
    details['rank'] = rank_tag.text.strip() if rank_tag else "N/A"
    
    chapter_container = soup.find('ul', class_='main')
    chapter_items = chapter_container.find_all('li') if chapter_container else []
    details['first_chapter'] = chapter_items[-1].find('a')['href'].split('/')[-2] if chapter_items else "N/A"
    details['last_chapter'] = chapter_items[0].find('a')['href'].split('/')[-2] if chapter_items else "N/A"

    return jsonify(details)

from flask import request

@app.route("/genre/<genreid>", methods=["GET"])
def get_genre_details(genreid):
    page = request.args.get('page', default=1, type=int)
    url = f"{base_url}manga-genre/{genreid}/page/{page}"
    soup = fetch_page(url)
    if not soup:
        return jsonify({"message": "Failed to retrieve data"}), 500
    
    genre_details = []
    manga_container = soup.find_all('div', class_='page-item-detail')
    for manga in manga_container:
        cover_tag = manga.find('img')
        title_tag = manga.find('a', title=True)
        chapter_tag = manga.find('a', class_='btn-link')
        rating_tag = manga.find('span', class_='score')
        date_tag = manga.find('span', class_='post-on')
        
        if title_tag and cover_tag and chapter_tag:
            title = title_tag['title']
            manga_id = title_tag['href'].split('/')[-2]
            cover_url = cover_tag['src']
            chapters = chapter_tag.text.strip()
            chapter_id = chapter_tag['href'].split('/')[-2]
            rating = rating_tag.text.strip() if rating_tag else 'N/A'
            date = date_tag.text.strip() if date_tag else 'N/A'
            genre_details.append({'name': title, 'cover': cover_url, 'chapters': chapters, 'chapter_id': chapter_id, 'manga_id': manga_id, 'rating': rating, 'date': date})
    
    return jsonify(genre_details)


@app.route("/manga/<id>/<chapterid>", methods=["GET"])
def get_chapter_images(id, chapterid):
    url = f"{base_url}manga/{id}/{chapterid}"
    soup = fetch_page(url)
    if not soup:
        return jsonify({"message": "Failed to retrieve data"}), 500
    
    image_urls = []
    image_container = soup.find('div', class_='reading-content')
    images = image_container.find_all('img') if image_container else []
    for img in images:
        cleaned_src = img['src'].strip()
        image_urls.append(cleaned_src)
    
    prev_chapter_tag = soup.find('a', class_='prev_page')
    next_chapter_tag = soup.find('a', class_='next_page')
    
    prev_chapter = prev_chapter_tag['href'].split('/')[-2] if prev_chapter_tag else None
    next_chapter = next_chapter_tag['href'].split('/')[-2] if next_chapter_tag else None
    
    return jsonify({'images': image_urls, 'previous_chapter': prev_chapter, 'next_chapter': next_chapter})
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
