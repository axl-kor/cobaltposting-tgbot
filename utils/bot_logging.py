import logging, os
from datetime import datetime
from colorama import Fore
from utils import shortcuts, config
from time import mktime

_dirname = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
logs_path = f'logs/{_dirname}/'
os.makedirs(logs_path, exist_ok=True)

main_logger = logging.Logger("main")

handler = logging.FileHandler(filename=logs_path + 'lib.log', encoding='utf-8', mode='w')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    handlers=[
        logging.FileHandler(logs_path + "bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


class DateFormatter(logging.Formatter):
  def __init__(self,datefmt, fmt, *args, **kwargs):
    super(DateFormatter, self).__init__(datefmt=datefmt, fmt=fmt)

  def formatTime(self, record, datefmt=None):
    ct = self.converter(record.created)
    dt = shortcuts.datetime_from_timestamp(mktime(ct) + record.msecs / 1000.)
    return dt

handler.setFormatter(
  DateFormatter(datefmt="%d.%b %H:%M:%S", timezone=config.defaultTimezone, fmt='%(asctime)s | %(levelname)s | %(name)s - %(message)s')
)

main_logger.addHandler(handler)

class Logging:
  def __init__(self):
    self.log = self.info
    self.logs_path = logs_path

  def info(self, *args, type: str):
    """%Y-%m-%d %H:%M:%S | INFO | {type} | {kwargs} | {kwargs} | {kwargs}..."""
    args = [str(i) for i in list(args)]

    main_logger.info(f'{type} | {" | ".join(args)}')

    argTypes = {
        "debug": f"{Fore.YELLOW}- DBG{Fore.RESET}",
        "internal": f"{Fore.CYAN}- INT{Fore.RESET}",
        "autorenewal": f"{Fore.LIGHTGREEN_EX}- REN REM{Fore.RESET}",
        "recv": f"{Fore.LIGHTMAGENTA_EX}< RECV{Fore.RESET}",
        "resp": f"{Fore.LIGHTMAGENTA_EX}> RESP{Fore.RESET}",
        "preload": f"- LOAD",
        "modules": f"{Fore.LIGHTBLUE_EX}- MODULES{Fore.RESET}",
        "warn": f"{Fore.RED}~ WR{Fore.RESET}",
        "ok": f"{Fore.CYAN}V OK{Fore.RESET}",
        "error": f"{Fore.LIGHTRED_EX}X ER{Fore.RESET}",
        "db": f"{Fore.LIGHTBLUE_EX}- DB{Fore.RESET}",
        "pos": f"{Fore.LIGHTWHITE_EX}- POS{Fore.RESET}",
        "global": f"{Fore.MAGENTA}- GLOBAL{Fore.RESET}",
    }

    if type in config.logIgnoreTypes:
        return
    try:
        args.insert(0, argTypes[type.lower()])
    except:
        pass

    time = shortcuts.nowdt().strftime("%H:%M:%S.%f")[:-3]
    datetimeformat = shortcuts.nowdt().strftime(f"%d/%m/%Y {time} %Z")
    print(f"[{datetimeformat}] {' | '.join(args)}")
