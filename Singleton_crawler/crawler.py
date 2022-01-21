import os
import threading
from urllib import request
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
import httplib2


class Singleton:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance


class ImageDownLoaderThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print(f"Starting thread {self.name}")
        download_images(self.name)
        print(f"Finished thread {self.name}")


def traverse_site(max_links=10):
    link_parser_singleton = Singleton()

    while link_parser_singleton.queue_to_parse:
        if len(link_parser_singleton.to_visit) == max_links:
            return

        url = link_parser_singleton.queue_to_parse.pop()
        http = httplib2.Http()
        try:
            status, response = http.request(url)
        except Exception:
            continue
        if "text/html" not in status.get("content-type"):
            continue
        link_parser_singleton.to_visit.add(url)
        print(f"Added {url} to queue")

        bs = BeautifulSoup(response)
        for link in BeautifulSoup.find_all(bs, "a"):
            link_url = link.get("href")
            if not link_url:
                continue

            parsed = urlparse(link_url)
            if parsed.netloc and parsed.netloc != parsed_root.netloc:
                continue

            link_url = (parsed.scheme or parsed_root.scheme) + "://" + (
                parsed.netloc or parsed_root.netloc
            ) + parsed.path or ""

            if link_url in link_parser_singleton.to_visit:
                continue

            link_parser_singleton.queue_to_parse = [
                link_url
            ] + link_parser_singleton.queue_to_parse


def download_images(thread_name):
    singleton = Singleton()
    while singleton.to_visit:
        url = singleton.to_visit.pop()

        http = httplib2.Http()
        print(f"{thread_name} Starting downloading images from {url}")

        try:
            status, response = http.request(url)
        except Exception:
            continue

        bs = BeautifulSoup(response)

        images = BeautifulSoup.find_all(bs, "img")

        for image in images:
            src = image.get("src")
            src = urljoin(url, src)

            basename = os.path.basename(src)
            if src not in singleton.downloaded:
                singleton.downloaded.add(src)
                print(f"Downloading {src}")
                request.urlretrieve(src, os.path.join("images", basename))

        print(f"{thread_name} finished downloading images from {url}")


if __name__ == "__main__":
    root = "https://python.org"
    parsed_root = urlparse(root)

    singleton = Singleton()
    singleton.queue_to_parse = [root]
    singleton.to_visit = set()
    singleton.downloaded = set()

    traverse_site()

    if not os.path.exists("images"):
        os.makedirs("images")

    thread1 = ImageDownLoaderThread(1, "Thread-1", 1)
    thread2 = ImageDownLoaderThread(2, "Thread-2", 2)

    thread1.start()
    thread2.start()
