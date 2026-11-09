import telebot
from telebot import types
import time

PART1 = '9010916803:AAH-'
PART2 = 'FiHdtYzPhMBGRsNpKzAaZrpbufltFQY'
TOKEN = PART1 + PART2
ADMIN_ID = 8710363965

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("💎 86 Diamonds (MLBB)", callback_data="buy_86")
        btn2 = types.InlineKeyboardButton("💎 Weekly Diamond Pass", callback_data="buy_wdp")
        markup.add(btn1, btn2)
        
        bot.send_message(
            message.chat.id,
            "👋 မင်္ဂလာပါ ဗျ။\n\nBenett Store မှ ကြိုဆိုပါတယ်။ ကျေးဇူးပြု၍ လိုချင်သော Package ကို ရွေးချယ်ပါ။",
            reply_markup=markup
        )
    except Exception as e:
        print(f"Error in start: {e}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.answer_callback_query(call.id)
        
        if call.data == "buy_86":
            msg = bot.send_message(
                call.message.chat.id,
                "📦 သင်ရွေးချယ်ထားသော Package: **86 Diamonds**\n\nကျေးဇူးပြု၍ သင့်၏ **Game ID နှင့် Server ID** ကို ရိုက်ထည့်ပေးပါ (ဥပမာ: 12345678 1234)"
            )
            bot.register_next_step_handler(msg, receive_game_id, "86 Diamonds")
            
        elif call.data == "buy_wdp":
            msg = bot.send_message(
                call.message.chat.id,
                "📦 သင်ရွေးချယ်ထားသော Package: **Weekly Diamond Pass**\n\nကျေးဇူးပြု၍ သင့်၏ **Game ID နှင့် Server ID** ကို ရိုက်ထည့်ပေးပါ (ဥပမာ: 12345678 1234)"
            )
            bot.register_next_step_handler(msg, receive_game_id, "Weekly Diamond Pass")
    except Exception as e:
        print(f"Callback error: {e}")

def receive_game_id(message, package_name):
    try:
        user_game_id = message.text
        chat_id = message.chat.id
        
        bot.send_message(
            chat_id,
            f"✅ ရရှိပါပြီ။\n\n📦 Package: {package_name}\n🆔 Game ID: {user_game_id}\n\nကျေးဇူးပြု၍ ငွေလွှဲပြေစာ (Screenshot) ပုံကို ပို့ပေးပါ။"
        )
        bot.register_next_step_handler(message, receive_slip, package_name, user_game_id)
    except Exception as e:
        print(f"Game ID error: {e}")

def receive_slip(message, package_name, user_game_id):
    if message.photo:
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            caption = (
                f"🚨 **ငွေလွှဲပြေစာ အသစ်ရောက်ရှိပါပြီ!**\n\n"
                f"👤 ဝယ်ယူသူ ID: `{message.from_user.id}`\n"
                f"👤 အမည်: {message.from_user.first_name}\n"
                f"📦 Package: {package_name}\n"
                f"🆔 Game ID: {user_game_id}"
            )
            bot.send_photo(ADMIN_ID, downloaded_file, caption=caption, parse_mode="Markdown")
            bot.reply_to(message, "✅ ငွေလွှဲပြေစာ (Slip) လက်ခံရရှိပါပြီ။\nAdmin မှ စစ်ဆေးပြီးပါက သင့်အကောင့်သို့ Diamond ဖြည့်သွင်းပေးပါမည်။ ကျေးဇူးတင်ပါတယ်။")
        except Exception as e:
            print(f"Error sending to admin: {e}")
    else:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ငွေလွှဲပြေစာ (Screenshot) ပုံကိုသာ ပို့ပေးပါ။")
        bot.register_next_step_handler(message, receive_slip, package_name, user_game_id)

if __name__ == "__main__":
    print("Bot is running...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Connection error: {e}, restarting in 5 seconds...")
            time.sleep(5)
          
