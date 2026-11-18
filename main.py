
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@Best_mix_gym"

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set")

bot = telebot.TeleBot(TOKEN)

def check_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 عضویت در کانال", url="https://t.me/Best_mix_gym")
    )
    markup.add(
        InlineKeyboardButton("✅ بررسی عضویت", callback_data="check")
    )
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    if check_member(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "🎉 خوش آمدی! عضویت شما تأیید شد."
        )
    else:
        bot.send_message(
            message.chat.id,
            "برای استفاده از ربات ابتدا عضو کانال شو:",
            reply_markup=main_menu()
        )

@bot.callback_query_handler(func=lambda call: call.data == "check")
def verify(call):
    if check_member(call.from_user.id):
        bot.answer_callback_query(call.id, "عضویت تأیید شد ✅")
        bot.send_message(
            call.message.chat.id,
            "🎉 خوش آمدی! حالا می‌توانی از ربات استفاده کنی."
        )
    else:
        bot.answer_callback_query(
            call.id,
            "هنوز عضو کانال نشده‌ای!",
            show_alert=True
        )

@bot.message_handler(commands=["admin"])
def admin(message):
    if message.from_user.id == 0:
        bot.send_message(message.chat.id, "پنل مدیریت")
    else:
        bot.send_message(message.chat.id, "شما دسترسی مدیریت ندارید.")

print("Bot is running...")
bot.infinity_polling()
