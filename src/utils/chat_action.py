from __future__ import annotations

import asyncio
import logging
import time
from asyncio import Event, Lock
from contextlib import suppress
from typing import TYPE_CHECKING, Any, Optional, Union

from hydrogram.enums import ChatAction
from loguru import logger

if TYPE_CHECKING:
    from hydrogram import Client

DEFAULT_INTERVAL = 5.0
DEFAULT_INITIAL_SLEEP = 0.0

class ChatActionSender:
    """Sends chat actions periodically."""

    __slots__ = (
        "client",
        "chat_id",
        "action",
        "interval",
        "initial_sleep",
        "_lock",
        "_close_event",
        "_closed_event",
        "_task",
    )

    def __init__(
        self,
        client: Client,
        chat_id: Union[str, int],
        action: ChatAction,
        initial_sleep: Union[float, int] = DEFAULT_INITIAL_SLEEP,
        interval: Union[float, int] = DEFAULT_INTERVAL
    ) -> None:
        self.client = client
        self.chat_id = chat_id
        self.action = action
        self.initial_sleep = initial_sleep
        self.interval = interval

        self._lock = Lock()
        self._close_event = Event()
        self._closed_event = Event()
        self._task: Optional[asyncio.Task[None]] = None

    @property
    def running(self) -> bool:
        return self._task is not None

    async def _wait(self, interval: Union[float, int]) -> None:
        if interval > 0:
            with suppress(asyncio.TimeoutError):
                await asyncio.wait_for(self._close_event.wait(), timeout=interval)

    async def _worker(self) -> None:
        if not self.client.is_connected():
            raise RuntimeError("Bot is not started")

        chat_id = self.chat_id
        action = self.action

        logger.debug(f'Started chat action {action} sender in chat_id={chat_id}')

        try:
            counter = 0
            await self._wait(self.initial_sleep)

            while not self._close_event.is_set():
                start_time = time.monotonic()

                logger.debug(f'Sending chat action {action} to chat_id={chat_id} (sent {counter} actions)')

                try:
                    await self.client.send_chat_action(chat_id=chat_id, action=action)
                except Exception as e:
                    logger.exception('Failed to send chat action: ')
                    await asyncio.sleep(1)
                    continue

                counter += 1

                elapsed_time = time.monotonic() - start_time
                await self._wait(max(0, self.interval - elapsed_time))

        except Exception:
            logger.exception('Exception in chat action worker:')
        finally:
            logger.debug(f'Finished chat action {action} sender in chat_id={chat_id}')
            self._closed_event.set()

    async def start(self) -> None:
        async with self._lock:
            if self.running:
                raise RuntimeError("Already running")

            self._close_event.clear()
            self._closed_event.clear()
            self._task = asyncio.create_task(self._worker())

    async def stop(self) -> None:
        async with self._lock:
            if not self.running:
                return

            self._close_event.set()
            await self._closed_event.wait()
            self._task = None

    async def __aenter__(self) -> "ChatActionSender":
        await self.start()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.stop()

    @classmethod
    def _create(
        cls,
        client: Client,
        chat_id: Union[int, str],
        action: ChatAction,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls(client, chat_id, action, interval, initial_sleep)

    @classmethod
    def typing(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.TYPING, interval, initial_sleep)

    @classmethod
    def upload_photo(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.UPLOAD_PHOTO, interval, initial_sleep)

    @classmethod
    def record_video(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.RECORD_VIDEO, interval, initial_sleep)

    @classmethod
    def upload_video(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.UPLOAD_VIDEO, interval, initial_sleep)

    @classmethod
    def record_audio(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.RECORD_AUDIO, interval, initial_sleep)

    @classmethod
    def upload_audio(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.UPLOAD_AUDIO, interval, initial_sleep)

    @classmethod
    def upload_document(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.UPLOAD_DOCUMENT, interval, initial_sleep)

    @classmethod
    def choose_sticker(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.CHOOSE_STICKER, interval, initial_sleep)

    @classmethod
    def find_location(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.FIND_LOCATION, interval, initial_sleep)

    @classmethod
    def record_video_note(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.RECORD_VIDEO_NOTE, interval, initial_sleep)

    @classmethod
    def upload_video_note(
        cls,
        client: Client,
        chat_id: Union[int, str],
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP
    ) -> "ChatActionSender":
        return cls._create(client, chat_id, ChatAction.UPLOAD_VIDEO_NOTE, interval, initial_sleep)
