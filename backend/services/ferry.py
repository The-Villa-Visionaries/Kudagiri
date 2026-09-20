import os
from database import ConnectDatabase
from schemas import FetchAllHotels, BookHotel, MakeHotels, FetchAllFerry, BookFerry, MakeFerry, FetchAllThemeParks, BookThemeParks, MakeThemeParks, FetchAllPromos, MakePromo, FetchAllEvents, MakeEvents, CheckHotelBooking, GenerateTicket, CheckTicket

STATIC_DIRECTORY:str = 'static/'
ALLOWED_EXTENSIONS:tuple = ('.jpg', '.jpeg', '.png', '.webp')

def GetAllFerry(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * 
            FROM ferry''')
        ferry = cursor.fetchall()
        if not ferry:
            return {'message': 'No ferry found'}
        return [dict(x) for x in ferry]

def FerryBooking(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ferry_booking (requestId, ferryId)
            VALUES (?, ?)
        ''', (data.requestId, data.ferryId))
        conn.commit()
    return None

async def CreateFerry(data:MakeFerry):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
            return {'message': 'Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.'}
        fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
        filePath: str = os.path.join(f'{STATIC_DIRECTORY}/ferry', f'{data.name}.{fileExtension}')
        with open(filePath, 'wb') as file:
            file.write(await data.image.read())
        cursor.execute('''
            INSERT INTO ferry (name, description, price, rating, duration, image)
            VALUES (?, ?, ?, ?, ?, ?)''', (data.name, data.description, data.price, data.rating, data.duration, filePath))
        conn.commit()
        return data.name
