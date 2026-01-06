import logging

def setup_logger():
    logger = logging.getLogger("BinanceBot")
    logger.setLevel(logging.INFO)
    
    # File handler appends to 'bot.log' in the root directory
    fh = logging.FileHandler("bot.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(fh)
    return logger

logger = setup_logger()
