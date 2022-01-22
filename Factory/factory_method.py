import abc
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup


class Connector(abc.ABC):
    def __init__(self, is_secure):
        self.is_secure = is_secure
        self.port = self.port_factory_method()
        self.protocol = self.protocol_factory_method()

    @abc.abstractmethod
    def protocol_factory_method(self):
        pass

    @abc.abstractmethod
    def port_factory_method(self):
        pass

    @abc.abstractmethod
    def parse(self):
        pass

    def read(self, host, path):
        url = f"{self.protocol}://{host}:{str(self.port)}{path}"
        print(f"Connection to {url}")
        return urlopen(url, timeout=2).read()


class HTTPConnector(Connector):
    def protocol_factory_method(self):
        return "https" if self.is_secure else "http"

    def port_factory_method(self):
        return HTTPSPort() if self.is_secure else HTTPPort()

    def parse(self, content):
        filenames = []
        soup = BeautifulSoup(content, features="xml")
        links = soup.find_all("a")
        for link in links:
            filenames.append(link.text)
        return "\n".join(filenames)


class FTPConnector(Connector):
    def protocol_factory_method(self):
        return "ftp"

    def port_factory_method(self):
        return FTPPort()

    def parse(self, content):
        content = content.decode("utf-8")
        lines = content.split("\n")
        filenames = []
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])

        return "\n".join(filenames)


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
        connector = HTTPConnector(is_secure)
    else:
        is_secure = False
        connector = FTPConnector(is_secure)

    try:
        content = connector.read(domain, path)
    except URLError as e:
        print("Can't access resource with this method")
    else:
        print(connector.parse(content))
