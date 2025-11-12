from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# --- CONFIGURAZIONE ---
TOKEN = "8256160734:AAGdwQ5UU-je6JANlKN_mOkjWwQrtCrdmZU"

# --- LOGGING ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- COMANDI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao ?? Sono il GymResultBot!\n\n"
        "Inviami un comando come:\n"
        "/analizza <link_gara> <Nome Cognome>\n"
        "E ti mostrerò i punteggi e i confronti ??"
    )

async def analizza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "?? Uso corretto: /analizza <link_gara> <Nome Cognome>"
        )
        return

    link = context.args[0]
    nome = " ".join(context.args[1:])
    await update.message.reply_text(
        f"Sto analizzando la gara per {nome}...\n?? {link}"
    )

# --- AVVIO BOT ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analizza", analizza))
    app.run_polling()

if __name__ == "__main__":
    print("?? Bot avviato... premi CTRL+C per fermarlo.")
    main()