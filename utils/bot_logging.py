import logging


def initialize_logging():
    logger = logging.getLogger('disnake')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='./logs/bot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logger.addHandler(handler)
    print("Logging set up.")
