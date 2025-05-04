from datetime import date
from dao.time_off_dao import TimeOffDao
from models.time_off import TimeOffRequest, TimeOffCategory
from utils.exceptions import TimeOffOverlapError
from constants.request_categories import ALLOW_OVERLAP_WITH
class TimeOffService:
    """
    Handles time off request business rules and logic.
    Delegates all DB interactions to TimeOffDao.
    """

    def __init__(self, dao: TimeOffDao) -> None:
        self._dao = dao

    def has_disallowed_overlap(
        self,
        *,
        employee_id: str,
        new_start: date,
        new_end: date,
        new_category_id: int
    ) -> bool:
        new_category: TimeOffCategory = self._dao.get_category(category_id=new_category_id)

        overlapping: list[TimeOffRequest] = self._dao.get_overlapping_requests(
            employee_id=employee_id,
            start=new_start,
            end=new_end
        )

        for existing_request in overlapping:
            existing_category = self._dao.get_category(category_id=existing_request.request_category_id)

            if self._overlap_is_disallowed(new_category.name, existing_category.name):
                return True

        return False

    def create_time_off_request(
        self,
        *,
        employee_id: str,
        category_id: int,
        start_date: date,
        end_date: date
    ) -> None:
        if self.has_disallowed_overlap(
            employee_id=employee_id,
            new_start=start_date,
            new_end=end_date,
            new_category_id=category_id
        ):
            raise TimeOffOverlapError("Overlapping time off request not allowed unless one is 'Work Remotely'")

        self._dao.insert_time_off_request(
            employee_id=employee_id,
            category_id=category_id,
            start=start_date,
            end=end_date
        )

    @staticmethod
    def _overlap_is_disallowed(new: str, existing: str) -> bool:
        """
        Returns True if neither category allows overlap.
        """
        return new not in ALLOW_OVERLAP_WITH and existing not in ALLOW_OVERLAP_WITH
