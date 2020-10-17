from models.alert import Alert
from dotenv import load_dotenv

load_dotenv()

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()
    alert.json()

if not alerts:
    print("No alerts in db.")
