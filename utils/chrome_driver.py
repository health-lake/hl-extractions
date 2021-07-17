from selenium import webdriver


class ChromeDriver:
    """
        Class ConfigurarGoogle: Configura as opções para iniciar o Google Chrome
        
        -> PARAMS:
            
        -> METHODS:
            - get_driver: cria o objeto driver que será utilizado para iniciar o chrome
    """
    def get_driver(self):
        options = webdriver.ChromeOptions()

        options.add_argument("--dns-prefetch-disable")
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1420,1080')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--enable-automation')
        options.add_argument('ignore-certificate-errors')
        options.page_load_strategy = 'normal'

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(300) 

        return driver
