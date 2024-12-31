import requests
import json
from config import MIDTRANS_CLIENT_KEY, MIDTRANS_SERVER_KEY, MIDTRANS_URL

headers = {
    'Authorization': f'Basic {MIDTRANS_SERVER_KEY}',
    'Content-Type': 'application/json'
}

transaction_data = {
    "payment_type": "bank_transfer",  # Metode pembayaran: transfer bank
    "transaction_details": {
        "order_id": "order-id-12345",
        "gross_amount": 100000  # Total pembayaran
    },
    "bank_transfer": {
        "bank": "bca"  # Pilihan bank tujuan, misalnya BCA
    }
}

response = requests.post(MIDTRANS_URL, headers=headers, data=json.dumps(transaction_data))

if response.status_code == 201:
    print("Pembayaran berhasil:", response.json())
else:
    print("Error dalam proses pembayaran:", response.json())
