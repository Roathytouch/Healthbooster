from aiohttp import web
import json
import requests

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token
TELEGRAM_API = f"https://api.telegram.org/bot{8148818305:AAHtrO5_G4HfZSy4vL9oDDthELYEzEWey8A}"

async def handle_webhook(request):
    update = await request.json()
    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")

    # Conversational logic
    if text == "/start":
        message = "Welcome to our shop! 🍽️ Use /menu to see items, /order to track, or /support for help."
        reply_markup = {
            "inline_keyboard": [
                [{"text": "View Menu", "callback_data": "menu"}],
                [{"text": "Support", "callback_data": "support"}]
            ]
        }
    elif text == "/menu" or update.get("callback_query", {}).get("data") == "menu":
        message = "Our Menu:\n🍕 Pizza - $10\n🍔 Burger - $8\n🍣 Sushi - $12"
        reply_markup = {
            "inline_keyboard": [[{"text": "Place Order", "callback_data": "order"}]]
        }
    elif text == "/order" or update.get("callback_query", {}).get("data") == "order":
        message = "Your order #123 is being prepared. We'll notify you when it ships!"
        reply_markup = None
    elif text == "/support":
        message = "Contact us at support@yourshop.com or ask here!"
        reply_markup = None
    else:
        message = "Sorry, I didn't understand. Try /menu or /support."
        reply_markup = None

    # Send response
    payload = {"chat_id": chat_id, "text": message}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)

    # Handle callback queries (button clicks)
    if "callback_query" in update:
        callback_id = update["callback_query"]["id"]
        requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={"callback_query_id": callback_id})

    return web.Response()

app = web.Application()
app.router.add_post("/webhook", handle_webhook)

if __name__ == "__main__":
    web.run_app(app, port=3000)
