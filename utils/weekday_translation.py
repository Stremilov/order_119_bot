def get_weekday_ru(weekday) -> str or None:
    translation_dict = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье",
    }
    try:
        answer = translation_dict[weekday]
        return answer
    except KeyError:
        return None
