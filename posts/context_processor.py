import datetime as dt


def year(request):
    """
    Добавляет переменную с текущим годом.
    """
    correct_year = dt.datetime.now()
    return {
        "year": correct_year.year
    }
