from accounting.log import logger
from database.tables import ChatGroupMapping
import methods


class ChatGroupMappingMgmt:
    async def add_chat_group_mapping(
        self: "methods.Methods",
        chat_id: int,
        group_id: int,
    ) -> ChatGroupMapping:
        """
        添加映射
        :param chat_id: Tg对话ID
        :param group_id: 账单ID
        :return:
        """
        logger.info(f"添加映射: chat_id={chat_id}, group_id={group_id}")
        return await self.db.add(ChatGroupMapping(chat_id=chat_id, group_id=group_id))

    async def delete_chat_group_mapping(
        self: "methods.Methods",
        chat_id: int,
    ) -> ChatGroupMapping:
        """
        删除映射
        :param chat_id: Tg对话ID
        :return:
        """
        logger.info(f"删除映射: chat_id={chat_id}")
        return await self.db.delete(
            ChatGroupMapping, ChatGroupMapping.chat_id == chat_id
        )

    async def get_chat_group_mapping(
        self: "methods.Methods",
        chat_id: int,
    ) -> ChatGroupMapping:
        """
        获取映射
        :param chat_id: Tg对话ID
        :return:
        """
        return await self.db.get_one(
            ChatGroupMapping, ChatGroupMapping.chat_id == chat_id
        )

    async def edit_chat_group_mapping(
        self: "methods.Methods",
        chat_id: int,
        group_id: int,
    ) -> ChatGroupMapping:
        """
        修改映射
        :param chat_id: Tg对话ID
        :param group_id: 账单ID
        :return:
        """
        logger.info(f"修改映射: chat_id={chat_id}, group_id={group_id}")
        return await self.db.update(
            ChatGroupMapping, ChatGroupMapping.chat_id == chat_id, group_id=group_id
        )
