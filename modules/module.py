from abc import ABC, abstractmethod
import json
from queue import Queue


class Module(ABC):
    unmanaged_fields: list = ["gstate", "state", "queue"]

    id: str
    gstate: any
    queue: Queue

    def __init__(self, from_data):
        self.gstate = None
        for k, v in from_data.items():
            if k not in self.unmanaged_fields:
                setattr(self, k, v)

    def set_state(self, gstate):
        self.gstate = gstate

    def set_queue(self, queue):
        self.queue = queue

    def printb(self, message="", end="\n", flush=False):
        print(self)
        self.queue.put(message + end, block=False)

    @abstractmethod
    def on_activate(self):
        pass

    @abstractmethod
    def on_input(self, line):
        pass

    @abstractmethod
    def extra_json(self, d):
        pass

    def toJSON(self):
        d = {
            "id": self.id,
            "class": self.__class__.__name__,
        }
        for k, v in vars(self).items():
            if k not in self.unmanaged_fields:
                d[k] = v

        d = self.extra_json(d)

        return json.dumps(d, indent=4)
