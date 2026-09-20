import os
from fastapi import HTTPException
from database import ConnectDatabase
from schemas import FetchAllHotels, BookHotel, MakeHotels, FetchAllFerry, BookFerry, MakeFerry, FetchAllThemeParks, BookThemeParks, MakeThemeParks, FetchAllPromos, MakePromo, FetchAllEvents, MakeEvents, CheckHotelBooking, GenerateTicket, CheckTicket, UpdateHotels

STATIC_DIRECTORY:str = 'static/'
ALLOWED_EXTENSIONS:tuple = ('.jpg', '.jpeg', '.png', '.webp')

def GetAllHotels(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * 
            FROM hotel''')
        hotel = cursor.fetchall()
        if not hotel:
            return {'message': 'No hotels found'}
        return [dict(x) for x in hotel]

def HotelBooking(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO hotel_booking (userId, hotelId, price, checkInDate, checkOutDate, numGuests, promoCode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data.requestId, data.hotelId, data.price, data.checkInDate, data.checkOutDate, data.numGuests, data.promoCode))
        conn.commit()
        cursor.execute('''
            UPDATE hotel
            SET totalBookings = totalBookings + 1
            WHERE hotelId = ?
        ''', (data.hotelId,))
        conn.commit()
    return None

async def CreateHotel(data:MakeHotels):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
            raise HTTPException(status_code=400, detail='Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.')
        fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
        filePath: str = os.path.join(f'{STATIC_DIRECTORY}/hotel', f'{data.name}.{fileExtension}')
        with open(filePath, 'wb') as file:
            file.write(await data.image.read())
        cursor.execute('''
            INSERT INTO hotel (name, description, price, capacity, roomSize, bedType, amenities, offers, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (data.name, data.description, data.price, data.capacity, data.roomSize, data.bedType, data.amenities, data.offers, filePath))
        conn.commit()
        return data.name

def CheckHotelBooked(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT hotelId 
            FROM hotel_booking 
            WHERE userId = ?''', (data.userId,))
        hotelId = cursor.fetchone()
        if not hotelId:
            return {'message': 'User not valid.'}
        cursor.execute('''
            SELECT name 
            FROM hotel 
            WHERE hotelId = ?''', (hotelId[0],))
        hotel = cursor.fetchone()
        return hotel[0]

async def UpdateHotel(data:UpdateHotels):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.image:
            if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
                raise HTTPException(status_code=400, detail='Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.')
            cursor.execute('SELECT image FROM hotel WHERE name = ?', (data.name,))
            oldImage = cursor.fetchone()
            if oldImage:
                os.remove(oldImage[0])
            fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
            filePath: str = os.path.join(f'{STATIC_DIRECTORY}/hotel', f'{data.name}.{fileExtension}')
            with open(filePath, 'wb') as file:
                file.write(await data.image.read())
            cursor.execute('''
                UPDATE hotel 
                SET name = ?, description = ?, price = ?, capacity = ?, roomSize = ?, bedType = ?, amenities = ?, offers = ?, image = ?
                WHERE name = ?''', 
                (data.name, data.description, data.price, data.capacity, data.roomSize, data.bedType, data.amenities, data.offers, filePath, data.name))
        else:
            cursor.execute('''
                UPDATE hotel 
                SET name = ?, description = ?, price = ?, capacity = ?, roomSize = ?, bedType = ?, amenities = ?, offers = ?
                WHERE name = ?''', 
                (data.name, data.description, data.price, data.capacity, data.roomSize, data.bedType, data.amenities, data.offers, data.name))
        conn.commit()
        return data.name

def DeleteHotel(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT image FROM hotel WHERE name = ?', (data.name,))
        oldImage = cursor.fetchone()
        if oldImage:
            os.remove(oldImage[0])
        cursor.execute('DELETE FROM hotel WHERE name = ?', (data.name,))
        conn.commit()
    return {'message': f'Hotel {data.name} deleted successfully'}