import logging

def get_logger(name="BinanceBot"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # File handler appends to 'bot.log' in the root directory
    fh = logging.FileHandler("bot.log")
    # ISO-8601 format for timestamps is a professional best practice
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(fh)
    return logger
