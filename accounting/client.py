from .database import async_session
from .database.base.db import DB
from .methods import Methods
from .utiles.singleton import singleton
from .tools import Tools


@singleton
class Accounting(Methods, Tools):
    def __init__(self):
        self.db = DB(async_session)
        super().__init__()


acc = Accounting()
