import json
import logging.config
import os
import sys
from pathlib import Path

path = os.path.dirname(os.path.realpath(__file__))
LOG_CONFIG_FILENAME = os.path.join(path, 'log_config.json')
TRACEBACK_LOGGER_ERRORS = True


def get_logger(logger_name):
    try:
        with open(LOG_CONFIG_FILENAME) as log_config_json:
            log_config = json.load(log_config_json)
            configured_loggers = [log_config.get('root', {})] + log_config.get('loggers', [])
            used_handlers = {handler for log in configured_loggers for handler in log.get('handlers', [])}

            for handler_id, handler in list(log_config['handlers'].items()):
                if handler_id not in used_handlers:
                    del log_config['handlers'][handler_id]
                elif 'filename' in handler.keys():
                    filename = handler['filename']
                    logfile_path = Path(filename).expanduser().resolve()
                    handler['filename'] = str(logfile_path)

            logging.config.dictConfig(log_config)
            logger = logging.getLogger(logger_name)
    except Exception:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)

        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)d %(levelname)s in \'%(name)s\'[\'%(module)s\'] at line %(lineno)d: %(message)s',
            '%Y-%m-%d %H:%M:%S')

        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formatter)
        handler.setLevel(logging.WARNING)

        logger.addHandler(handler)

        logger.error(
            'LOGGER ERROR: Can not initialise {} logger, '
            'logging to the stderr. Error traceback:\n'.format(logger_name), exc_info=TRACEBACK_LOGGER_ERRORS)

    return logger
