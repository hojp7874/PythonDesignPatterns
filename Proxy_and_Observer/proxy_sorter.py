import abc
from random import random


class AbstractSubject(abc.ABC):
    @abc.abstractmethod
    def sort(self, reverse=False):
        pass


class ReadSubject(AbstractSubject):
    def __init__(self):
        self.digits = []
        for _ in range(10000000):
            self.digits.append(random())

    def sort(self, reverse: bool = False):
        self.digits.sort()
        if reverse:
            self.digits.reverse()


class Proxy(AbstractSubject):
    reference_count = 0

    def __init__(self):
        if not getattr(Proxy, "cached_object", None):
            Proxy.cached_object = ReadSubject()
            print("Created new object")
        else:
            print("Using cached object")
        Proxy.reference_count += 1
        print(f"Count of references = {Proxy.reference_count}")

    @classmethod
    def sort(Proxy, reverse=False):
        print("Called sort method with args:")
        print(locals().items())
        Proxy.cached_object.sort(reverse=reverse)

    def __del__(self):
        Proxy.reference_count -= 1

        if Proxy.reference_count == 0:
            print("Number of reference_count ids 0, Deleting cached object...")
            del Proxy.cached_object
        print(f"Deleted object. Count of objects = {Proxy.reference_count}")


if __name__ == "__main__":
    proxy1 = Proxy()
    proxy2 = Proxy()
    proxy3 = Proxy()
    print()

    proxy1.sort(reverse=True)
    print()

    del proxy2
    print()

    print("The other objects are deleted upon program termination")
