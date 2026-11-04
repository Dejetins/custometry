"""Pin package TZif bytes at creation; never consult the host database."""

import base64
import hashlib
from importlib.resources import files
import tzdata
from packages.contracts.semantic import (
    CalendarFailure,
    ZonedCalendarInputV2,
    ZonedCalendarProfileV2,
)


class PackagedCalendarRules:
    def resolve(self, profile: ZonedCalendarInputV2) -> ZonedCalendarProfileV2:
        try:
            resource = files("tzdata.zoneinfo").joinpath(*profile.timezone.split("/"))
            data = resource.read_bytes()
            return ZonedCalendarProfileV2(
                **profile.model_dump(),
                tzdata_version=tzdata.__version__,
                tzif_base64=base64.b64encode(data).decode("ascii"),
                tzif_sha256=hashlib.sha256(data).hexdigest(),
            )
        except (OSError, ValueError, EOFError) as exc:
            raise CalendarFailure("CALENDAR_TIMEZONE_UNAVAILABLE") from exc
