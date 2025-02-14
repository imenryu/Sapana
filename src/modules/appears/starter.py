from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from constants import BOT_TOKEN  # Import the bot token from constants.py

# Define the starter Pokémon
STARTERS = ["Bulbasaur", "Charmander", "Squirtle", "Choose None"]

async def start(update: Update, context: CallbackContext) -> None:
    """Handler for the /start command."""
    # Create a custom keyboard with the starter Pokémon options
    keyboard = [STARTERS]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    # Send the message with the starter options
    await update.message.reply_text(
        "Welcome to the Pokémon world! Choose your starter Pokémon:",
        reply_markup=reply_markup
    )

async def handle_choice(update: Update, context: CallbackContext) -> None:
    """Handler for user's choice."""
    user_choice = update.message.text
    
    if user_choice in STARTERS:
        if user_choice == "Choose None":
            await update.message.reply_text("You chose none. Here's your Pikachu! ⚡")
        else:
            await update.message.reply_text(f"You chose {user_choice}! Great choice!")
    else:
        await update.message.reply_text("Invalid choice. Please try again.")

def main() -> None:
    """Start the bot."""
    # Use the bot token from constants.py
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
