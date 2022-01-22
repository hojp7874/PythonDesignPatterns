import abc
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup


class AbstractFactory(abc.ABC):
    def __init__(self, is_secure):
        self.is_secure = is_secure

    @abc.abstractmethod
    def create_protocol(self):
        pass

    @abc.abstractmethod
    def create_port(self):
        pass

    @abc.abstractmethod
    def create_parser(self):
        pass


class HTTPFactory(AbstractFactory):
    def create_protocol(self):
        return "https" if self.is_secure else "http"

    def create_port(self):
        return HTTPSPort() if self.is_secure else HTTPPort()

    def create_parser(self):
        return HTTPParser()


class FTPFactory(AbstractFactory):
    def create_protocol(self):
        return "ftp"

    def create_port(self):
        return FTPPort()

    def create_parser(self):
        return FTPParser()


class Parser(abc.ABC):
    @abc.abstractmethod
    def __call__(self, content):
        pass


class HTTPParser(Parser):
    def __call__(self, content):
        filenames = []
        soup = BeautifulSoup(content, features="xml")
        links = soup.find_all("a")
        for link in links:
            filenames.append(link.text)
        return "\n".join(filenames)


class FTPParser(Parser):
    def __call__(self, content):
        content = content.decode("utf-8")
        lines = content.split("\n")
        filenames = []
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])

        return "\n".join(filenames)


class Connector:
    def __init__(self, factory: AbstractFactory):
        self.protocol = factory.create_protocol()
        self.port = factory.create_port()
        self.parser = factory.create_parser()

    def read(self, host, path):
        url = f"{self.protocol}://{host}:{str(self.port)}{path}"
        print(f"Connection to {url}")
        return urlopen(url, timeout=2).read()

    def parse(self, content):
        return self.parser(content)


class Port(abc.ABC):
    @abc.abstractmethod
    def __str__(self):
        pass


class HTTPPort(Port):
    def __str__(self):
        return "80"


class HTTPSPort(Port):
    def __str__(self):
        return "443"


class FTPPort(Port):
    def __str__(self):
        return "21"


if __name__ == "__main__":
    domain = "ftp.freebsd.org"
    path = "/pub/FreeBSD/"

    protocol = input("Protocol? (HTTP, FTP): ").upper()
    if protocol == "HTTP":
        is_secure = True if input("Is secure? (Y, N): ").upper() == "Y" else False
        factory = HTTPFactory(is_secure)
    elif protocol == "FTP":
        is_secure = False
        factory = FTPFactory(is_secure)
    else:
        print("Wrong answer.")

    connector = Connector(factory)

    try:
        content = connector.read(domain, path)
    except URLError as e:
        print("Can't access resource with this method")
    else:
        print(connector.parse(content))
