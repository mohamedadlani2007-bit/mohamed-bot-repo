import os
import logging
from datetime import datetime, timedelta
import json
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('BOT_TOKEN', '8348188479:AAFMAzyBi5KQzdYEFTEtz1ktnhqnmclat7Q')

clients = {}
user_sessions = {}

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("➕ إضافة عميل جديد", callback_data='add_client')],
        [InlineKeyboardButton("📋 قائمة العملاء", callback_data='list_clients')],
        [InlineKeyboardButton("⏱️ تمديد اشتراك", callback_data='extend_subscription')],
        [InlineKeyboardButton("🚫 حذف عميل", callback_data='delete_client')],
        [InlineKeyboardButton("📊 إحصائيات", callback_data='stats')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_protocol_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔹 Trojan", callback_data='protocol_trojan')],
        [InlineKeyboardButton("🔸 V2Ray", callback_data='protocol_v2ray')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_duration_keyboard():
    keyboard = [
        [InlineKeyboardButton("15 دقيقة", callback_data='dur_15m'), InlineKeyboardButton("30 دقيقة", callback_data='dur_30m')],
        [InlineKeyboardButton("1 ساعة", callback_data='dur_1h'), InlineKeyboardButton("6 ساعات", callback_data='dur_6h')],
        [InlineKeyboardButton("12 ساعة", callback_data='dur_12h'), InlineKeyboardButton("1 يوم", callback_data='dur_1d')],
        [InlineKeyboardButton("7 أيام", callback_data='dur_7d'), InlineKeyboardButton("30 يوم", callback_data='dur_30d')],
        [InlineKeyboardButton("365 يوم", callback_data='dur_365d'), InlineKeyboardButton("♾️ غير محدود", callback_data='dur_unlimited')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_client_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_config(protocol, duration):
    return f"""
{protocol} Configuration
========================
Server: vpn.example.com
Port: 443
Protocol: {protocol}
Duration: {duration}
UUID: {''.join(random.choices(string.hexdigits.lower(), k=8))}-{''.join(random.choices(string.hexdigits.lower(), k=4))}-{''.join(random.choices(string.hexdigits.lower(), k=4))}-{''.join(random.choices(string.hexdigits.lower(), k=4))}-{''.join(random.choices(string.hexdigits.lower(), k=12))}
Password: {''.join(random.choices(string.ascii_letters + string.digits, k=12))}
"""

def format_duration(duration):
    if duration is None:
        return "♾️ غير محدود"
    days = duration.days
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    parts = []
    if days > 0: parts.append(f"{days} يوم")
    if hours > 0: parts.append(f"{hours} ساعة")
    if minutes > 0: parts.append(f"{minutes} دقيقة")
    return "، ".join(parts) if parts else "أقل من دقيقة"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🌟 مرحباً بك {user.first_name}!\n\n🔹 بوت إدارة اشتراكات VPN\n\n📌 اختر من القائمة:",
        reply_markup=get_main_keyboard()
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data == 'add_client':
        await query.edit_message_text("🔹 اختر نوع البروتوكول:", reply_markup=get_protocol_keyboard())
        user_sessions[user_id] = {'step': 'protocol'}
    
    elif data == 'list_clients':
        if not clients:
            await query.edit_message_text("📋 لا يوجد عملاء حالياً", reply_markup=get_main_keyboard())
            return
        text = "📋 قائمة العملاء:\n\n"
        for cid, c in clients.items():
            status = "🟢" if c['expiry'] is None or c['expiry'] > datetime.now() else "🔴"
            expiry = "غير محدود" if c['expiry'] is None else c['expiry'].strftime('%Y/%m/%d %H:%M')
            text += f"{status} `{cid}` - {c['protocol']} | {expiry}\n"
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=get_main_keyboard())
    
    elif data == 'extend_subscription':
        if not clients:
            await query.edit_message_text("📋 لا يوجد عملاء للتمديد", reply_markup=get_main_keyboard())
            return
        text = "⏱️ اختر العميل للتمديد:\n\n"
        for cid in list(clients.keys())[:5]:
            text += f"• أرسل المعرف: `{cid}`\n"
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=get_main_keyboard())
    
    elif data == 'delete_client':
        if not clients:
            await query.edit_message_text("📋 لا يوجد عملاء للحذف", reply_markup=get_main_keyboard())
            return
        text = "🚫 اختر العميل للحذف:\n\n"
        for cid in list(clients.keys())[:5]:
            text += f"• أرسل المعرف: `{cid}`\n"
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=get_main_keyboard())
    
    elif data == 'stats':
        total = len(clients)
        active = sum(1 for c in clients.values() if c['expiry'] is None or c['expiry'] > datetime.now())
        text = f"📊 الإحصائيات:\n\n👥 إجمالي العملاء: {total}\n🟢 نشط: {active}\n🔴 منتهي: {total - active}"
        await query.edit_message_text(text, reply_markup=get_main_keyboard())
    
    elif data == 'back_main':
        await query.edit_message_text("🌟 القائمة الرئيسية:", reply_markup=get_main_keyboard())
        user_sessions.pop(user_id, None)
    
    elif data.startswith('protocol_'):
        protocol = data.replace('protocol_', '').upper()
        user_sessions[user_id]['protocol'] = protocol
        user_sessions[user_id]['step'] = 'duration'
        await query.edit_message_text(f"✅ تم اختيار {protocol}\n📌 اختر المدة:", reply_markup=get_duration_keyboard())
    
    elif data.startswith('dur_'):
        duration_map = {
            '15m': timedelta(minutes=15), '30m': timedelta(minutes=30),
            '1h': timedelta(hours=1), '6h': timedelta(hours=6),
            '12h': timedelta(hours=12), '1d': timedelta(days=1),
            '7d': timedelta(days=7), '30d': timedelta(days=30),
            '365d': timedelta(days=365), 'unlimited': None
        }
        duration = duration_map.get(data.replace('dur_', ''), timedelta(days=1))
        session = user_sessions.get(user_id, {})
        protocol = session.get('protocol', 'TROJAN')
        
        client_id = generate_client_id()
        expiry = None if duration is None else datetime.now() + duration
        clients[client_id] = {
            'id': client_id, 'protocol': protocol, 'duration': duration,
            'expiry': expiry, 'created_at': datetime.now(),
            'config': generate_config(protocol, format_duration(duration))
        }
        
        expiry_text = "غير محدود" if expiry is None else expiry.strftime('%Y/%m/%d %H:%M')
        await query.edit_message_text(
            f"✅ تم إضافة العميل!\n\n🆔 المعرف: `{client_id}`\n🔹 البروتوكول: {protocol}\n⏱️ المدة: {format_duration(duration) if duration else 'غير محدود'}\n📅 ينتهي: {expiry_text}\n\n📋 الإعدادات:\n```\n{clients[client_id]['config']}\n```",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        user_sessions.pop(user_id, None)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # محاولة حذف عميل
    if text.startswith('delete_'):
        client_id = text.replace('delete_', '')
        if client_id in clients:
            del clients[client_id]
            await update.message.reply_text(f"✅ تم حذف العميل `{client_id}`", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ العميل غير موجود")
        return
    
    # محاولة تمديد عميل
    if text.startswith('extend_'):
        client_id = text.replace('extend_', '')
        if client_id in clients:
            clients[client_id]['expiry'] = datetime.now() + timedelta(days=30)
            await update.message.reply_text(f"✅ تم تمديد اشتراك `{client_id}` لمدة 30 يوم", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ العميل غير موجود")
        return
    
    await update.message.reply_text("📌 استخدم الأزرار أو الأوامر: /start")

def main():
    print("🚀 تشغيل البوت...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت يعمل! اضغط Ctrl+C للإيقاف")
    app.run_polling(allowed_updates=[])

if __name__ == "__main__":
    main()
