import os, secrets
from fastapi import HTTPException
from database import ConnectDatabase
from schemas import FetchAllHotels, BookHotel, MakeHotels, FetchAllFerry, BookFerry, MakeFerry, FetchAllThemeParks, BookThemeParks, MakeThemeParks, FetchAllPromos, MakePromo, FetchAllEvents, MakeEvents, CheckHotelBooking, GenerateTicket, CheckTicket

STATIC_DIRECTORY:str = 'static/'
ALLOWED_EXTENSIONS:tuple = ('.jpg', '.jpeg', '.png', '.webp')

'''
cursor.execute(
    CREATE TABLE IF NOT EXISTS user (
    userId INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT UNIQUE NOT NULL, 
    password TEXT NOT NULL, 
    email TEXT NOT NULL, 
    role TEXT NOT NULL, 
    balance INTEGER DEFAULT 0,
    profilePicture TEXT))
'''

def GetAllUsers(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user')
        users = cursor.fetchall()
        if not users:
            return {'message': 'No users found'}
        return [dict(x) for x in users]

def GetUserById(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE userId = ?', (data.userId,))
        user = cursor.fetchone()
        if not user:
            return {'message': 'User not found'}
        return dict(user)

async def CreateUser(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
            raise HTTPException(status_code=400, detail='Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.')
        fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
        filePath: str = os.path.join(f'{STATIC_DIRECTORY}/user', f'profile_{cursor.lastrowid}.{fileExtension}')
        with open(filePath, 'wb') as file:
            file.write(await data.image.read())
        cursor.execute('''
            INSERT INTO user (name, email, password, role, profilePicture)
            VALUES (?, ?, ?, ?, ?)''', (data.name, data.email, data.password, data.role, filePath))
        conn.commit()
        return data.name

async def UpdateUser(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        if data.image:
            if not str(data.image.filename).lower().endswith(ALLOWED_EXTENSIONS):
                raise HTTPException(status_code=400, detail='Invalid file type. Only JPG, JPEG, PNG, and WEBP files are allowed.')
            fileExtension: str = os.path.splitext(str(data.image.filename))[1].lstrip('.')
            filePath: str = os.path.join(f'{STATIC_DIRECTORY}/user', f'profile_{data.userId}.{fileExtension}')
            with open(filePath, 'wb') as file:
                file.write(await data.image.read())
            cursor.execute('''
                UPDATE user 
                SET name = ?, email = ?, password = ?, role = ?, profilePicture = ?
                WHERE userId = ?''', (data.name, data.email, data.password, data.role, filePath, data.userId))
        else:
            cursor.execute('''
                UPDATE user 
                SET name = ?, email = ?, password = ?, role = ?
                WHERE userId = ?''', (data.name, data.email, data.password, data.role, data.userId))
        conn.commit()
        return data.name

def DeleteUser(data):
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT profilePicture 
            FROM user 
            WHERE userId = ?''', (data.userId,))
        oldImage = cursor.fetchone()
        if oldImage:
            os.remove(oldImage[0])
        cursor.execute('''
            DELETE FROM user 
            WHERE userId = ?''', (data.userId,))
        conn.commit()
    return data.userId
