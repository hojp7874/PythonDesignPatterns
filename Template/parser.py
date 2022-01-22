import abc
from urllib import request
from xml.dom import minidom


class AbstractNewsParser(abc.ABC):
    def print_top_news(self):
        url = self.get_url()
        raw_content = self.get_raw_content(url)
        content = self.parse_content(raw_content)
        cropped = self.crop(content)

        for item in cropped:
            print(f"Title: {item['title']}")
            print(f"Link: {item['link']}")
            print(f"Published: {item['published']}")
            print(f"Id: {item['id']}")
            print()

    @abc.abstractmethod
    def get_url(self):
        pass

    def get_raw_content(self, url):
        return request.urlopen(url).read()

    @abc.abstractmethod
    def parse_content(self, content):
        pass

    def crop(self, parsed_content, max_items=3):
        return parsed_content[:max_items]


class YahooParser(AbstractNewsParser):
    def get_url(self):
        return "https://news.yahoo.com/rss/"

    def parse_content(self, raw_content):
        parsed_content = []

        dom = minidom.parseString(raw_content)

        for node in dom.getElementsByTagName("item"):
            parsed_item = {}

            try:
                parsed_item["title"] = (
                    node.getElementsByTagName("title")[0].childNodes[0].nodeValue
                )
            except IndexError:
                parsed_item["title"] = None

            try:
                parsed_item["link"] = (
                    node.getElementsByTagName("link")[0].childNodes[0].nodeValue
                )
            except IndexError:
                parsed_item["link"] = None

            try:
                parsed_item["id"] = (
                    node.getElementsByTagName("guid")[0].childNodes[0].nodeValue
                )
            except IndexError:
                parsed_item["id"] = None

            try:
                parsed_item["published"] = (
                    node.getElementsByTagName("pubDate")[0].childNodes[0].nodeValue
                )
            except IndexError:
                parsed_item["published"] = None

            parsed_content.append(parsed_item)

        return parsed_content


class GoogleParser(AbstractNewsParser):
    def get_url(self):
        return "https://news.google.com/news/feeds?output=atom"

    def parse_content(self, raw_content):
        parsed_content = []
        dom = minidom.parseString(raw_content)

        for node in dom.getElementsByTagName("entry"):
            parsed_item = {}

            try:
                parsed_item["title"] = (
                    node.getElementsByTagName("title")[0].childNodes[0].nodeValue
                )
            except IndexError:
                parsed_item["title"] = None

            try:
                parsed_item["link"] = (
                    node.getElementsByTagName("link")[0].childNodes[0].nodeValue
                )
            except IndexError:
                parsed_item["link"] = None

            try:
                parsed_item["id"] = (
                    node.getElementsByTagName("id")[0].childNodes[0].nodeValue
                )
            except IndexError:
                parsed_item["id"] = None

            try:
                parsed_item["published"] = (
                    node.getElementsByTagName("updated")[0].childNodes[0].nodeValue
                )
            except IndexError:
                parsed_item["published"] = None

            parsed_content.append(parsed_item)

        return parsed_content


if __name__ == "__main__":
    google = GoogleParser()
    yahoo = YahooParser()

    print("Google:")
    google.print_top_news()
    print()
    print("Yahoo:")
    yahoo.print_top_news()
