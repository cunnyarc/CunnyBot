"""
 ╔════════════════════════════════════════════════════════════════════════════════════════════════════════[─]═[□]═[×]═╗
 ║ Custom Logging Script                                                                                              ║
 ╠══════════════════════════╦═════════════════════════════════════════════════════════════════════════════════════════╣
 ║ Original By:             ║ https://github.com/V3ntus                                                               ║
 ║ Modified By:             ║ https://github.com/GlitchChan                                                           ║
 ╠══════════════════════════╩═════════════════════════════════════════════════════════════════════════════════════════╣
 ║                                                                                                                    ║
 ║ Custom logging script                                                                                              ║
 ║ Code taken from my contributions in:                                                                               ║
 ║ https://github.com/savioxavier/repo-finder-bot/                                                                    ║
 ║ Additional thanks to savioxavier                                                                                   ║
 ║                                                                                                                    ║
 ║ Modified by Glitchy#6969 for custom coloring.                                                                      ║
 ║                                                                                                                    ║
 ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

import logging

import colorama

from config import DEBUG


def get_logger(name):
    """Function to get a logger
    Useful for modules that have already initialized a logger, such as discord.py
    """
    __logger = logging.getLogger(name)
    __logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    __ch = logging.StreamHandler()
    __ch.setFormatter(CustomFormatter())
    __logger.addHandler(__ch)
    return __logger


def init_logger(name="root"):
    """Function to create a designated logger for separate modules"""
    __logger = logging.Logger(name)
    __ch = logging.StreamHandler()
    __ch.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    __ch.setFormatter(CustomFormatter())
    __logger.addHandler(__ch)
    return __logger


class CustomFormatter(logging.Formatter):
    """Custom formatter class"""
    # grey = "\x1b[38;1m"
    # green = "\x1b[42;1m"
    # yellow = "\x1b[43;1m"
    # red = "\x1b[41;1m"
    # bold_red = "\x1b[31;1m"
    # reset = "\x1b[0m"
    reset = f"{colorama.Back.RESET}{colorama.Fore.RESET}"
    green = colorama.Back.GREEN
    yellow = colorama.Back.YELLOW
    red = colorama.Back.RED
    bold_red = f"{colorama.Style.BRIGHT}{colorama.Fore.RED}"

    # format = "[%(asctime)s][%(levelname)-7s][%(name)-14s][%(lineno)4s] %(message)s"
    FORMATS = {
        logging.DEBUG: f"{reset}[%(asctime)s]{green}[%(levelname)-7s]{reset}[%(name)-14s] [{yellow}%(lineno)4s{reset}] %(message)s",
        logging.INFO: f"{reset}[%(asctime)s][%(levelname)-7s][%(name)-14s] {reset}[{yellow}%(lineno)4s{reset}] %(message)s",
        logging.WARNING: f"{reset}[%(asctime)s]{yellow}[%(levelname)-7s]{reset}[%(name)-14s] [{yellow}%(lineno)4s{reset}] %(message)s",
        logging.ERROR: f"{reset}[%(asctime)s]{red}[%(levelname)-7s]{reset}[%(name)-14s] [{yellow}%(lineno)4s{reset}] %(message)s",
        logging.CRITICAL: f"{reset}[%(asctime)s]{bold_red}[%(levelname)-7s]{reset}[%(name)-14s] [{yellow}%(lineno)4s{reset}] %(message)s"
    } if DEBUG else {
        logging.DEBUG: f"{reset}[%(asctime)s]{green}[%(levelname)-7s]{reset}[%(name)-14s] [{yellow}%(lineno)4s{reset}] %(message)s",
        logging.INFO: f"{reset}[%(asctime)s][%(levelname)7s] %(message)s",
        logging.WARNING: f"{yellow}[%(asctime)s][%(levelname)7s] %(message)s{reset}",
        logging.ERROR: f"{red}[%(asctime)s][%(levelname)7s] %(message)s{reset}",
        logging.CRITICAL: f"{reset}{bold_red}[%(asctime)s][%(levelname)7s] %(message)s{reset}"
    }
    # Documenting my dwindling sanity here

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%I:%M.%S%p")
        return formatter.format(record)
