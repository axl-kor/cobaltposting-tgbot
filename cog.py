import json
from datetime import timedelta
from pprint import pp

import shortuuid
from aiogram import BaseMiddleware, F
from aiogram import methods as aiomethods
from aiogram import types as aiotypes
from aiogram.client.session.middlewares.base import BaseRequestMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ErrorEvent, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import formatting
from colorama import Fore as clr
from dateutil.relativedelta import relativedelta

from utils import cobaltAPI, config, parser, types
from utils import shortcuts as sh
from utils.cog import (
    CallbackQuery,
    Cog,
    Message,
    regAdmin,
    regCallback,
    regError,
    regMessage,
    regMyChatMember,
)
from utils.service import Bot
