from datetime import date, datetime, timedelta, timezone

ISLAND_TIMEZONE = timezone(timedelta(hours=5), "Maldives")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def island_today() -> date:
    return utc_now().astimezone(ISLAND_TIMEZONE).date()


def validate_stay(check_in: date, check_out: date) -> None:
    if check_in < island_today():
        raise ValueError("Check-in cannot be in the past")
    if check_out <= check_in:
        raise ValueError("Check-out must be after check-in")
    if (check_out - check_in).days > 365:
        raise ValueError("A stay cannot exceed 365 nights")
