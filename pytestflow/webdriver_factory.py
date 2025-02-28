
import platform
from typing import Any

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService

from selenium.webdriver.common.options import ArgOptions as Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from pytestflow.pytest_flow_exceptions import PyTestFlowException
from pytestflow.test_config_data_loader import Config


class WebDriverFactory:
    """
    A base class to create and manage WebDriver instances. It provides functionality to initialize WebDriver objects for
    both local and remote execution using Selenium.
    """
    __SUPPORTED_BROWSERS = ['chrome', 'edge', 'firefox', 'safari']

    def __init__(self, browser: str | None = None, remote: bool = False, grid_url: str = None, test_config_path: str = None):
        """
        Args:
            browser: The browser to be used for the test, e.g., 'chrome', 'firefox'. If none is provided, defaults to None.
            remote: Flag indicating whether the tests should run in a remote environment. Default is False.
            grid_url: The URL of the Selenium Grid to be used for remote testing. Default is None.
            test_config_path: Path to the configuration file containing test settings.
        """
        self.__browser: str = browser
        self.__remote: bool = remote
        self.__grid_url: str = grid_url
        self.__driver: WebDriver | None = None
        self.__service = None
        self.__config_data: dict[str, Any] = {}
        if test_config_path:
            self.__config_data: dict[str, Any] = Config(test_config_path=test_config_path).get_config_data(browser=self.__browser)
        self.__check_platform_compatibility()
        self.__check_browser_availability()
        self.__set_webdriver()

    def __check_platform_compatibility(self) -> None:
        """
        Checks if the current platform and browser combination is compatible.

        Raises an exception if the browser is not supported on the current platform.

        :return: None
        :raises PyTestFlowException: If the browser is not supported on the current platform.
        """
        if platform.system() == 'Windows' and self.__browser == 'safari':
            raise PyTestFlowException(f"{self.__browser} is not supported on Windows.")

    def __check_browser_availability(self) -> None:
        """
        Checks if the browser specified is available in the list of supported browsers.

        :raises PyTestFlowException: If the specified browser is not in the supported browsers list"""
        if self.__browser not in self.__SUPPORTED_BROWSERS:
            raise PyTestFlowException(f"Unsupported Browser: {self.__browser}. "
                                    f"Supported browsers are {','.join(self.__SUPPORTED_BROWSERS)}")

    def __set_webdriver(self) -> None:
        """
        Create webdriver instance
        :return: None
        """
        self.__driver = self.__create_remote_driver() if self.__remote and self.__grid_url else (
            self.__create_local_driver())

    def __init_service(self):
        """
        Initializes the browser-specific service for WebDriver.

        Depending on the browser name stored in ``self.__browser``, this method sets up
        and starts the respective WebDriver service. It supports Chrome, Firefox, Edge, and Safari browsers.
        The WebDriver managers are used to automatically handle driver download and setup.

        Raises:
            PyTestFlowException: If an error is encountered while initializing the service for the specified browser.

        """
        try:
            if self.__browser == 'chrome':
                self.__service = ChromeService(ChromeDriverManager().install())
            elif self.__browser == 'firefox':
                self.__service = FirefoxService(GeckoDriverManager().install())
            elif self.__browser == 'edge':
                self.__service = EdgeService(EdgeChromiumDriverManager().install())
            elif self.__browser == 'safari':
                self.__service = SafariService()
        except Exception as e:
            raise PyTestFlowException(f"An Error encountered while initializing service for {self.__browser} browser."
                                    f"Original Exception is: {e}") from e


    def __get_options(self) -> Options | None:
        """
        Retrieves browser-specific options and configurations.

        This method constructs and configures options for the selected browser
        based on the internal configuration data. It supports Chrome, Firefox, Edge,
        and Safari web browsers. The options object is customized by:
          - Adding arguments from the "args" configuration.
          - Setting additional capabilities from other configuration key-value pairs.

        Returns:
            Options | None: The initialized options object for the selected browser
            or None if the browser type is not recognized.
        """
        args = self.__config_data.get("args", [])
        options: Options | None = None
        if self.__browser == 'chrome':
            options = ChromeOptions()
        elif self.__browser == 'firefox':
            options = FireFoxOptions()
        elif self.__browser == 'edge':
            options = EdgeOptions()
        elif self.__browser == 'safari':
            options = SafariOptions()

        for arg in args:
            options.add_argument(arg)

        for key, value in self.__config_data.items():
            options.set_capability(key, value)

        return options



    def __create_remote_driver(self) -> WebDriver | None:
        """
        Creates a remote WebDriver instance using Selenium WebDriver.

        This method initializes a Selenium Remote WebDriver by specifying
        a remote grid URL and browser options. It handles potential errors
        during the driver creation process and raises custom exceptions
        with detailed error messages.

        Returns:
            WebDriver | None: Returns the initialized remote WebDriver instance,
            or None if initialization fails.

        Raises:
            PyTestFlowException: Raised when there is an issue creating the remote
            WebDriver, with details about the encountered exception.
        """
        options = self.__get_options()
        self.__init_service()
        try:
            self.__driver = webdriver.Remote(
                command_executor=self.__grid_url,
                options=options
            )

        except WebDriverException as e:
            raise PyTestFlowException(f"WebDriverException Encountered while creating remote webdriver for "
                                    f"{self.__browser} Original Error: {e}") from e
        except Exception as e:
            raise PyTestFlowException(
                f"An Exception is encountered while creating remote webdriver for {self.__browser}"
                f"Original Error: {e}") from e

        return self.__driver

    def __create_local_driver(self):
        """
        Creates and initializes a local web driver instance based on the specified browser type.

        Supported browsers:
        - chrome
        - edge
        - firefox
        - safari

        For each supported browser, the respective driver is installed and used to instantiate the corresponding
        WebDriver. If an unsupported browser type is specified, a PyTestFlowException will be raised.

        :return: An instance of the web driver for the specified browser type
        :rtype: selenium.webdriver
        :raises PyTestFlowException: If the specified browser is not supported
        """
        options = self.__get_options()
        self.__init_service()

        if self.__browser == 'chrome':
            self.__driver = webdriver.Chrome(options=options, service=self.__service)
        elif self.__browser == 'edge':
            self.__driver =  webdriver.Edge(options=options, service=self.__service)
        elif self.__browser == 'firefox':
            self.__driver =  webdriver.Firefox(options=options, service=self.__service)
        elif self.__browser == 'safari':
            self.__driver =  webdriver.Safari(options=options, service=self.__service)

        return self.__driver

    def get_webdriver(self) -> WebDriver | None:
        """
        Returns the current WebDriver instance if it exists.

        This method retrieves the active WebDriver instance that is being
        managed internally. If no WebDriver instance exists, it returns None.

        Returns:
            WebDriver | None: The active WebDriver instance or None if no driver is set.
        """
        return self.__driver

    def quit_webdriver(self) -> None:
        """
        Closes the WebDriver instance.

        This method attempts to close the WebDriver instance initiated by the automation framework.
        If an exception occurs during the process, it captures the error and raises a `PyTestFlowException`
        with the original exception message.

        Raises:
            PyTestFlowException: If an exception occurs while quitting the WebDriver.
        """
        try:
            self.__driver.quit()
        except Exception as e:
            raise PyTestFlowException(f"Error in closing WebDriver. Original Error: {e}") from e

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Args:
            exc_type: The exception type of the error raised during the execution of the code block.
            exc_val: The exception value, which typically includes details of the error.
            exc_tb: The traceback object providing information about where in the code the exception occurred.

        """
        if self.__driver:
            self.quit_webdriver()
