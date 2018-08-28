from abc import ABC, abstractmethod


class BaseIntegration(ABC):

    @abstractmethod
    def pull_from_journals(self, query):
        pass

    @abstractmethod
    def push_to_journals(self, data):
        pass

    @abstractmethod
    def pull_from_service(self, query):
        pass

    @abstractmethod
    def push_to_service(self, data):
        pass
