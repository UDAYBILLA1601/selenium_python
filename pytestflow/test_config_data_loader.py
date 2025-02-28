import json
from typing import Any


from pytestflow.pytest_flow_exceptions import PyTestFlowException

class Config:
    """
    Class TestConfig provides functionality to load and retrieve test configuration data from a JSON file.

    Methods:
        - __init__(test_config_path: str | None): Initializes a TestConfig instance with a given test configuration file path or defaults to "test_environment.json".
        - __load_test_config_data(): Loads the configuration data from the specified JSON file.
        - get_config_data(browser: str | None, device: str | None): Retrieves configuration data for a specified browser or device.

    """
    def __init__(self, test_config_path: str | None = None):
        """
        :param test_config_path: Path to the test configuration file. If None, the default configuration will be loaded.
        """
        self.__test_config_path: str = test_config_path if test_config_path else r"test_environment.json"
        self.__config_data: dict[str, Any] = {}
        self.__load_test_config_data()

    def __load_test_config_data(self):
        """
        :param config_file_path: The file path to the configuration file, defaulting to "test_environment.json".
        :return: None
        :raises PyTestFlowException: Raised when the configuration file is not found or cannot be opened for any other reason.
        """

        try:
            with open(self.__test_config_path, "r", encoding=None) as config_file:
                self.__config_data = json.load(config_file)
        except FileNotFoundError as e:
            raise PyTestFlowException(f"Test config data file path not found. Please verify the correct path location."
                                    f"Path provided is: {self.__test_config_path}") from e
        except Exception as e:
            raise PyTestFlowException(f"Error in opening test config data file. Original Error: {e}") from e

    def get_config_data(self,browser: str | None = None, device: str | None = None) -> dict[str, Any]:
        """
        :param test_config_path: The path to the test configuration file. This parameter is optional and can be None.
        :param browser: The name of the browser for which configuration data needs to be retrieved. This parameter is optional and can be None.
        :param device: The name of the device for which configuration data needs to be retrieved. This parameter is optional and can be None.
        :return: A dictionary containing configuration data for the specified browser or device. Returns None if neither browser nor device is provided or if data for the specified parameter is not available.
        """

        if browser:
            return self.__config_data.get("browsers").get(browser, {})
        if device:
            return self.__config_data.get("devices").get(device, {})





