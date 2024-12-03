from accounting.database.base.db import DB
from database import async_session
from methods.chat_group_mapping_mgmt import ChatGroupMappingMgmt


class Methods(ChatGroupMappingMgmt):
    def __init__(self):
        self.db = DB(async_session)
        super().__init__()
