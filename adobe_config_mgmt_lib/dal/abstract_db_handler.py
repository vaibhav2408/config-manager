from abc import ABC, abstractmethod


class AbstractDBHandler(ABC):
    """
    Abstract model for all DAL(Data access layer) to extend
    """

    @abstractmethod
    def add_configs(self, data: dict, execution_context: dict):
        """
        Method to create an entry in the database
        Args:
            data: the filtering/query data
            execution_context: any additional data/info required for performing the operation
        """

    @abstractmethod
    def get_configs(self, data: dict, execution_context: dict):
        """
        Method to read an entry from the database
        Args:
            data: the filtering/query data
            execution_context: any additional data/info required for performing the operation
        """

    @abstractmethod
    def update_configs(self, data: dict, execution_context: dict):
        """
        Method to update an entry in the database
        Args:
            data: the filtering/query data
            execution_context: any additional data/info required for performing the operation
        """

    @abstractmethod
    def delete_configs(self, data: dict, execution_context: dict):
        """
        Method to delete an entry from the database
        Args:
            data: the filtering/query data
            execution_context: any additional data/info required for performing the operation
        """
