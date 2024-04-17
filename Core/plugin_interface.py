
from abc import ABC, abstractmethod
from typing import Any, Dict

class PluginInterface(ABC):
    """
    A base class for defining the interface that all plugins must implement
    to be compatible with the system. This interface now includes methods for
    initializing the plugin, executing its main functionality, and cleaning up
    resources, along with asynchronous execution support.
    """

    version = "1.0.0"  # Default version, can be overridden by subclasses

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with necessary configuration. This method is
        called once before the plugin is executed for the first time.

        :param config: A configuration object or dictionary with necessary
                       settings for the plugin.
        """
        pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> None:
        """
        Execute the plugin's main functionality. This method is called
        whenever the plugin's action is required.

        :param args: Positional arguments that the plugin might need.
        :param kwargs: Keyword arguments that the plugin might need.
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """
        Perform any necessary cleanup operations. This method is called
        when the plugin is being unloaded or the application is shutting down,
        allowing the plugin to release resources or save state as needed.
        """
        pass

    async def execute_async(self, *args: Any, **kwargs: Any) -> None:
        """
        Optionally implement this method in plugins for asynchronous execution.
        """
        pass
