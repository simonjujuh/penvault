import logging
from colorama import init, Fore, Style

# Initialiser colorama pour prendre en charge les codes de couleurs ANSI sous Windows
init(autoreset=True)

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Configuration du formateur
        formatter = logging.Formatter('%(message)s')

        # Configuration du gestionnaire de console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(Fore.BLUE + "[*] " + Style.RESET_ALL + message)

    def success(self, message):
        self.logger.info(Fore.GREEN + "[+] " + Style.RESET_ALL + message)

    def error(self, message):
        self.logger.error(Fore.RED + "[-] " + Style.RESET_ALL + message)

    def warning(self, message):
        self.logger.warning(Fore.YELLOW + "[!] " + Style.RESET_ALL + message)


log = Logger("penvault")


if __name__ == "__main__":
    logger = Logger("example_logger")
    logger.info("This is an information message.")
    logger.success("This is a success message.")
    logger.error("This is an error message.")
    logger.warning("This is a warning message.")
