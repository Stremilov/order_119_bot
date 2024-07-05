from aiogram.fsm.state import State, StatesGroup


class ScheduleForm(StatesGroup):
    askForDate = State()
    showSchedule = State()


class BookForm(StatesGroup):
    askForDate = State()
    askForStartTime = State()
    askForEndTime = State()
    askForReason = State()
    PendingApproval = State()


class UnBookForm(StatesGroup):
    askForDescription = State()
    sendTicket = State()
