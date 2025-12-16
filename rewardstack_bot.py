from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from sqlalchemy.orm import Session
from database import Session as DBSession, User
from config import BOT_TOKEN, PLANS
import os

# ===== Main Menu Keyboard =====
def main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("🚀 Plans", callback_data="plans")],
        [InlineKeyboardButton("💳 Buy Booster", callback_data="buy")],
        [InlineKeyboardButton("🏦 Set Wallet", callback_data="set_wallet")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== /start Command =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = DBSession()
    user_id = update.effective_user.id
    username = update.effective_user.username

    user = session.get(User, user_id)
    if not user:
        user = User(telegram_id=user_id, username=username)
        session.add(user)
        session.commit()

    await update.message.reply_text(
        "👋 Welcome to RewardStack Bot!\nSelect an option below:",
        reply_markup=main_menu()
    )

# ===== Button Callback Handler =====
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    session = DBSession()
    user = session.get(User, query.from_user.id)

    if not user:
        await query.message.reply_text("❌ You are not registered. Use /start first.")
        return

    if query.data == "balance":
        await query.message.reply_text(
            f"💼 Balance: {user.balance:.2f} USDT\n"
            f"📦 Daily reward: {user.daily_reward} USDT\n"
            f"⬇ Min withdrawal: {user.min_withdraw} USDT",
            reply_markup=main_menu()
        )
    elif query.data == "plans":
        text = "🚀 Available Booster Plans:\n\n"
        for cost, p in PLANS.items():
            if cost == 0: continue
            text += f"🔹 {cost} USDT → {p['daily']} USDT/day | Withdraw {p['min_withdraw']} USDT\n"
        await query.message.reply_text(text, reply_markup=main_menu())
    elif query.data == "buy":
        text = "📌 To buy a booster, send the amount you want to buy (10, 15, 30, 50 USDT).\nExample: `10`"
        await query.message.reply_text(text, reply_markup=main_menu())
    elif query.data == "set_wallet":
        await query.message.reply_text(
            "Please send your **TRC20 USDT wallet address** now.",
            reply_markup=main_menu()
        )

# ===== Save Wallet Sent by User =====
async def save_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet = update.message.text.strip()
    session = DBSession()
    user = session.get(User, update.effective_user.id)

    if not user:
        await update.message.reply_text("❌ You are not registered. Use /start first.")
        return

    if user.trc20_wallet:
        await update.message.reply_text("✅ Wallet already saved.", reply_markup=main_menu())
        return

    if not wallet.startswith("T") or len(wallet) < 34:
        await update.message.reply_text("❌ Invalid TRC20 wallet address.", reply_markup=main_menu())
        return

    user.trc20_wallet = wallet
    session.commit()

    await update.message.reply_text(
        "✅ Wallet saved successfully!\n"
        "You are now on the FREE plan.\n"
        f"💰 Daily reward: {user.daily_reward} USDT\n"
        f"⬇ Minimum withdrawal: {user.min_withdraw} USDT",
        reply_markup=main_menu()
    )

# ===== Main =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_wallet))

    app.run_polling()

if __name__ == "__main__":
    main()
