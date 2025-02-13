from beanie import init_beanie

from src import constants
from .models import Pokemon, Trainer, Sudoers

class Database:
  __slots__ = ('client',)

  async def initialize(self):
    self.client = AsyncIOMotorClient(constants.DB_URL)
    await init_beanie(database=self.client.db_name, document_models=[Pokemon, Trainer, Sudoers])
    
