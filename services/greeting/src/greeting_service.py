from abc import ABC, abstractmethod


class IGreetingService(ABC):
    @abstractmethod
    def hello(self, name: str, numOfExclamations: int = 1) -> str:
        """Generates a greeting message.

        Args:
            name: The name to include in the greeting.
            numOfExclamations: The number of exclamation points to include.

        Returns:
            A greeting string.
        """
        pass


class GreetingService(IGreetingService):
    def hello(self, name: str, numOfExclamations: int = 1) -> str:
        return f"Hello {name}{'!' * numOfExclamations}"
