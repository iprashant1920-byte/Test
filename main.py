import os
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="ITSM Identity Verification API",
    version="3.0.0",
    description="Highly optimized identity verification API built for Render deployment."
)

# Enable CORS for all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# O(1) Pre-indexed In-Memory Database
# Contains ALL records from the provided dataset
# ==========================================
DB = {
    "AADHAAR": {
        "369874512458": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "478512369874": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "589632147852": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "698745123698": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "712369845123": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "845123698745": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "956874123698": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "874512369874": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "923847561204": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "784512369870": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "812345679845": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "934567812345": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "923456781234": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "834567891245": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "745612389654": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "698745612389": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "812369874512": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "923698745123": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "734561289745": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "845612397845": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "956123874569": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "867451239876": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "978451236789": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "789654123789": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "812345678901": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "923456789012": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "734567890123": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "845678901234": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "956789012345": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "867890123456": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "978901234567": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "789012345678": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "890123456789": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "901234567890": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "812345678912": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "923456789123": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "734567891234": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "845678912345": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "956789123456": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "867891234567": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "978912345678": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "789123456789": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "890234567890": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "901345678901": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "812456789012": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "923567890123": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "734678901234": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "PAN": {
        "ABCDE1234F": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "LKJHG4321P": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "QWERT6789L": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "ASDFG2345H": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "ZXCVB8765K": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "POIUY5432R": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "AKJAI1234M": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "MXPRN5678N": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "MNBVC5432X": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "POIUY9876T": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "CANGR1234A": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "USMNT6789B": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "ALLAN1234Z": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "GILLI5678Y": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "PENNI6789X": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "BIASO7890W": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "CAPUT1234V": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "LINNA2345U": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "JACKS3456T": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "OCHAA4567S": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "SCHER5678R": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "FEREN6789Q": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "COGER7890P": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "FRIET8901O": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "ANNIE9012N": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "MCCLE0123M": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "ALLDI1234L": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "THIER2345K": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "APUSR3456J": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "MUSHT4567I": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "KOLMA5678H": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "PAPIK6789G": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "UBHIA7890F": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "HAJAR8901E": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "STARK9012D": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "LEONE0123C": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "PARKE1234B": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "KUMAR2345A": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "ASMAN3456Z": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "ATFCM4567Y": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "ATFSM5678X": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "ATFUS6789W": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "TESTI7890V": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "TESTU8901U": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "CANTU9012T": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "FONTA0123S": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "AUDRA1234R": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "PASSPORT": {
        "K7P9L2Q1": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "ZX91PQ78": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "UK778899": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "SP998877": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "DE112233": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "AU556677": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "IN889900": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "MX112299": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "F9988776": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "G8877665": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "CA778899": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "US445566": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "UK556677": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "US667788": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "CA889900": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "IT112233": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "ES223344": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "US334455": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "UK556688": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "DE667799": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "IT778811": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "US889922": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "ES990033": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "IN101144": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "US112255": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "UK223366": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "DE334477": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "IN445588": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "IN556699": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "US667700": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "MX778811": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "UK889922": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "IN990033": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "UK101144": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "US223366": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        },
        "IN334477": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "US556699": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "IN778811": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "IN889922": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "US101144": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "EMIRATES_ID": {
        "784-1995-1234567-1": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "784-1988-7654321-2": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "784-1992-3344556-3": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "784-1990-1122334-4": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "784-1993-9988776-5": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "784-1994-5566778-6": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "784-1998-2233445-7": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "784-1991-6677889-8": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "784-1996-7812345-2": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "784-2000-3344556-3": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "784-1997-3344556-9": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "784-1992-7788990-1": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "784-1991-2345678-2": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "784-1993-3456789-3": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "784-1994-4567890-4": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "784-1995-5678901-5": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "784-1996-6789012-6": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "784-1997-7890123-7": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "784-1998-8901234-8": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "784-1999-9012345-9": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "784-1990-1123456-1": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "784-1991-2234567-2": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "784-1992-3345678-3": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "784-1993-4456789-4": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "784-1994-5567890-5": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "784-1995-6678901-6": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "784-1996-7789012-7": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "784-1997-8890123-8": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "784-1998-9901234-9": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "784-1999-1012345-1": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "784-1990-2123456-2": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "784-1991-3234567-3": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "784-1992-4345678-4": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "784-1993-5456789-5": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "784-1994-6567890-6": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "784-1995-7678901-7": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "784-1996-8789012-8": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "784-1997-9890123-9": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "784-1998-1012346-1": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "784-1999-2123457-2": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "784-1990-3234568-3": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "784-1991-4345679-4": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "784-1992-5456780-5": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "784-1993-6567891-6": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "784-1994-7678902-7": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "784-1995-8789013-8": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "784-1996-9890124-9": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "DRIVING_LICENSE": {
        "DL0612341234567": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "CA9912345678901": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "UK2212345678901": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "SP0112345678901": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "DE5512345678901": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "AU9912345678901": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "DL0212345678901": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "MX3312345678901": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "DL0612345678901": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "DL0512345678901": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "CA9912345678902": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "US4412345678903": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "UK3312345678901": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "US5512345678902": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "CA6612345678903": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "IT7712345678904": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "ES8812345678905": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "US9912345678906": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "US1012345678907": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "UK1112345678908": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "DE1212345678909": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "IT1312345678910": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "US1412345678911": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "ES1512345678912": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "DL1612345678913": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "US1712345678914": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "UK1812345678915": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "DE1912345678916": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "DL2012345678917": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "DL2112345678918": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "US2212345678919": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "MX2312345678920": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "UK2412345678921": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "DL2512345678922": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "UK2612345678923": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "US2712345678924": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "US2812345678925": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "DL2912345678926": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "DL3012345678927": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "US3112345678928": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "US3212345678929": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "DL3312345678930": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "DL3412345678931": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "DL3512345678932": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "US3612345678933": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "US3712345678934": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "US3812345678935": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "SSN": {
        "521-45-9876": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "234-56-7891": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "345-67-8912": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "456-78-9123": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "567-89-1234": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "678-91-2345": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "789-12-3456": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "891-23-4567": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "391-82-5567": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "628-44-1937": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "712-34-5678": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "823-45-6789": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "912-34-5678": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "923-45-6789": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "934-56-7890": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "945-67-8901": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "956-78-9012": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "967-89-0123": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "978-90-1234": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "989-01-2345": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "123-45-6780": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "134-56-7891": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "145-67-8902": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "156-78-9013": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "167-89-0124": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "178-90-1235": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "189-01-2346": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "190-12-3457": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "201-23-4568": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "212-34-5679": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "223-45-6780": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "245-67-8902": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "256-78-9013": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "267-89-0124": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "278-90-1235": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "289-01-2346": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "290-12-3457": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "301-23-4568": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "312-34-5679": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "323-45-6780": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "334-56-7891": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "345-67-8902": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "356-78-9013": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "367-89-0124": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "378-90-1235": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "389-01-2346": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "GST": {
        "07ABCDE1234F1Z5": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "22LKJHG4321P1Z3": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "11QWERT6789L1Z9": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "33ASDFG2345H1Z2": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "44ZXCVB8765K1Z7": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "55POIUY5432R1Z8": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "09AKJAI1234M1Z2": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "66MXPRN5678N1Z4": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "66MNBVC5432X1Z4": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "55POIUY9876T1Z3": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "77CANGR1234A1Z6": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "88USMNT6789B1Z1": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "12ALLAN1234Z1Z1": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "13GILLI5678Y1Z2": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "14PENNI6789X1Z3": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "15BIASO7890W1Z4": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "16CAPUT1234V1Z5": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "17LINNA2345U1Z6": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "18JACKS3456T1Z7": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "19OCHAA4567S1Z8": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "20SCHER5678R1Z9": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "21FEREN6789Q1Z1": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "22COGER7890P1Z2": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "23FRIET8901O1Z3": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "24ANNIE9012N1Z4": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "25MCCLE0123M1Z5": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "26ALLDI1234L1Z6": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "27THIER2345K1Z7": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "28APUSR3456J1Z8": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "29MUSHT4567I1Z9": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "30KOLMA5678H1Z1": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "31PAPIK6789G1Z2": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "32UBHIA7890F1Z3": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "33HAJAR8901E1Z4": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "34STARK9012D1Z5": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "35LEONE0123C1Z6": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "36PARKE1234B1Z7": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "37KUMAR2345A1Z8": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "38ASMAN3456Z1Z9": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "39ATFCM4567Y1Z1": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "40ATFSM5678X1Z2": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "41ATFUS6789W1Z3": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "42TESTI7890V1Z4": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "43TESTU8901U1Z5": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "44CANTU9012T1Z6": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "45FONTA0123S1Z7": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "46AUDRA1234R1Z8": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "VAT": {
        "IN9988776655": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "US5566778899": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "GB4455667788": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "ES1122334455": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "DE6677889900": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "AU9988776655": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "IN1122446688": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "MX3344556677": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "GB7788990011": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "US2233445566": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "CA1122334455": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "US7788990011": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        },
        "GB1122334455": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "US3344556677": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "CA5566778899": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "IT6677889900": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "ES7788990011": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "US8899001122": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "US9900112233": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "GB0011223344": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "DE1122334455": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "IT2233445566": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "ES4455667788": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "IN5566778899": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "US6677889900": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "DE8899001122": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "IN9900112233": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "IN0011223344": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "US1122334455": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "MX2233445566": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "GB3344556677": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "IN4455667788": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "GB5566778899": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "IN8899001122": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "US0011223344": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "IN2233445566": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "IN3344556677": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        }
    },
    "TRADE_LICENSE": {
        "TL-IND-778899": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "TL-USA-112233": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "TL-UK-445566": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "TL-ES-778899": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "TL-DE-223344": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "TL-AU-556677": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "TL-IN-998877": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "TL-MX-334455": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "TL-88990011": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "TL-11223344": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "TL-CA-778899": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "TL-US-990011": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "TL-UK-998877": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "TL-US-223344": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "TL-CA-334455": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "TL-IT-445566": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "TL-ES-556677": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "TL-US-667788": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "TL-US-778899": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "TL-UK-889900": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "TL-DE-990011": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "TL-IT-101112": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "TL-US-121314": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "TL-ES-141516": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "TL-IN-161718": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "TL-US-181920": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "TL-UK-202122": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "TL-DE-222324": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "TL-IN-242526": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "TL-IN-262728": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "TL-US-282930": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "TL-MX-303132": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "TL-UK-323334": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "TL-IN-343536": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "TL-UK-363738": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "TL-US-383940": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "TL-US-404142": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "TL-IN-424344": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "TL-IN-444546": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "TL-US-464748": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "TL-US-484950": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "TL-IN-505152": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "TL-IN-525354": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "TL-IN-545556": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "TL-US-565758": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "TL-US-585960": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "TL-US-606162": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "BUSINESS_REG": {
        "BR99887766": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "BR22334455": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "BR33445566": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "BR44556677": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "BR55667788": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "BR66778899": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "BR77889900": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "BR88990011": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "BR11223344": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "BR99001122": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "BR00112233": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "BR22334411": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "BR33445522": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "BR44556633": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "BR55667744": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "BR66778855": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "BR77889966": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "BR88990077": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "BR99001188": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "BR10111213": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "BR12131415": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "BR14151617": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "BR16171819": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "BR18192021": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "BR20212223": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "BR22232425": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "BR24252627": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "BR26272829": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "BR28293031": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "BR30313233": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "BR32333435": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "BR34353637": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "BR36373839": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "BR38394041": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "BR40414243": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "BR42434445": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "BR44454647": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "BR46474849": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "BR48495051": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "BR50515253": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "BR52535455": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "BR54555657": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "BR56575859": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "BR58596061": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "BR60616263": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "BR62636465": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "EIN": {
        "12-3456789": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "23-4567891": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "34-5678912": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "45-6789123": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "56-7891234": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "67-8912345": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "78-9123456": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "89-1234567": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "11-2233445": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "22-3344556": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "90-1234567": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "91-2345678": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "11-3344556": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "12-4455667": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "13-5566778": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "14-6677889": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "15-7788990": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "16-8899001": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "17-9900112": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "18-0011223": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "19-1122334": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "20-2233445": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "21-3344556": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "22-4455667": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "23-5566778": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "24-6677889": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "25-7788990": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "26-8899001": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "27-9900112": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "28-0011223": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "29-1122334": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "30-2233445": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "31-3344556": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "32-4455667": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "33-5566778": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "34-6677889": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "35-7788990": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "36-8899001": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "37-9900112": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "38-0011223": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "39-1122334": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "40-2233445": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "41-3344556": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "42-4455667": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "43-5566778": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "44-6677889": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "45-7788990": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    },
    "INCORPORATION": {
        "U12345DL2022PTC123456": {
            "name": "Abel Tuter",
            "country": "India",
            "status": "active"
        },
        "U54321NY2021PTC654321": {
            "name": "Abraham Lincoln",
            "country": "USA",
            "status": "active"
        },
        "U67890LN2020PTC789012": {
            "name": "Ace Ford",
            "country": "UK",
            "status": "active"
        },
        "U11223MD2019PTC112233": {
            "name": "Adela Cervantsz",
            "country": "Spain",
            "status": "active"
        },
        "U99887BR2018PTC998877": {
            "name": "Adriana Wolfe",
            "country": "Germany",
            "status": "active"
        },
        "U33445SY2017PTC334455": {
            "name": "Aileen Mottern",
            "country": "Australia",
            "status": "active"
        },
        "U55667DL2023PTC556677": {
            "name": "Akshat Jain",
            "country": "India",
            "status": "active"
        },
        "U77889MX2022PTC778899": {
            "name": "Alejandra Prenatt",
            "country": "Mexico",
            "status": "active"
        },
        "U45784DL2023PTC457896": {
            "name": "Alejandro Mascall",
            "country": "UK",
            "status": "active"
        },
        "U45784DL2023PTC985674": {
            "name": "Alene Rabeck",
            "country": "USA",
            "status": "active"
        },
        "U99001CA2020PTC990011": {
            "name": "Alfonso Griglen",
            "country": "Canada",
            "status": "active"
        },
        "U11223US2021PTC112244": {
            "name": "Alissa Mountjoy",
            "country": "USA",
            "status": "active"
        },
        "U22334LN2022PTC223344": {
            "name": "Allan Schwantd",
            "country": "UK",
            "status": "active"
        },
        "U33445US2023PTC334455": {
            "name": "Allyson Gillispie",
            "country": "USA",
            "status": "active"
        },
        "U44556CA2021PTC445566": {
            "name": "Alva Pennigton",
            "country": "Canada",
            "status": "active"
        },
        "U55667IT2020PTC556677": {
            "name": "Alyssa Biasotti",
            "country": "Italy",
            "status": "active"
        },
        "U66778MD2019PTC667788": {
            "name": "Amelia Caputo",
            "country": "Spain",
            "status": "active"
        },
        "U77889US2022PTC778899": {
            "name": "Amos Linnan",
            "country": "USA",
            "status": "active"
        },
        "U88990US2023PTC889900": {
            "name": "Andrew Jackson",
            "country": "USA",
            "status": "active"
        },
        "U99001LN2021PTC990011": {
            "name": "Andrew Och",
            "country": "UK",
            "status": "active"
        },
        "U10111BR2020PTC101112": {
            "name": "Angelique Schermerhorn",
            "country": "Germany",
            "status": "active"
        },
        "U12131IT2022PTC121314": {
            "name": "Angelo Ferentz",
            "country": "Italy",
            "status": "active"
        },
        "U14151US2021PTC141516": {
            "name": "Annabelle Coger",
            "country": "USA",
            "status": "active"
        },
        "U16171MD2020PTC161718": {
            "name": "Annette Frietas",
            "country": "Spain",
            "status": "active"
        },
        "U18191DL2023PTC181920": {
            "name": "Annie Approver",
            "country": "India",
            "status": "active"
        },
        "U20212US2022PTC202122": {
            "name": "Antione Mccleary",
            "country": "USA",
            "status": "active"
        },
        "U22232LN2021PTC222324": {
            "name": "Antony Alldis",
            "country": "UK",
            "status": "active"
        },
        "U24252BR2020PTC242526": {
            "name": "Antony Thierauf",
            "country": "Germany",
            "status": "active"
        },
        "U26272DL2023PTC262728": {
            "name": "Approver User",
            "country": "India",
            "status": "active"
        },
        "U28292DL2022PTC282930": {
            "name": "Aqib Mushtaq",
            "country": "India",
            "status": "active"
        },
        "U30313US2021PTC303132": {
            "name": "Armando Kolm",
            "country": "USA",
            "status": "active"
        },
        "U32333MX2020PTC323334": {
            "name": "Armando Papik",
            "country": "Mexico",
            "status": "active"
        },
        "U34353LN2022PTC343536": {
            "name": "Arron Ubhi",
            "country": "UK",
            "status": "active"
        },
        "U36373DL2023PTC363738": {
            "name": "Arya Hajarha",
            "country": "India",
            "status": "active"
        },
        "U38393LN2021PTC383940": {
            "name": "Arya Stark",
            "country": "UK",
            "status": "active"
        },
        "U40414US2022PTC404142": {
            "name": "Ashley Leonesio",
            "country": "USA",
            "status": "active"
        },
        "U42434US2023PTC424344": {
            "name": "Ashley Parker",
            "country": "USA",
            "status": "active"
        },
        "U44454DL2023PTC444546": {
            "name": "Ashutosh Kumar",
            "country": "India",
            "status": "active"
        },
        "U46474DL2022PTC464748": {
            "name": "Asset Manager",
            "country": "India",
            "status": "active"
        },
        "U48494US2021PTC484950": {
            "name": "ATF Change Management",
            "country": "USA",
            "status": "active"
        },
        "U50515US2020PTC505152": {
            "name": "ATF Service Level Mgmt",
            "country": "USA",
            "status": "active"
        },
        "U52535DL2023PTC525354": {
            "name": "ATF User",
            "country": "India",
            "status": "active"
        },
        "U54555DL2022PTC545556": {
            "name": "ATF_TestItilUser1",
            "country": "India",
            "status": "active"
        },
        "U56575DL2021PTC565758": {
            "name": "ATF_TestItilUser2",
            "country": "India",
            "status": "active"
        },
        "U58595US2022PTC585960": {
            "name": "Athena Cantu",
            "country": "USA",
            "status": "active"
        },
        "U60616US2023PTC606162": {
            "name": "Athena Fontanilla",
            "country": "USA",
            "status": "active"
        },
        "U62636US2021PTC626364": {
            "name": "Audra Cantu",
            "country": "USA",
            "status": "active"
        }
    }
}

# Pydantic schema for response structure
class VerifyResponse(BaseModel):
    success: bool
    id_type: str
    id_number: str
    data: dict

@app.get("/", tags=["General"])
def root():
    return {
        "status": "API is running successfully",
        "supported_document_types": sorted(list(DB.keys())),
        "example_usage": "/verify/PAN/ABCDE1234F"
    }

@app.get("/health", tags=["General"])
def health_check():
    total_records = sum(len(records) for records in DB.values())
    return {"status": "healthy", "total_indexed_records": total_records}

@app.get("/verify/{id_type}/{id_number}", response_model=VerifyResponse, tags=["Verification"])
def verify_document(
    id_type: str = Path(..., description="Type of the document (e.g., PAN, AADHAAR, PASSPORT)"),
    id_number: str = Path(..., description="The document number to verify")
):
    """
    Verify a document by its type and number.
    """
    id_type_clean = id_type.strip().upper()
    id_num_clean = id_number.strip()

    # 1. Validate ID Type
    if id_type_clean not in DB:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported document type: '{id_type_clean}'. Supported types: {', '.join(DB.keys())}"
        )
        
    # 2. Perform O(1) Database Lookup
    record = DB[id_type_clean].get(id_num_clean)
    
    # 3. Handle Not Found
    if not record:
        raise HTTPException(
            status_code=404, 
            detail="Document record not found in the database."
        )
        
    # 4. Return Success Data
    return {
        "success": True,
        "id_type": id_type_clean,
        "id_number": id_num_clean,
        "data": record
    }

if __name__ == "__main__":
    # Render assigns the port dynamically via the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
