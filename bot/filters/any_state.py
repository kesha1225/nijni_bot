from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class AnyStateClearMessageFilter(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        if await state.get_state() is not None:
            await state.clear()

        return True


class StateMessageFilter(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return await state.get_state() is not None
