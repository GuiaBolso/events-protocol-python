import logging
import typing


def supress_log(f):
    def wrapper(*args, **kwargs):
        disable_logs()
        return f(*args, **kwargs)

    return wrapper


def disable_logs(log_names: typing.List[str] = []) -> None:
    filtered_logs = []
    log_keys = logging.Logger.manager.loggerDict.keys()
    if len(log_names) == 0:
        filtered_logs = log_keys
    else:
        for log in log_names:
            for key in log_keys:
                if key.startswith(log):
                    filtered_logs.append(key)
    for filter_key in filtered_logs:
        log = logging.getLogger(filter_key)
        log.disabled = True
        log.addHandler(logging.NullHandler())
        log.propagate = False
        log.addFilter(lambda record: False)
