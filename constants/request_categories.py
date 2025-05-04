from typing import Final

ANNUAL_LEAVE: Final[str] = "Annual Leave"
SICK_LEAVE: Final[str] = "Sick Leave"
WORK_REMOTELY: Final[str] = "Work Remotely"

# Categories where overlapping is allowed
ALLOW_OVERLAP_WITH: Final[set[str]] = {WORK_REMOTELY}
