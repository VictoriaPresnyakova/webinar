from dataclasses import dataclass
from datetime import datetime

from database import StatusEnum


@dataclass()
class User:
    id: int
    created_at: datetime
    status: StatusEnum
    status_updated_at: datetime
    msg_num: int
    msg_to_send_at: datetime
