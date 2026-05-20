import functools
import inspect
from typing import Any, Callable, Optional

from aiogram import types

from utils import service


class Message(types.Message):
    """Customized Message class"""

    def __init__(self, bot: service.Bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.as_(bot)

    """Customized Message class"""

    async def safe_edit(
        self: types.Message,
        text: Optional[str] = None,
        photo: types.FSInputFile | None = None,
        reply_markup=None,
        *opts,
    ):
        if self.text:
            return await self.edit_text(text=text, reply_markup=reply_markup, *opts)
        elif self.caption:
            # return await self.edit_caption(
            # 		caption=text,
            # 		reply_markup=reply_markup,
            # 		*opts
            # 	)
            if photo:
                mediaunion = types.InputMediaPhoto(media=photo, caption=text)
            else:
                mediaunion = types.InputMediaPhoto(
                    media=self.photo[0].file_id, caption=text
                )
            return await self.edit_media(
                media=mediaunion, reply_markup=reply_markup, *opts
            )


class CallbackQuery(types.CallbackQuery):
    """Custom Callback Query Class"""

    def __init__(
        self,
        bot: service.Bot,
        id: str,
        from_user: types.User,
        chat_instance: str,
        game_short_name: str | None = None,
        message: types.Message | None = None,
        inline_message_id: str | None = None,
        data: str | None = None,
        **kwargs,
    ):
        super().__init__(
            id=id,
            from_user=from_user,
            chat_instance=chat_instance,
            message=message,
            inline_message_id=inline_message_id,
            data=data,
            game_short_name=game_short_name,
            **kwargs,
        )
        self.as_(bot)
        self.message: Message


def regCallback(filter) -> Callable[..., Any]:
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper._type = "callbackquery"
        wrapper._filter = filter
        return wrapper

    return decorator


def regError(filter=None) -> Callable[..., Any]:
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper._type = "error"
        wrapper._filter = filter
        return wrapper

    return decorator


def regMessage(filter):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper._type = "message"
        wrapper._filter = filter
        return wrapper

    return decorator


def regMyChatMember(filter):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper._type = "myChatMember"
        wrapper._filter = filter
        return wrapper

    return decorator


def regAdmin(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract Cog instance and event
        if not args or len(args) < 2:
            return

        cog_self = args[0]  # self (Cog instance)
        event = args[1]  # callback_query or message

        user = event.from_user if hasattr(event, "from_user") else None
        if not user:
            return

        if user.id in cog_self.bot.config.adminsIds:
            return await func(*args, **kwargs)

        # try:
        #     db_users = await cog_self.bot.dbm.readUsers(tgId=user.id, cacheOverwrite=True)

        #     if db_users and len(db_users) > 0:
        #         db_user = db_users[0]
        #         if (db_user.role == "admin"):
        #             return await func(*args, **kwargs)

        # except Exception as e:
        #     cog_self.bot.log(f"Error checking admin status: {e}", type="error")
        #     return

    return wrapper


class Cog:
    def __init__(self, bot: service.Bot):
        self.bot = bot

    def register(self):
        for name, m in inspect.getmembers(self, predicate=inspect.ismethod):
            val = getattr(m.__func__, "_type", None)
            filter = getattr(m.__func__, "_filter", None)
            if val is not None:
                if val == "callbackquery":
                    self.bot.dispatcher.callback_query.register(m, filter)
                elif val == "message":
                    self.bot.dispatcher.message.register(m, filter)
                elif val == "myChatMember":
                    self.bot.dispatcher.my_chat_member.register(m, filter)
                elif val == "error":
                    self.bot.dispatcher.errors.register(m)

                self.bot.log(f"{m.__name__} registered", type="preload")
