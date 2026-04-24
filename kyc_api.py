from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Custom names
names = [
    "Abel Tuter",
    "Abraham Lincoln",
    "Ace Ford",
    "Adela Cervantsz",
    "Adriana Wolfe",
    "Aileen Mottern",
    "Akshat Jain",
    "Alejandra Prenatt",
    "Alejandro Mascall",
    "Alene Rabeck"
]

# Dataset
mock_db = {
    "india": {

        "AADHAAR": [
            {"name": names[i], "aadhaar": str(111122223330 + i)}
            for i in range(10)
        ],

        "PAN": [
            {"name": names[i], "pan": f"ABCDE1234{chr(65+i)}"}
            for i in range(10)
        ],

        "GST": [
            {"name": names[i], "gst": f"22ABCDE1234F1Z{i}"}
            for i in range(10)
        ],

        "INCORPORATION": [
            {"name": names[i], "cin": f"U12345DL2020PTC10000{i}"}
            for i in range(10)
        ]
    }
}

class VerifyRequest(BaseModel):
    country: str
    doc_type: str
    value: str

@app.post("/verify")
def verify_doc(req: VerifyRequest):

    country = req.country.lower()
    doc_type = req.doc_type.upper()
    value = req.value

    if country not in mock_db:
        raise HTTPException(status_code=400, detail="Unsupported country")

    if doc_type not in mock_db[country]:
        raise HTTPException(status_code=400, detail="Unsupported document type")

    for record in mock_db[country][doc_type]:

        if doc_type == "AADHAAR" and record["aadhaar"] == value:
            return success_response(record)

        elif doc_type == "PAN" and record["pan"] == value:
            return success_response(record)

        elif doc_type == "GST" and record["gst"] == value:
            return success_response(record)

        elif doc_type == "INCORPORATION" and record["cin"] == value:
            return success_response(record)

    return {
        "status": "failed",
        "message": "Document not found"
    }

def success_response(record):
    return {
        "status": "success",
        "message": "Document verified",
        "data": record
    }
