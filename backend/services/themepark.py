import os
import secrets
from database import ConnectDatabase
from schemas import FetchAllHotels, BookHotel, MakeHotels, FetchAllFerry, BookFerry, MakeFerry, FetchAllThemeParks, BookThemeParks, MakeThemeParks, FetchAllPromos, MakePromo, FetchAllEvents, MakeEvents, CheckHotelBooking, GenerateTicket, CheckTicket

STATIC_DIRECTORY:str = 'static/'
ALLOWED_EXTENSIONS:tuple = ('.jpg', '.jpeg', '.png', '.webp')

def GetThemePark(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM theme_park')
        themePark = cursor.fetchall()
        if not themePark:
            return {'message': 'No Theme Park found'}
        return [dict(x) for x in themePark]

def ThemeParkBooking(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        ticketCode = f'TP-{secrets.token_hex(6)}'
        cursor.execute('''
            INSERT INTO theme_park_booking (userId, themeParkId, price, ticketCode)
            VALUES (?, ?, ?, ?)
        ''', (data.requestId, data.themeParkId, data.price, ticketCode))
        conn.commit()   
    return ticketCode

async def CreateThemePark(data:MakeThemeParks):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
            return {'message': 'Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.'}
        fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
        filePath: str = os.path.join(f'{STATIC_DIRECTORY}/theme-park', f'{data.name}.{fileExtension}')
        with open(filePath, 'wb') as file:
            file.write(await data.image.read())
        cursor.execute('''
            INSERT INTO theme_park (name, description, price, duration, location, ageLimit, capacity, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (data.name, data.description, data.price, data.duration, data.location, data.ageLimit, data.capacity, filePath))
        conn.commit()
        return data.name

async def UpdateThemePark(data:MakeThemeParks):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.image:
            if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
                return {'message': 'Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.'}
            fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
            filePath: str = os.path.join(f'{STATIC_DIRECTORY}/theme-park', f'{data.name}.{fileExtension}')
            with open(filePath, 'wb') as file:
                file.write(await data.image.read())
            cursor.execute('''
                UPDATE theme_park 
                SET name = ?, description = ?, price = ?, duration = ?, location = ?, ageLimit = ?, capacity = ?, image = ?
                WHERE name = ?''', (data.name, data.description, data.price, data.duration, data.location, data.ageLimit, data.capacity, filePath, data.name))
        else:
            cursor.execute('''
                UPDATE theme_park 
                SET name = ?, description = ?, price = ?, duration = ?, location = ?, ageLimit = ?, capacity = ?
                WHERE name = ?''', (data.name, data.description, data.price, data.duration, data.location, data.ageLimit, data.capacity, data.name))
        conn.commit()
        return data.name

def DeleteThemePark(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM theme_park WHERE name = ?', (data.name,))
        conn.commit()
    return data.name
