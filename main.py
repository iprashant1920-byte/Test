import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI(title="ID Verification API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PATTERNS = {
    "AADHAAR": r"^[2-9][0-9]{11}$",
    "PAN": r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$",
    "GST": r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]Z[0-9A-Z]$",
    "PASSPORT": r"^[A-Z0-9]{6,9}$",
    "SSN": r"^\d{3}-\d{2}-\d{4}$",
    "EIN": r"^\d{2}-\d{7}$",
    "EMIRATES_ID": r"^\d{3}-\d{4}-\d{7}-\d{1}$",
    "TRADE_LICENSE": r"^[A-Z0-9]{6,12}$",
    "DRIVING_LICENSE": r"^[A-Z0-9]{8,16}$",
    "VAT": r"^[A-Z0-9]{8,12}$",
}

COUNTRY_ID_TYPES = {
    "India": ["AADHAAR", "PAN", "GST"],
    "UAE":   ["EMIRATES_ID", "TRADE_LICENSE", "VAT"],
    "UK":    ["PASSPORT", "DRIVING_LICENSE", "VAT"],
    "USA":   ["SSN", "EIN"],
}

DB = {
    "AADHAAR": {
        "234567890123": {"name": "Abel Tuter", "id_type": "AADHAAR", "id_number": "234567890123", "dob": "1990-03-15", "father_name": "Victor Tuter", "country": "India", "address": "12 MG Road, Bengaluru 560001", "gender": "Male", "status": "active"},
        "345678901234": {"name": "Abraham Lincoln", "id_type": "AADHAAR", "id_number": "345678901234", "dob": "1975-02-12", "father_name": "Thomas Lincoln", "country": "India", "address": "45 Connaught Place, New Delhi 110001", "gender": "Male", "status": "active"},
        "567890123456": {"name": "Angelique Schermerhorn", "id_type": "AADHAAR", "id_number": "567890123456", "dob": "1993-05-20", "father_name": "Hans Schermerhorn", "country": "India", "address": "78 Park Street, Kolkata 700016", "gender": "Female", "status": "active"},
        "678901234567": {"name": "Arron Ubhi", "id_type": "AADHAAR", "id_number": "678901234567", "dob": "1979-07-17", "father_name": "Gurdev Ubhi", "country": "India", "address": "23 Anna Salai, Chennai 600002", "gender": "Male", "status": "active"},
        "789012345678": {"name": "Athena Cantu", "id_type": "AADHAAR", "id_number": "789012345678", "dob": "1996-08-30", "father_name": "Miguel Cantu", "country": "India", "address": "56 Civil Lines, Jaipur 302006", "gender": "Female", "status": "active"},
    },
    "PAN": {
        # Same person as AADHAAR — names match exactly
        "ABCDE1234F": {"name": "Abel Tuter", "id_type": "PAN", "id_number": "ABCDE1234F", "dob": "1990-03-15", "father_name": "Victor Tuter", "country": "India", "pan_type": "Individual", "status": "active"},
        "PQRST6789K": {"name": "Abraham Lincoln", "id_type": "PAN", "id_number": "PQRST6789K", "dob": "1975-02-12", "father_name": "Thomas Lincoln", "country": "India", "pan_type": "Individual", "status": "active"},
        "QWERT1234L": {"name": "Angelique Schermerhorn", "id_type": "PAN", "id_number": "QWERT1234L", "dob": "1993-05-20", "father_name": "Hans Schermerhorn", "country": "India", "pan_type": "Individual", "status": "active"},
        "LKJHG1234Q": {"name": "Arron Ubhi", "id_type": "PAN", "id_number": "LKJHG1234Q", "dob": "1979-07-17", "father_name": "Gurdev Ubhi", "country": "India", "pan_type": "Individual", "status": "active"},
        "ASDFG1234H": {"name": "Athena Cantu", "id_type": "PAN", "id_number": "ASDFG1234H", "dob": "1996-08-30", "father_name": "Miguel Cantu", "country": "India", "pan_type": "Individual", "status": "active"},
        # PAN-only India users
        "ACEFD1234F": {"name": "Ace Ford", "id_type": "PAN", "id_number": "ACEFD1234F", "dob": "1988-02-28", "father_name": "Henry Ford", "country": "India", "pan_type": "Individual", "status": "active"},
        "LMNOP4321Z": {"name": "Adela Cervantsz", "id_type": "PAN", "id_number": "LMNOP4321Z", "dob": "1992-11-07", "father_name": "Ramon Cervantsz", "country": "India", "pan_type": "Individual", "status": "active"},
        "ALLYS6789K": {"name": "Allyson Gillispie", "id_type": "PAN", "id_number": "ALLYS6789K", "dob": "1999-02-25", "father_name": "Tom Gillispie", "country": "India", "pan_type": "Individual", "status": "active"},
        "AMOSN1234F": {"name": "Amos Linnan", "id_type": "PAN", "id_number": "AMOSN1234F", "dob": "1985-09-10", "father_name": "Peter Linnan", "country": "India", "pan_type": "Individual", "status": "active"},
        "ZXCVB6789P": {"name": "Angelo Ferentz", "id_type": "PAN", "id_number": "ZXCVB6789P", "dob": "1989-09-27", "father_name": "Kirk Ferentz", "country": "India", "pan_type": "Individual", "status": "active"},
        "TYUIO9876R": {"name": "Annabelle Coger", "id_type": "PAN", "id_number": "TYUIO9876R", "dob": "1999-06-14", "father_name": "David Coger", "country": "India", "pan_type": "Individual", "status": "active"},
        "POIUY9876T": {"name": "Arya Hajarha", "id_type": "PAN", "id_number": "POIUY9876T", "dob": "2000-03-22", "father_name": "Kaveh Hajarha", "country": "India", "pan_type": "Individual", "status": "active"},
        "MNBVC5432X": {"name": "Arya Stark", "id_type": "PAN", "id_number": "MNBVC5432X", "dob": "2001-05-05", "father_name": "Eddard Stark", "country": "India", "pan_type": "Individual", "status": "active"},
        "HJKLQ9876W": {"name": "Athena Fontanilla", "id_type": "PAN", "id_number": "HJKLQ9876W", "dob": "1994-03-09", "father_name": "Jose Fontanilla", "country": "India", "pan_type": "Individual", "status": "active"},
        "QAZWS1234E": {"name": "Audra Cantu", "id_type": "PAN", "id_number": "QAZWS1234E", "dob": "1994-01-14", "father_name": "Carlos Cantu", "country": "India", "pan_type": "Individual", "status": "active"},
    },
    "GST": {
        "22ABCDE1234F1Z5": {"gst_name": "Ace Ford Enterprises", "gst_number": "22ABCDE1234F1Z5", "owner_name": "Ace Ford", "date_of_creation": "2020-05-10", "expiry_date": "2030-05-10", "country": "India", "state": "Uttar Pradesh", "business_type": "Proprietorship", "status": "active"},
        "29LMNOP4321Z1Z9": {"gst_name": "Adela Cervantsz Trading", "gst_number": "29LMNOP4321Z1Z9", "owner_name": "Adela Cervantsz", "date_of_creation": "2019-03-15", "expiry_date": "2029-03-15", "country": "India", "state": "Karnataka", "business_type": "Partnership", "status": "active"},
        "27PQRST6789K1Z2": {"gst_name": "Allyson Gillispie & Co", "gst_number": "27PQRST6789K1Z2", "owner_name": "Allyson Gillispie", "date_of_creation": "2021-07-20", "expiry_date": "2031-07-20", "country": "India", "state": "Maharashtra", "business_type": "Proprietorship", "status": "active"},
        "33ZXCVB6789P1Z1": {"gst_name": "Angelo Ferentz Industries", "gst_number": "33ZXCVB6789P1Z1", "owner_name": "Angelo Ferentz", "date_of_creation": "2018-11-01", "expiry_date": "2028-11-01", "country": "India", "state": "Tamil Nadu", "business_type": "LLP", "status": "active"},
        "44TYUIO9876R1Z2": {"gst_name": "Annabelle Coger Exports", "gst_number": "44TYUIO9876R1Z2", "owner_name": "Annabelle Coger", "date_of_creation": "2022-01-08", "expiry_date": "2032-01-08", "country": "India", "state": "Rajasthan", "business_type": "Private Ltd", "status": "active"},
        "55POIUY9876T1Z3": {"gst_name": "Arya Hajarha Solutions", "gst_number": "55POIUY9876T1Z3", "owner_name": "Arya Hajarha", "date_of_creation": "2023-06-12", "expiry_date": "2033-06-12", "country": "India", "state": "Himachal Pradesh", "business_type": "Startup", "status": "active"},
        "66MNBVC5432X1Z4": {"gst_name": "Arya Stark Ventures", "gst_number": "66MNBVC5432X1Z4", "owner_name": "Arya Stark", "date_of_creation": "2022-09-20", "expiry_date": "2032-09-20", "country": "India", "state": "Punjab", "business_type": "Proprietorship", "status": "active"},
        "77HJKLQ9876W1Z5": {"gst_name": "Athena Fontanilla Consulting", "gst_number": "77HJKLQ9876W1Z5", "owner_name": "Athena Fontanilla", "date_of_creation": "2021-04-04", "expiry_date": "2031-04-04", "country": "India", "state": "West Bengal", "business_type": "LLP", "status": "active"},
        "88QAZWS1234E1Z6": {"gst_name": "Audra Cantu & Associates", "gst_number": "88QAZWS1234E1Z6", "owner_name": "Audra Cantu", "date_of_creation": "2020-12-01", "expiry_date": "2030-12-01", "country": "India", "state": "Odisha", "business_type": "Partnership", "status": "active"},
    },
    "EMIRATES_ID": {
        "784-1987-1234567-1": {"name": "Adriana Wolfe", "id_type": "EMIRATES_ID", "id_number": "784-1987-1234567-1", "dob": "1987-08-19", "nationality": "German", "country": "UAE", "emirate": "Dubai", "gender": "Female", "expiry_date": "2030-08-19", "status": "active"},
        "784-2001-7654321-2": {"name": "Alva Pennigton", "id_type": "EMIRATES_ID", "id_number": "784-2001-7654321-2", "dob": "1984-08-08", "nationality": "American", "country": "UAE", "emirate": "Abu Dhabi", "gender": "Female", "expiry_date": "2028-08-08", "status": "active"},
        "784-1999-2223334-1": {"name": "Annette Frietas", "id_type": "EMIRATES_ID", "id_number": "784-1999-2223334-1", "dob": "1999-04-22", "nationality": "Brazilian", "country": "UAE", "emirate": "Sharjah", "gender": "Female", "expiry_date": "2027-04-22", "status": "active"},
        "784-2002-8889990-1": {"name": "Ashley Leonesio", "id_type": "EMIRATES_ID", "id_number": "784-2002-8889990-1", "dob": "1996-07-28", "nationality": "Italian", "country": "UAE", "emirate": "Ajman", "gender": "Female", "expiry_date": "2029-07-28", "status": "active"},
    },
    "TRADE_LICENSE": {
        "TL123456": {"company_name": "Aileen Mottern Holdings", "trade_license_number": "TL123456", "owner_name": "Aileen Mottern", "date_of_creation": "2018-06-01", "expiry_date": "2028-06-01", "country": "UAE", "emirate": "Dubai", "business_activity": "General Trading", "status": "active"},
        "TRADE1234": {"company_name": "Akshat Jain FZE", "trade_license_number": "TRADE1234", "owner_name": "Akshat Jain", "date_of_creation": "2020-09-15", "expiry_date": "2030-09-15", "country": "UAE", "emirate": "Abu Dhabi", "business_activity": "IT Services", "status": "active"},
        "TRADE9876": {"company_name": "Andrew Jackson Trading LLC", "trade_license_number": "TRADE9876", "owner_name": "Andrew Jackson", "date_of_creation": "2017-03-22", "expiry_date": "2027-03-22", "country": "UAE", "emirate": "Dubai", "business_activity": "Import & Export", "status": "active"},
        "TL998877": {"company_name": "Annie Approver Retail LLC", "trade_license_number": "TL998877", "owner_name": "Annie Approver", "date_of_creation": "2021-12-10", "expiry_date": "2031-12-10", "country": "UAE", "emirate": "Sharjah", "business_activity": "Retail", "status": "active"},
        "TRADE7788": {"company_name": "Antione Mccleary Group", "trade_license_number": "TRADE7788", "owner_name": "Antione Mccleary", "date_of_creation": "2019-08-05", "expiry_date": "2029-08-05", "country": "UAE", "emirate": "Ras Al Khaimah", "business_activity": "Logistics", "status": "active"},
        "TL556677": {"company_name": "Ashley Parker Ventures", "trade_license_number": "TL556677", "owner_name": "Ashley Parker", "date_of_creation": "2022-04-18", "expiry_date": "2032-04-18", "country": "UAE", "emirate": "Fujairah", "business_activity": "Consulting", "status": "active"},
        "TRADE3344": {"company_name": "Ashutosh Kumar Tech FZE", "trade_license_number": "TRADE3344", "owner_name": "Ashutosh Kumar", "date_of_creation": "2023-01-20", "expiry_date": "2033-01-20", "country": "UAE", "emirate": "Abu Dhabi", "business_activity": "Software", "status": "active"},
    },
    "PASSPORT": {
        "A1234567": {"name": "Alejandra Prenatt", "id_type": "PASSPORT", "id_number": "A1234567", "dob": "1991-07-04", "nationality": "British", "country": "UK", "issue_date": "2019-07-04", "expiry_date": "2029-07-04", "gender": "Female", "status": "active"},
        "B9876543": {"name": "Alyssa Biasotti", "id_type": "PASSPORT", "id_number": "B9876543", "dob": "1997-11-19", "nationality": "British", "country": "UK", "issue_date": "2020-11-19", "expiry_date": "2030-11-19", "gender": "Female", "status": "active"},
        "C9988776": {"name": "Antony Alldis", "id_type": "PASSPORT", "id_number": "C9988776", "dob": "1981-06-20", "nationality": "British", "country": "UK", "issue_date": "2018-06-20", "expiry_date": "2028-06-20", "gender": "Male", "status": "active"},
        "D3344556": {"name": "Asset Manager", "id_type": "PASSPORT", "id_number": "D3344556", "dob": "1980-01-01", "nationality": "British", "country": "UK", "issue_date": "2021-01-01", "expiry_date": "2031-01-01", "gender": "Male", "status": "active"},
    },
    "DRIVING_LICENSE": {
        "DL12345AB": {"name": "Alejandra Prenatt", "id_type": "DRIVING_LICENSE", "id_number": "DL12345AB", "dob": "1991-07-04", "country": "UK", "issue_date": "2015-07-04", "expiry_date": "2025-07-04", "license_category": "B", "address": "10 Oxford Street, London W1D 1BS", "status": "active"},
        "DL67890CD": {"name": "Alyssa Biasotti", "id_type": "DRIVING_LICENSE", "id_number": "DL67890CD", "dob": "1997-11-19", "country": "UK", "issue_date": "2019-11-19", "expiry_date": "2029-11-19", "license_category": "B", "address": "25 Baker Street, London W1U 6PL", "status": "active"},
        "DL99887EF": {"name": "Antony Alldis", "id_type": "DRIVING_LICENSE", "id_number": "DL99887EF", "dob": "1981-06-20", "country": "UK", "issue_date": "2018-06-20", "expiry_date": "2028-06-20", "license_category": "B+E", "address": "5 Royal Mile, Edinburgh EH1 1ST", "status": "active"},
        "DL55443GH": {"name": "Asset Manager", "id_type": "DRIVING_LICENSE", "id_number": "DL55443GH", "dob": "1980-01-01", "country": "UK", "issue_date": "2016-01-01", "expiry_date": "2026-01-01", "license_category": "B", "address": "18 Piccadilly, London W1J 9LL", "status": "active"},
    },
    "SSN": {
        "123-45-6789": {"name": "Alfonso Griglen", "id_type": "SSN", "id_number": "123-45-6789", "dob": "1987-03-17", "country": "USA", "state_issued": "California", "status": "active"},
        "987-65-4321": {"name": "Amelia Caputo", "id_type": "SSN", "id_number": "987-65-4321", "dob": "1992-07-15", "country": "USA", "state_issued": "New York", "status": "active"},
        "111-22-3333": {"name": "Aqib Mushtaq", "id_type": "SSN", "id_number": "111-22-3333", "dob": "1993-06-18", "country": "USA", "state_issued": "Texas", "status": "active"},
        "222-33-4444": {"name": "ATF User", "id_type": "SSN", "id_number": "222-33-4444", "dob": "1985-04-01", "country": "USA", "state_issued": "Florida", "status": "active"},
    },
    "EIN": {
        "12-3456789": {"company_name": "Alissa Mountjoy Media", "ein_number": "12-3456789", "owner_name": "Alissa Mountjoy", "date_of_creation": "2016-02-14", "country": "USA", "state": "New York", "business_type": "LLC", "industry": "Media", "status": "active"},
        "98-7654321": {"company_name": "Allan Schwantd Finance", "ein_number": "98-7654321", "owner_name": "Allan Schwantd", "date_of_creation": "2010-09-09", "country": "USA", "state": "Illinois", "business_type": "S-Corp", "industry": "Finance", "status": "active"},
        "23-4567890": {"company_name": "Armando Kolm Construction", "ein_number": "23-4567890", "owner_name": "Armando Kolm", "date_of_creation": "2012-06-25", "country": "USA", "state": "Arizona", "business_type": "Partnership", "industry": "Construction", "status": "active"},
        "34-5678901": {"company_name": "Armando Papik Holdings", "ein_number": "34-5678901", "owner_name": "Armando Papik", "date_of_creation": "2015-08-01", "country": "USA", "state": "Nevada", "business_type": "C-Corp", "industry": "Real Estate", "status": "active"},
        "45-6789012": {"company_name": "ATF TestItilUser1 LLC", "ein_number": "45-6789012", "owner_name": "ATF_TestItilUser1", "date_of_creation": "2020-01-15", "country": "USA", "state": "Washington", "business_type": "LLC", "industry": "Testing", "status": "active"},
        "56-7890123": {"company_name": "ATF TestItilUser2 Corp", "ein_number": "56-7890123", "owner_name": "ATF_TestItilUser2", "date_of_creation": "2021-03-30", "country": "USA", "state": "Oregon", "business_type": "C-Corp", "industry": "Testing", "status": "active"},
    },
    "VAT": {
        "VAT1234567": {"company_name": "Aileen Mottern Consulting", "vat_number": "VAT1234567", "owner_name": "Aileen Mottern", "date_of_creation": "2018-06-01", "expiry_date": "2028-06-01", "country": "UAE", "emirate": "Dubai", "status": "active"},
        "VAT9988770": {"company_name": "Alejandro Mascall Group", "vat_number": "VAT9988770", "owner_name": "Alejandro Mascall", "date_of_creation": "2020-12-05", "expiry_date": "2030-12-05", "country": "UK", "status": "active"},
        "VAT8765432": {"company_name": "Andrew Jackson Trading", "vat_number": "VAT8765432", "owner_name": "Andrew Jackson", "date_of_creation": "2017-03-22", "expiry_date": "2027-03-22", "country": "UAE", "emirate": "Dubai", "status": "active"},
        "VAT4455660": {"company_name": "Andrew Och Consulting", "vat_number": "VAT4455660", "owner_name": "Andrew Och", "date_of_creation": "2019-07-10", "expiry_date": "2029-07-10", "country": "UK", "status": "active"},
        "VAT4455667": {"company_name": "Annie Approver Retail", "vat_number": "VAT4455667", "owner_name": "Annie Approver", "date_of_creation": "2021-12-10", "expiry_date": "2031-12-10", "country": "UAE", "emirate": "Sharjah", "status": "active"},
        "VAT1122330": {"company_name": "Antony Thierauf Partners", "vat_number": "VAT1122330", "owner_name": "Antony Thierauf", "date_of_creation": "2018-09-20", "expiry_date": "2028-09-20", "country": "UK", "status": "active"},
        "VAT7788990": {"company_name": "Ashley Parker Ventures", "vat_number": "VAT7788990", "owner_name": "Ashley Parker", "date_of_creation": "2022-04-18", "expiry_date": "2032-04-18", "country": "UAE", "emirate": "Fujairah", "status": "active"},
        "VAT6677880": {"company_name": "ATF Change Management Ltd", "vat_number": "VAT6677880", "owner_name": "ATF Change Management", "date_of_creation": "2020-05-01", "expiry_date": "2030-05-01", "country": "UK", "status": "active"},
    },
}


def validate_format(id_type: str, id_number: str) -> bool:
    pattern = PATTERNS.get(id_type.upper())
    if not pattern:
        return False
    return bool(re.match(pattern, id_number))


@app.get("/")
def root():
    return {"message": "ID Verification API", "version": "1.1.0", "countries": list(COUNTRY_ID_TYPES.keys()), "endpoints": {"lookup": "/lookup?id_type=AADHAAR&id_number=234567890123", "country_ids": "/country/{country}", "id_types": "/id-types", "health": "/health"}}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/id-types")
def list_id_types():
    return {"country_id_types": COUNTRY_ID_TYPES}


@app.get("/country/{country}")
def get_country_ids(country: str):
    matched = next((c for c in COUNTRY_ID_TYPES if c.lower() == country.lower()), None)
    if not matched:
        raise HTTPException(status_code=404, detail=f"Country '{country}' not found. Available: {list(COUNTRY_ID_TYPES.keys())}")
    return {"country": matched, "supported_id_types": COUNTRY_ID_TYPES[matched]}


@app.get("/lookup")
def lookup(id_type: str, id_number: str):
    id_type_upper = id_type.upper()
    all_types = {t for types in COUNTRY_ID_TYPES.values() for t in types}
    if id_type_upper not in all_types:
        raise HTTPException(status_code=400, detail=f"Unknown id_type '{id_type}'. Valid types: {sorted(all_types)}")
    if not validate_format(id_type_upper, id_number):
        raise HTTPException(status_code=422, detail={"error": "Invalid format", "id_type": id_type_upper, "id_number": id_number, "expected_pattern": PATTERNS.get(id_type_upper, "unknown")})
    record = DB.get(id_type_upper, {}).get(id_number)
    if not record:
        raise HTTPException(status_code=404, detail={"error": "Record not found", "id_type": id_type_upper, "id_number": id_number})
    return {"success": True, "data": record}
