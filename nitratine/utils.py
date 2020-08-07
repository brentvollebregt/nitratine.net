import datetime
import calendar
from pathlib import Path
import io
from dataclasses import dataclass
from typing import Tuple
import math

from PIL import Image


def chunk_list(l, n):
    """ Yield successive n-sized chunks from l. src: https://stackoverflow.com/a/312464 """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_nzst_timezone_for_date(date: datetime.date) -> datetime.timezone:
    """
    Identify the timezone for a specific date in New Zealand
    > Daylight saving starts each year at 2am on the last Sunday in September,
    > and ends at 3am on the first Sunday in April.
    """
    calendar_object = calendar.Calendar()

    # Get all the Sundays in September and then get the last - this is the target day
    SEPTEMBER = 9
    SUNDAY = 6
    last_sunday_in_september_day = [
        d
        for d in calendar_object.itermonthdays4(date.year, SEPTEMBER)
        if d[0] == date.year and d[1] == SEPTEMBER and d[3] == SUNDAY
    ][-1]
    last_sunday_in_september = datetime.date(
        year=last_sunday_in_september_day[0],
        month=last_sunday_in_september_day[1],
        day=last_sunday_in_september_day[2]
    )


    APRIL = 4
    first_sunday_in_april_day = [
        d
        for d in calendar_object.itermonthdays4(date.year, APRIL)
        if d[0] == date.year and d[1] == APRIL and d[3] == SUNDAY
    ][0]
    first_sunday_in_april = datetime.date(
        year=first_sunday_in_april_day[0],
        month=first_sunday_in_april_day[1],
        day=first_sunday_in_april_day[2]
    )

    if first_sunday_in_april < date < last_sunday_in_september:
        return datetime.timezone(datetime.timedelta(hours=12))
    else:
        return datetime.timezone(datetime.timedelta(hours=13))


@dataclass
class ResizedImage:
    image_bytes: bytes
    original_size: Tuple[int, int]
    resized_size: Tuple[int, int]


def get_resized_image(path: Path, new_width: int) -> ResizedImage:
    """ Get the bytes for a resized image """
    # Get image and calculate required ratio
    image = Image.open(str(path))
    original_size = image.size
    ratio = new_width / original_size[0]

    # Calculate new size and resize the image
    new_size = (math.floor(original_size[0] * ratio), math.floor(original_size[1] * ratio))
    image.thumbnail(new_size, Image.ANTIALIAS)

    # Turn the image into a bytes object
    bytes_io = io.BytesIO()
    image.save(bytes_io, format='PNG')

    return ResizedImage(bytes_io.getvalue(), original_size, new_size)


def guess_rendered_size(original_size: Tuple[int, int], max_with: int) -> Tuple[int, int]:
    """ Guesses the dimensions of a rendered image by taking into account the max with of the page """
    ratio = max_with / original_size[0]
    return math.floor(original_size[0] * ratio), math.floor(original_size[1] * ratio)
