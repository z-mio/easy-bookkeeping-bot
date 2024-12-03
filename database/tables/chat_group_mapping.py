from sqlalchemy import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from database.tables.base import Base


class ChatGroupMapping(Base):
    __tablename__ = "chat_group_mapping"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    chat_id: Mapped[int] = mapped_column(INTEGER, unique=True)  # TG对话ID
    group_id: Mapped[int] = mapped_column(INTEGER)  # 分组ID
