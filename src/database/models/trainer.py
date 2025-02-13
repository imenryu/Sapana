from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field

from pokedex import enums


class RefferalRequirements:
    level = 10
    pokemon_seen = 20
    pokemon_obtained = 5
    pokemon_caught = 10
    pokeballs_used = 50
    win = 5
    loss = 3

class Trainer(Document):

    class Settings:
        name = 'trainer'
        keep_nulls = False
        use_cache = True
        use_revision = True
        use_state_management = True
        state_management_replace_objects = True

    # General
    user_id: int
    timestamp: datetime = Field(default_factory=datetime.utcnow, frozen=True)
    referred_by: Optional[int] = Field(default=None)

    # Details
    xp: int = Field(default=0)

    # Region 
    region: enums.Region = Field(default=enums.Region.KANTO)

    # Pokémon
    pokemon_seen: list = Field(default=[])
    pokemon_obtained: list = Field(default=[])

    shiny_pokemon_caught_streak: int = Field(default=0)
    pokemon_caught_streak: int = Field(default=0)

    shiny_pokemon_caught: int = Field(default=0)
    pokemon_caught: int = Field(default=0)
    pokemon_released: int = Field(default=0)

    pokeballs_used: int = Field(default=0)

    # Battle
    win: int = Field(default=0)
    win_strike: int = Field(default=0)
    loss: int = Field(default=0)
    trophy: int = Field(default=0)

    # Shop
    balance: int = Field(default=0)

    @property
    def is_valid_refferal(self):
        return (self.level >= ReferralRequirements.level and
                len(self.pokemon_seen) >= ReferralRequirements.pokemon_seen and
                len(self.pokemon_obtained) >= ReferralRequirements.pokemon_obtained and
                self.pokemon_caught >= ReferralRequirements.pokemon_caught and
                self.pokeballs_used >= ReferralRequirements.pokeballs_used and
                self.win >= ReferralRequirements.win
                self.loss >= ReferralRequirements.loss)
