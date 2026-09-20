import os
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
        cursor.execute('''
            INSERT INTO theme_park_booking (userId, themeParkId, price, ticketCode)
            VALUES (?, ?, ?, ?)
        ''', (data.requestId, data.themeParkId, data.price, data.ticketCode))
        conn.commit()
    return None

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
            INSERT INTO theme_park (name, description, price, rating, duration, location, ageLimit, capacity, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (data.name, data.description, data.price, data.rating, data.duration, data.location, data.ageLimit, data.capacity, filePath))
        conn.commit()
        return data.name
