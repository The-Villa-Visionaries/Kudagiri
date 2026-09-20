import secrets

from fastapi import HTTPException
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
        ticketCode = f'FR-{secrets.token_hex(6)}'
        cursor.execute('''
            INSERT INTO ferry_booking (requestId, ferryId)
            VALUES (?, ?)
        ''', (data.requestId, data.ferryId))
        conn.commit()
    return ticketCode

async def CreateFerry(data:MakeFerry):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
            raise HTTPException(status_code=400, detail='Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.')
        fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
        filePath: str = os.path.join(f'{STATIC_DIRECTORY}/ferry', f'{data.name}.{fileExtension}')
        with open(filePath, 'wb') as file:
            file.write(await data.image.read())
        cursor.execute('''
            INSERT INTO ferry (name, description, price, duration, image)
            VALUES (?, ?, ?, ?, ?)''', (data.name, data.description, data.price, data.duration, filePath))
        conn.commit()
        return data.name

async def UpdateFerry(data:MakeFerry):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.image:
            if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
                raise HTTPException(status_code=400, detail='Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.')
            fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
            filePath: str = os.path.join(f'{STATIC_DIRECTORY}/ferry', f'{data.name}.{fileExtension}')
            with open(filePath, 'wb') as file:
                file.write(await data.image.read())
            cursor.execute('''
                UPDATE ferry 
                SET name = ?, description = ?, price = ?, duration = ?, image = ?
                WHERE name = ?''', (data.name, data.description, data.price, data.duration, filePath, data.name))
        else:
            cursor.execute('''
                UPDATE ferry 
                SET name = ?, description = ?, price = ?, duration = ?
                WHERE name = ?''', (data.name, data.description, data.price, data.duration, data.name))
        conn.commit()
        return data.name

def DeleteFerry(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT image FROM ferry WHERE name = ?', (data.name,))
        oldImage = cursor.fetchone()
        if oldImage:
            os.remove(oldImage[0])
        cursor.execute('DELETE FROM ferry WHERE name = ?', (data.name,))
        conn.commit()
    return data.name