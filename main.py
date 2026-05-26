from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from email_service import send_received_email, send_confirmation_email, send_admin_notification
from meet_service import create_meet_link

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://scamehospital.netlify.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_EMAIL = "scamehospital@gmail.com"

# --- Request Models ---
class RegistrationRequest(BaseModel):
    name: str
    email: str
    scam_type: str
    package: str
    date: str
    time: str

# --- Existing Routes ---
@app.get("/")
def root():
    return {"message": "Scam Hospital API is running!"}

@app.post("/analyze")
def analyze(data: dict):
    message = data.get("message", "")
    return {
        "risk_score": 80,
        "category": "Phishing",
        "message": message,
    }

# --- Called when user clicks Proceed to Payment ---
@app.post("/register")
def register(data: RegistrationRequest):
    send_received_email(data.name, data.email, data.scam_type)
    send_admin_notification(ADMIN_EMAIL, data.name, data.email, data.scam_type, data.package, data.date, data.time)
    return {"status": "ok"}

# --- Called when user clicks Pay button ---
@app.post("/initialize-payment")
def initialize_payment(data: dict):
    return {
        "payment_url": "https://paystack.com/pay/test-payment-link"
    }

# --- Called by Paystack after successful payment ---
@app.post("/paystack-webhook")
async def paystack_webhook(request: Request):
    payload = await request.json()
    if payload.get("event") == "charge.success":
        meta = payload["data"]["metadata"]
        name = meta["name"]
        email = meta["email"]
        scam_type = meta.get("scam_type", "Unknown")
        package = meta["package"]
        date = meta["date"]
        time = meta["time"]
        meet_link = create_meet_link(name, email, date, time)
        send_confirmation_email(name, email, package, date, time, meet_link)
        send_admin_notification(ADMIN_EMAIL, name, email, scam_type, package, date, time)
    return {"status": "ok"}

# --- Called by Flutterwave after successful payment ---
@app.post("/flutterwave-webhook")
async def flutterwave_webhook(request: Request):
    payload = await request.json()
    if payload.get("event") == "charge.success":
        data = payload.get("data", {})
        meta = data.get("metadata", {})
        name = meta.get("name", "Customer")
        email = meta.get("email", "")
        scam_type = meta.get("scam_type", "Unknown")
        package = meta.get("package", "Unknown")
        date = meta.get("date", "")
        time = meta.get("time", "")
        meet_link = create_meet_link(name, email, date, time)
        send_confirmation_email(name, email, package, date, time, meet_link)
        send_admin_notification(ADMIN_EMAIL, name, email, scam_type, package, date, time)
    return {"status": "ok"}