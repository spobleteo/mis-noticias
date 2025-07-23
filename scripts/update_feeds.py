import feedparser
import json
import time

# Lee la lista de feeds desde el archivo feeds.txt
with open("scripts/feeds.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

def fetch_all_feeds():
    all_articles = []
    for url in urls:
        try:
            print(f"Fetching {url}...")
            parsed_feed = feedparser.parse(url)
            source_name = parsed_feed.feed.get("title", "Fuente desconocida")
            
            for entry in parsed_feed.entries:
                # Normalizamos los datos en una estructura limpia
                pub_date_parsed = feedparser._parse_date_strict(entry.get("published", entry.get("updated", "")))
                pub_date_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', pub_date_parsed)

                all_articles.append({
                    "sourceName": source_name,
                    "title": entry.get("title", "Sin título"),
                    "link": entry.get("link", ""),
                    "pubDate": pub_date_iso,
                    "description": entry.get("summary", ""),
                    "image": next((link['href'] for link in entry.get("links", []) if link.get('rel') == 'enclosure' and 'image' in link.get('type', '')), None)
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # Ordenar todos los artículos por fecha, de más nuevo a más antiguo
    all_articles.sort(key=lambda x: x['pubDate'], reverse=True)
    return all_articles

if __name__ == "__main__":
    articles = fetch_all_feeds()
    # Guardar los datos en el archivo que usará el HTML
    with open("datos.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved {len(articles)} articles to datos.json")
