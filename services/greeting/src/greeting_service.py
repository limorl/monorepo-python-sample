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

    def bye(self, name: str, numOfExclamations: int = 1) -> str:
        return f"Bye {name}{'!' * numOfExclamations}"

    def dumpsterFire(self, name: str, numOfHastages: int = 7) -> str:
        return f"{name} is in a dampster fire{'#' * numOfHastages}"
