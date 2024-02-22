import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        absolute_links = [urljoin(response.url, link['href']) for link in links]
        return absolute_links
    else:
        return []


def crawl_site(start_url, max_links=100):
    visited_urls = set()
    links_to_visit = [start_url]
    crawled_links = []

    while links_to_visit:
        current_url = links_to_visit.pop(0)
        if current_url not in visited_urls:
            visited_urls.add(current_url)
            print(f"Crawling {current_url}")

            links_on_page = get_links(current_url)
            for link in links_on_page:
                if len(crawled_links) >= max_links:
                    return crawled_links
                if link not in visited_urls and '#' not in link\
                        and '.png' not in link and '.jpg' not in link and '.svg' not in link:
                    links_to_visit.append(link)
                    crawled_links.append(link)

    return crawled_links


def save_links_to_file(links, filename):
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')


start_url = 'https://ru.wikipedia.org/wiki/Древнегреческая_мифология'
crawled_links = crawl_site(start_url, max_links=200)

output_file = 'crawled_links.txt'
save_links_to_file(crawled_links, output_file)

