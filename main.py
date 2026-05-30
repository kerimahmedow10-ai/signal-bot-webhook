from fastapi import FastAPI, Request
import httpx

app = FastAPI()

TELEGRAM_TOKEN = "7714536308:AAFbz8Vtx8kugXLSS-MdejC3qkMB781cink"
CHAT_ID = "@signalbot_po_ai" 

@app.post("/webhook")
async def receive_signal(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    
    pair = data.get("pair", "EUR/USD")
    direction = data.get("direction", "CALL")
    
    emoji = "🟢 CALL (ВВЕРХ)" if direction == "CALL" else "🔴 PUT (ВНИЗ)"
    
    text = (
        f"🚨 **ИИ-СИГНАЛ ОТ КОМПАНИИ SIGNALBOT** 🚨\n\n"
        f"📊 **Актив:** {pair}\n"
        f"⏱ **Таймфрейм:** 1m\n"
        f"⚡️ **ДЕЙСТВИЕ:** {emoji}\n"
        f"⏳ **Время экспирации:** 2 минуты\n\n"
        f"👉 Переходи на Pocket Option и открывай сделку!"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)
    
    return {"status": "success"}
