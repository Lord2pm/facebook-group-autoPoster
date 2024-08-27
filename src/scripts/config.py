from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def load_driver_config():
    service = Service()
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    # options.add_argument("--headless")

    return service, options
