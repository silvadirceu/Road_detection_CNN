import abc


class Component(abc.ABC):
    @abc.abstractclassmethod
    def render(self):
        pass
