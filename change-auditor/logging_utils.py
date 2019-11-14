import logging
import types

# function to log a blank line
def log_newline(self, how_many_lines=1):
    self.removeHandler(self.console_handler)
    self.addHandler(self.blank_handler)

    for i in range(how_many_lines):
        self.info('')

    self.removeHandler(self.blank_handler)
    self.addHandler(self.console_handler)



def initialize_logger():
    console_handler = logging.FileHandler('results.log')
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)-7s: %(message)s'))

    blank_handler = logging.FileHandler('results.log')
    blank_handler.setLevel(logging.DEBUG)
    blank_handler.setFormatter(logging.Formatter(fmt=''))

    logger = logging.getLogger('logging_test')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    logger.console_handler = console_handler
    logger.blank_handler = blank_handler
    logger.newline = types.MethodType(log_newline, logger)

    return logger



    
