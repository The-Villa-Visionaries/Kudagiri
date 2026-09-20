import os
from database import ConnectDatabase
from schemas import FetchAllHotels, BookHotel, MakeHotels, FetchAllFerry, BookFerry, MakeFerry, FetchAllThemeParks, BookThemeParks, MakeThemeParks, FetchAllPromos, MakePromo, FetchAllEvents, MakeEvents, CheckHotelBooking, GenerateTicket, CheckTicket

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
    return None

async def CreateHotel(data:MakeHotels):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
            return {'message': 'Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.'}
        fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
        filePath: str = os.path.join(f'{STATIC_DIRECTORY}/hotel', f'{data.name}.{fileExtension}')
        with open(filePath, 'wb') as file:
            file.write(await data.image.read())
        cursor.execute('''
            INSERT INTO hotel (name, description, price, rating, capacity, roomSize, bedType, amenities, offers, guests, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (data.name, data.description, data.price, data.rating, data.capacity, data.roomSize, data.bedType, data.amenities, data.offers, data.guests, filePath))
        conn.commit()
        return data.name

def CheckHotelBooked(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT userId 
            FROM hotel_booking 
            WHERE userId = ?''', (data.userId,))
        hotel = cursor.fetchall()
        if not hotel:
            return {'message': 'User not valid.'}
        return data.requestId

async def UpdateHotel(data:MakeHotels):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.image:
            if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
                return {'message': 'Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.'}
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
                SET name = ?, description = ?, price = ?, rating = ?, capacity = ?, roomSize = ?, bedType = ?, amenities = ?, offers = ?, guests = ?, image = ?
                WHERE name = ?''', 
                (data.name, data.description, data.price, data.rating, data.capacity, data.roomSize, data.bedType, data.amenities, data.offers, data.guests, filePath, data.name))
        else:
            cursor.execute('''
                UPDATE hotel 
                SET name = ?, description = ?, price = ?, rating = ?, capacity = ?, roomSize = ?, bedType = ?, amenities = ?, offers = ?, guests = ?
                WHERE name = ?''', 
                (data.name, data.description, data.price, data.rating, data.capacity, data.roomSize, data.bedType, data.amenities, data.offers, data.guests, data.name))
        conn.commit()
        return data.name