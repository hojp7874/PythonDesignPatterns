import abc
from datetime import datetime
import time


class Subject:
    def __init__(self):
        self.observers = []
        self.cur_time = None

    def register_observer(self, observer):
        if observer in self.observers:
            print(f"{observer} already in subscribed observers")
        else:
            self.observers.append(observer)

    def unregister_observer(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print("No such observer in subject")

    def notify_observers(self):
        self.cur_time = time.time()
        for observer in self.observers:
            observer.notify(self)


class Observer(abc.ABC):
    @abc.abstractmethod
    def notify(self, unix_timestamp):
        pass


class USATimeObserver(Observer):
    def __init__(self, name):
        self.name = name

    def notify(self, subject):
        time = datetime.fromtimestamp(int(subject.cur_time)).strftime(
            "%Y-%m-%d %I:%M:%S%p"
        )
        print(f"Observer {self.name} says: {time}")


class EUTimeObserver(Observer):
    def __init__(self, name):
        self.name = name

    def notify(self, subject):
        time = datetime.fromtimestamp(int(subject.cur_time)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        print(f"Observer {self.name} says: {time}")


if __name__ == "__main__":
    subject = Subject()

    print("Adding usa_time_observer")
    observer1 = USATimeObserver("usa_time_observer")
    subject.register_observer(observer1)
    subject.notify_observers()

    time.sleep(2)
    print("Adding eu_time_observer")
    observer2 = USATimeObserver("eu_time_observer")
    subject.register_observer(observer2)
    subject.notify_observers()

    time.sleep(2)
    print("Removing usa_time_observer")
    subject.unregister_observer(observer1)
    subject.notify_observers()
