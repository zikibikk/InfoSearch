import os
import requests
from requests.exceptions import RequestException


def download_html_pages(url_list, output_dir):
    html_contents = {}
    for i, url in enumerate(url_list):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_contents[url] = response.text
                filename = os.path.join(output_dir, f"{str(i+1)}.html")
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(response.text)
            else:
                print(f"Ошибка загрузки {url}: Статус код {response.status_code}")
        except RequestException as e:
            print(f"Ошибка загрузки {url}: {e}")
    return html_contents


def download_and_save_files(filepath, output_dir):
    urls = get_links_from_file(filepath)
    html_pages = download_html_pages(urls, output_dir)
    with open("index.txt", "w", encoding="utf-8") as file:
        for i, url in enumerate(html_pages.keys(), start=1):
            file.write(f"{i} - {url}\n")
            # Можно добавить запись содержимого страницы в файл, если это необходимо
    print(f"Скачивание завершено. Записано {len(html_pages)} постов в index.txt.")


def get_links_from_file(filename):
    links = []
    with open(filename, 'r') as file:
        for line in file:
            links.append(line.strip())

    return links


output_directory = "files_new"
os.makedirs(output_directory, exist_ok=True)
download_and_save_files('crawled_links.txt', output_directory)
