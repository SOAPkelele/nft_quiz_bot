import calendar
from datetime import datetime
from typing import Dict, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

emoji = {
    'right': '➡️',
    'left': '⬅️',
    'pencil': '✏️',
    'cross': '❌',
    'back_arrow': '↩️',
    'black_cross': '✖️',
    'envelope': '✉️',
    'megaphone': '📢',
    'arm': '💪🏼'
}

months = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}

view_workout_callback = CallbackData("view_workout", "offset", "workout_id")
page_callback = CallbackData("change_page", "offset")
workout_change_callback = CallbackData("workout", "action", "workout_id")
delete_workout_callback = CallbackData("delete_workout", "if_delete", "workout_id")
quit = InlineKeyboardButton('закрыть', callback_data="CLOSE_MENU")
workout_calendar_callback = CallbackData('calendar', 'action', 'year', 'month', 'workout_id')


async def workout_calendar(workouts: Dict, year: int = datetime.now().year, month: int = datetime.now().month):
    calendar_menu = InlineKeyboardMarkup(row_width=7)

    ignore_callback = workout_calendar_callback.new(action="IGNORE", year=year, month=month,
                                                    workout_id=0)  # for buttons with no answer

    # First row - Month and Year
    calendar_menu.row()
    # calendar.insert(InlineKeyboardButton("<", callback_data=calendar_callback.new("PREV-YEAR", year, month, 1)))
    calendar_menu.insert(InlineKeyboardButton(f'{months[month]} {str(year)}', callback_data=ignore_callback))
    # calendar.insert(InlineKeyboardButton(">", callback_data=calendar_callback.new("NEXT-YEAR", year, month, 1)))

    if len(workouts) == 0:
        calendar_menu.row(InlineKeyboardButton("Нет тренировок!", callback_data=ignore_callback))
    else:
        # Second row - Week Days
        calendar_menu.row()
        for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
            calendar_menu.insert(InlineKeyboardButton(day, callback_data=ignore_callback))

        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            calendar_menu.row()
            for day in week:
                if day == 0:
                    calendar_menu.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
                else:
                    if day in workouts:
                        calendar_menu.insert(
                            InlineKeyboardButton(emoji['arm'],
                                                 callback_data=workout_calendar_callback.new(action="VIEW_WORKOUT",
                                                                                             year=year,
                                                                                             month=month,
                                                                                             workout_id=workouts[day])))
                    else:
                        calendar_menu.insert(InlineKeyboardButton(str(day), callback_data=ignore_callback))

    # Last row - Buttons
    calendar_menu.row()
    calendar_menu.insert(InlineKeyboardButton("<<",
                                              callback_data=workout_calendar_callback.new(action="PREV-MONTH",
                                                                                          year=year,
                                                                                          month=month, workout_id=0)))
    calendar_menu.insert(InlineKeyboardButton(">>",
                                              callback_data=workout_calendar_callback.new(action="NEXT-MONTH",
                                                                                          year=year,
                                                                                          month=month, workout_id=0)))
    calendar_menu.row(quit)
    return calendar_menu


async def workouts_list(workouts: List, offset: int = 0):
    menu = InlineKeyboardMarkup(row_width=1)

    next_page = InlineKeyboardButton(emoji['right'], callback_data=page_callback.new(offset + 1))
    previous_page = InlineKeyboardButton(emoji['left'], callback_data=page_callback.new(offset - 1))

    if workouts is None:
        if offset == 0:
            return menu.row(InlineKeyboardButton("Нет сохранненых тренировок!", callback_data="no_saved_workouts"))
        else:
            menu.row(previous_page)
            menu.row(quit)
            return menu

    for workout in workouts:
        workout_id = workout['id']
        date = (workout['date']).strftime('%d-%m-%Y')
        menu.row(InlineKeyboardButton(date, callback_data=view_workout_callback.new(offset=offset,
                                                                                    workout_id=workout_id)))

    if len(workouts) == 3:
        if offset != 0:
            menu.row(previous_page, next_page)
        else:
            menu.row(next_page)
    elif offset != 0:
        menu.row(previous_page)
    menu.row(quit)

    return menu


async def workout_menu(workout_id: int, date_raw: datetime, data: Dict):
    menu = InlineKeyboardMarkup(row_width=2)
    date = date_raw.strftime('%d-%m-%Y')

    # change_workout = InlineKeyboardButton(emoji['pencil'], callback_data=workout_change_callback.new(action='change',
    #                                                                                                  workout_id=workout_id))
    delete_workout = InlineKeyboardButton(emoji['cross'], callback_data=workout_change_callback.new(action='delete',
                                                                                                    workout_id=workout_id))
    share_workout = InlineKeyboardButton(emoji['megaphone'], switch_inline_query=date)

    back_to_workouts = InlineKeyboardButton(emoji['back_arrow'], callback_data=workout_calendar_callback.new(
        action="CURRENT-MONTH",
        year=data['year'],
        month=data['month'],
        workout_id=0))

    menu.row(delete_workout, share_workout)  # , change_workout)
    menu.row(back_to_workouts)
    menu.row(quit)

    return menu


async def confirm_delete_menu(workout_id: int):
    menu = InlineKeyboardMarkup(row_width=2)

    yes = InlineKeyboardButton("да", callback_data=delete_workout_callback.new(if_delete=True, workout_id=workout_id))
    no = InlineKeyboardButton("нет", callback_data=delete_workout_callback.new(if_delete=False, workout_id=workout_id))

    menu.row(no, yes)
    return menu
