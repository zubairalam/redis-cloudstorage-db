from pydantic import BaseModel
from typing import Literal
from datetime import datetime, UTC
from . import DBClient

class UserInfo(BaseModel):
	guid: str | None = None
	emails: list[str] | None = []
	state: Literal['FREE-TRIAL', 'AD-SUPPORTED', 'PAID'] | None = 'AD-SUPPORTED'
	num_hidden_apps: int | None = 0
	last_deleted_at: datetime | None = datetime(2000, 1, 1, 0, 0)
	created_at: datetime = datetime.now(UTC)
	modified_at: datetime = datetime.now(UTC)
	auto_renew: bool | None = False
	google_aid: str | None = '{}'


class UserInfoDAO:
	
	@classmethod
	def create_or_update(cls, userinfo: UserInfo, tracer):
		key = f"UserInfo:{userinfo.guid}"
		user_record = DBClient.get_by_key(key)
		user_record.update(userinfo.model_dump())
		with tracer.start_as_current_span("put"):
			DBClient.put(user_record)
	
	@classmethod
	def get(cls, guid, tracer) -> UserInfo | None:
		key = f"UserInfo:{guid}"
		with tracer.start_as_current_span("get"):
			db_userinfo_row = DBClient.get(key)
		if db_userinfo_row:
			return UserInfo(**db_userinfo_row)
		return None
		

	
