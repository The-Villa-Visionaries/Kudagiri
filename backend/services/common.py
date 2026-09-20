import os
from database import ConnectDatabase
from schemas import FetchAllHotels, BookHotel, MakeHotels, FetchAllFerry, BookFerry, MakeFerry, FetchAllThemeParks, BookThemeParks, MakeThemeParks, FetchAllPromos, MakePromo, FetchAllEvents, MakeEvents, CheckHotelBooking, GenerateTicket, CheckTicket

STATIC_DIRECTORY:str = 'static/'
ALLOWED_EXTENSIONS:tuple = ('.jpg', '.jpeg', '.png', '.webp')

def GetAllPromotions(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM promotion')
        promotions = cursor.fetchall()
        if not promotions:
            return {'message': 'No promotions found'}
        return [dict(x) for x in promotions]

def CreatePromotion(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO promotion (name, description, offer, promoCode, fromDate, toDate)
            VALUES (?, ?, ?, ?, ?, ?)''', (data.name, data.description, data.offer, data.promoCode, data.fromDate, data.toDate))
        conn.commit()
        return data.name

# Event Functions
def GetAllEvents(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM event')
        events = cursor.fetchall()
        if not events:
            return {'message': 'No events found'}
        return [dict(event) for event in events]

async def CreateEvent(data:MakeEvents):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
            return {'message': 'Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.'}
        fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
        filePath: str = os.path.join(f'{STATIC_DIRECTORY}/event', f'{data.name}.{fileExtension}')
        with open(filePath, 'wb') as file:
            file.write(await data.image.read())
        cursor.execute('''
            INSERT INTO event (name, description, buttonText, tag, image)
            VALUES (?, ?, ?, ?, ?)
        ''', (data.name, data.description, data.buttonText, data.tag, filePath))
        conn.commit()
    return data.name

# Ticket Functions
def CreateTicket(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.type == 'ThemePark':
            cursor.execute('''
                INSERT INTO theme_park_booking (userId, themeParkId, price, ticketCode)
                VALUES (?, ?, ?, ?)
            ''', (000, data.typeId, data.price, data.ticketCode))
        elif data.type == 'Ferry':
            cursor.execute('''
                INSERT INTO ferry_booking (userId, ferryId, price, ticketCode)
                VALUES (?, ?, ?, ?)
            ''', (000, data.typeId, data.price, data.ticketCode))
        conn.commit()
    return data.ticketCode

def ValidateTicket(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.type == 'ThemePark':
            cursor.execute('''
                SELECT userId 
                FROM theme_park_booking
                WHERE ticketCode = ?
            ''', (data.ticketCode,))
        elif data.type == 'Ferry':
            cursor.execute('''
                SELECT userId 
                FROM ferry_booking
                WHERE ticketCode = ?
            ''', (data.ticketCode,))
        tickets = cursor.fetchall()
        if not tickets:
            return {'isValid': False}
        return {'isValid': True}
