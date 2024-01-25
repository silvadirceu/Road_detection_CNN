import abc


class Component(abc.ABC):
    @abc.abstractmethod
    def render(self):
        pass
