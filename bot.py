import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scraper import get_gare_femminili, cerca_gara

# === CONFIGURAZIONE ===
with open("config.json") as f:
    config = json.load(f)

TOKEN = "INSERISCI_IL_TUO_TOKEN_TELEGRAM"  # <-- sostituisci con il tuo
logging.basicConfig(level=logging.INFO)

# === COMANDI TELEGRAM ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Ciao! Sono il bot di GymResult.\n"
        "Posso mostrarti le gare femminili disponibili o i risultati di una specifica gara.\n\n"
        "Comandi disponibili:\n"
        "• /gare — Mostra le gare femminili attive\n"
        "• /cerca <parola> — Cerca una gara per parola chiave\n"
        "• /set_categoria <nome> — Imposta la categoria da monitorare\n"
        "• /info — Mostra la categoria e atleta attuali"
    )

async def gare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gare = get_gare_femminili()
    if not gare:
        await update.message.reply_text("Nessuna gara femminile trovata al momento 💤")
        return

    text = "\n\n".join([f"🏅 {g['nome']}\n🔗 {g['link']}" for g in gare[:10]])
    await update.message.reply_text(f"Gare femminili trovate:\n\n{text}")

async def cerca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usa: /cerca <parola>")
        return
    parola = " ".join(context.args)
    risultati = cerca_gara(parola)
    if not risultati:
        await update.message.reply_text(f"Nessuna gara trovata per '{parola}'.")
        return
    text = "\n\n".join([f"🏅 {g['nome']}\n🔗 {g['link']}" for g in risultati[:10]])
    await update.message.reply_text(f"Risultati per '{parola}':\n\n{text}")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"📄 Categoria: {config['categoria']}\n"
        f"🤸‍♀️ Disciplina: {config['disciplina']}\n"
        f"👤 Atleta monitorata: {config['atleta']}\n"
        f"🔁 Aggiornamenti automatici: {config['aggiornamenti_automatici']}"
    )
    await update.message.reply_text(msg)

async def set_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usa: /set_categoria <nome_categoria>")
        return
    nuova = " ".join(context.args)
    config["categoria"] = nuova
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    await update.message.reply_text(f"✅ Categoria aggiornata a: {nuova}")

# === AVVIO BOT ===

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gare", gare))
app.add_handler(CommandHandler("cerca", cerca))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("set_categoria", set_categoria))

if __name__ == "__main__":
    app.run_polling()
