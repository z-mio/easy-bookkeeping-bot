from .group_mgmt import GroupMgmt
from .bill_mgmt import BillMgmt
from .command_execute import CommandExecute


class Methods(GroupMgmt, BillMgmt, CommandExecute):
    pass
