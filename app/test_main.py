import pytest
from unittest import mock
import datetime
from app.main import outdated_products


@pytest.mark.parametrize(
    "products, today, expected",
    [
        (
            [
                {"name": "salmon", "expiration_date": datetime.date(2022, 2, 10)},
                {"name": "chicken", "expiration_date": datetime.date(2022, 2, 5)},
                {"name": "duck", "expiration_date": datetime.date(2022, 2, 1)},
            ],
            datetime.date(2022, 2, 10),
            ["chicken", "duck"],
        ),
        (
            [
                {"name": "salmon", "expiration_date": datetime.date(2022, 2, 10)},
                {"name": "chicken", "expiration_date": datetime.date(2022, 2, 5)},
                {"name": "duck", "expiration_date": datetime.date(2022, 2, 1)},
            ],
            datetime.date(2022, 2, 6),
            ["chicken", "duck"],
        ),
        (
            [
                {"name": "salmon", "expiration_date": datetime.date(2022, 2, 10)},
                {"name": "chicken", "expiration_date": datetime.date(2022, 2, 5)},
                {"name": "duck", "expiration_date": datetime.date(2022, 2, 1)},
            ],
            datetime.date(2022, 2, 2),
            ["duck"],
        ),
        (
            [
                {"name": "salmon", "expiration_date": datetime.date(2022, 2, 1)},
                {"name": "chicken", "expiration_date": datetime.date(2022, 1, 31)},
            ],
            datetime.date(2022, 2, 2),
            ["salmon", "chicken"],
        ),
    ],
)
def test_outdated_products(products: list[dict], today: datetime.date, expected: list[str]) -> None:
    with mock.patch("app.main.datetime.date") as mock_date:
        mock_date.today.return_value = today
        mock_date.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)

        assert outdated_products(products) == expected
