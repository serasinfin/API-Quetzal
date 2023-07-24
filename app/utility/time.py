from datetime import datetime, timedelta, time


def days_from_now(days) -> datetime:
    return datetime.now().replace(hour=00, minute=00) + timedelta(days=days)


def days_ago(days) -> datetime:
    return datetime.now().replace(hour=00, minute=00) - timedelta(days=days)


def days_since(date_in) -> int:
    return (datetime.now() - date_in.replace(tzinfo=None)).days


def today_now() -> datetime:
    return datetime.now()


def current_time() -> time:
    return datetime.now().time()


def tomorrow() -> datetime:
    return datetime.now() + timedelta(days=1)


def start_today() -> datetime:
    return datetime.now().replace(hour=00, minute=00, second=00)


def end_today() -> datetime:
    return datetime.now().replace(hour=23, minute=59, second=59)
