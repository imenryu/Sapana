from hydrogram import filters
    
from src.decorators import router
from src.filters import SudoOnly

@router.message(filters.command('error') & SudoOnly)
async def test_error_command(client, message):
    msg = 'Error Test!'
    raise ValueError(msg)
