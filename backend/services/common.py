import os, secrets
from fastapi import HTTPException
from database import ConnectDatabase
from schemas import FetchAllHotels, BookHotel, MakeHotels, FetchAllFerry, BookFerry, MakeFerry, FetchAllThemeParks, BookThemeParks, MakeThemeParks, FetchAllPromos, MakePromo, FetchAllEvents, MakeEvents, CheckHotelBooking, GenerateTicket, CheckTicket, UpdateEvents

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

def UpdatePromotion(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE promotion 
            SET name = ?, description = ?, offer = ?, promoCode = ?, fromDate = ?, toDate = ?
            WHERE name = ?''', (data.name, data.description, data.offer, data.promoCode, data.fromDate, data.toDate, data.name))
        conn.commit()
        return data.name

def DeletePromotion(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM promotion WHERE name = ?', (data.name,))
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
            raise HTTPException(status_code=400, detail='Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.')
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

async def UpdateEvent(data:UpdateEvents):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.image:
            if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
                raise HTTPException(status_code=400, detail='Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.')
            fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
            filePath: str = os.path.join(f'{STATIC_DIRECTORY}/event', f'{data.name}.{fileExtension}')
            with open(filePath, 'wb') as file:
                file.write(await data.image.read())
            cursor.execute('''
                UPDATE event 
                SET name = ?, description = ?, buttonText = ?, tag = ?, image = ?
                WHERE name = ?''', (data.name, data.description, data.buttonText, data.tag, filePath, data.name))
        else:
            cursor.execute('''
                UPDATE event 
                SET name = ?, description = ?, buttonText = ?, tag = ?
                WHERE name = ?''', (data.name, data.description, data.buttonText, data.tag, data.name))
        conn.commit()
    return data.name

def DeleteEvent(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM event WHERE name = ?', (data.name,))
        conn.commit()
    return data.name

# Ticket Functions
def CreateTicket(data):
    with ConnectDatabase() as conn:
        ticketCode = ''
        cursor = conn.cursor()
        if data.type == 'ThemePark':
            ticketCode = f'TP-{secrets.token_hex(6)}'
            cursor.execute('''
                INSERT INTO theme_park_booking (userId, themeParkId, price, ticketCode)
                VALUES (?, ?, ?, ?)
            ''', (000, data.typeId, data.price, ticketCode))
        elif data.type == 'Ferry':
            ticketCode = f'FR-{secrets.token_hex(6)}'
            cursor.execute('''
                INSERT INTO ferry_booking (userId, ferryId, price, ticketCode)
                VALUES (?, ?, ?, ?)
            ''', (000, data.typeId, data.price, ticketCode))
        conn.commit()
    return ticketCode

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
        userId = cursor.fetchone()
        if not userId:
            raise HTTPException(status_code=400, detail='Invalid ticket code.')
        return userId['userId']

def UseTicket(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.type == 'ThemePark':
            cursor.execute('''
                DELETE FROM theme_park_booking
                WHERE ticketCode = ?
            ''', (data.ticketCode,))
        elif data.type == 'Ferry':
            cursor.execute('''
                DELETE FROM ferry_booking
                WHERE ticketCode = ?
            ''', (data.ticketCode,))
        conn.commit()
    return {'message': 'Ticket used successfully'}

def GiveReview(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.type == 'Hotel':
            cursor.execute('''
                UPDATE hotel
                SET rating = CAST((reviewCount + 1) AS FLOAT) / NULLIF(totalBookings, 0) * 100,
                    reviewCount = reviewCount + 1
                WHERE hotelId = ?
            ''', (data.typeId,))
        elif data.type == 'ThemePark':
            cursor.execute('''
                UPDATE theme_park
                SET rating = CAST((reviewCount + 1) AS FLOAT) / NULLIF(totalBookings, 0) * 100,
                    reviewCount = reviewCount + 1
                WHERE themeParkId = ?
            ''', (data.typeId,))
        elif data.type == 'Ferry':
            cursor.execute('''
                UPDATE ferry
                SET rating = CAST((reviewCount + 1) AS FLOAT) / NULLIF(totalBookings, 0) * 100,
                    reviewCount = reviewCount + 1
                WHERE ferryId = ?
            ''', (data.typeId,))
        conn.commit()
    return {'message': 'Review submitted successfully'}