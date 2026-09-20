import sqlite3
import os
import random
from PIL import Image, ImageDraw

DATABASE: str = 'database.db'
REQUIRED_DIRECTORIES: list = [
    'static',
    'static/hotel',
    'static/ferry',
    'static/theme-park',
    'static/event'
]

def ConnectDatabase():
    """
    Tables Schema Overview
    
    user: userId, username, password, email, role, balance, profilePicture
    sessions: primarySid, altSid, uid, expireTime
    hotel: hotelId, name, description, price, rating, capacity, roomSize, bedType, amenities, offers, image
    hotel_booking: bookingId, userId, hotelId, price, checkInDate, checkOutDate, ticketCode, promoCode, numGuests
    ferry: ferryId, name, description, price, duration, rating, image
    ferry_booking: bookingId, userId, ferryId, price, ticketCode
    theme_park: themeParkId, name, description, price, duration, location, ageLimit, capacity, rating, image
    theme_park_booking: bookingId, userId, themeParkId, price, ticketCode
    promotion: promoId, name, description, offer, promoCode, fromDate, toDate
    event: eventId, name, description, buttonText, tag, image
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def CreateDirectory():
    """Ensures all static image directories exist."""
    for folder in REQUIRED_DIRECTORIES:
        if not os.path.exists(folder):
            os.makedirs(folder)

def GenerateRandomImage(filepath: str, width: int = 100, height: int = 100):
    """
    Generates a 100x100 RGB image with a random background color 
    and saves it to the specified filepath if it doesn't already exist.
    """
    if not os.path.exists(filepath):
        # Generate a random RGB color tuple
        random_color = (
            random.randint(40, 220),
            random.randint(40, 220),
            random.randint(40, 220)
        )
        img = Image.new('RGB', (width, height), color=random_color)
        img.save(filepath, format='JPEG')

def InitializeDatabase():
    CreateDirectory()
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        
        # Create Tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
            userId INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE NOT NULL, 
            password TEXT NOT NULL, 
            email TEXT NOT NULL, 
            role TEXT NOT NULL, 
            balance INTEGER DEFAULT 0,
            profilePicture TEXT)''')
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
            primarySid TEXT PRIMARY KEY, 
            altSid TEXT, 
            uid INTEGER UNIQUE, 
            expireTime FLOAT)''')
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hotel (
            hotelId INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT UNIQUE NOT NULL, 
            description TEXT NOT NULL, 
            price FLOAT NOT NULL,
            rating FLOAT DEFAULT 0,
            capacity INTEGER DEFAULT 0,
            roomSize TEXT NOT NULL,
            bedType TEXT NOT NULL,
            amenities TEXT NOT NULL,
            offers TEXT NOT NULL,
            image TEXT NOT NULL)''')
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hotel_booking (
            bookingId INTEGER PRIMARY KEY AUTOINCREMENT, 
            userId INTEGER NOT NULL, 
            hotelId INTEGER NOT NULL, 
            price FLOAT NOT NULL,
            checkInDate TEXT NOT NULL, 
            checkOutDate TEXT NOT NULL,
            ticketCode TEXT,
            promoCode TEXT,
            numGuests INTEGER NOT NULL,
            FOREIGN KEY (userId) REFERENCES user(userId),
            FOREIGN KEY (hotelId) REFERENCES hotel(hotelId))''')
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ferry (
            ferryId INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL, 
            description TEXT NOT NULL,
            price FLOAT NOT NULL,
            duration TEXT NOT NULL,
            rating FLOAT DEFAULT 0,
            image TEXT NOT NULL)''')
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ferry_booking (
            bookingId INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER NOT NULL,
            ferryId INTEGER NOT NULL,
            price FLOAT NOT NULL,
            ticketCode TEXT,
            FOREIGN KEY (userId) REFERENCES user(userId),
            FOREIGN KEY (ferryId) REFERENCES ferry(ferryId))''')
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS theme_park (
            themeParkId INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT UNIQUE NOT NULL, 
            description TEXT NOT NULL, 
            price FLOAT NOT NULL, 
            duration TEXT NOT NULL, 
            location TEXT NOT NULL, 
            ageLimit TEXT NOT NULL, 
            capacity INTEGER DEFAULT 0, 
            rating FLOAT DEFAULT 0,
            image TEXT NOT NULL)''')
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS theme_park_booking (
            bookingId INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER NOT NULL,
            themeParkId INTEGER NOT NULL,
            price FLOAT NOT NULL,
            ticketCode TEXT,
            FOREIGN KEY (userId) REFERENCES user(userId),
            FOREIGN KEY (themeParkId) REFERENCES theme_park(themeParkId))''')
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotion (
            promoId INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            description TEXT NOT NULL, 
            offer TEXT NOT NULL, 
            promoCode TEXT UNIQUE NOT NULL, 
            fromDate TEXT NOT NULL, 
            toDate TEXT NOT NULL)''')
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS event (
            eventId INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            description TEXT NOT NULL,
            buttonText TEXT NOT NULL, 
            tag TEXT NOT NULL,
            image TEXT)''')
            
        conn.commit()

def SeedDatabase():
    InitializeDatabase()
    
    # 1. Image paths configuration
    image_paths = [
        'static/profile_1.jpg',
        'static/profile_2.jpg',
        'static/profile_3.jpg',
        'static/profile_4.jpg',
        'static/theme-park/fantasy_world.jpg',
        'static/theme-park/island_thrills.jpg',
        'static/theme-park/ocean_splash.jpg',
        'static/hotel/azure_resort.jpg',
        'static/hotel/coral_haven.jpg',
        'static/hotel/sunset_lagoon.jpg',
        'static/ferry/express_cruiser.jpg',
        'static/ferry/island_hopper.jpg',
        'static/ferry/night_star.jpg',
        'static/event/music_fest.jpg',
        'static/event/night_scuba.jpg',
        'static/event/culinary_gala.jpg'
    ]
    
    # Generate all random 100x100 pictures
    for path in image_paths:
        GenerateRandomImage(path, width=100, height=100)

    with ConnectDatabase() as conn:
        cursor = conn.cursor()
        
        # 2. Seed Users
        users = [
            ('NightRaven', '1', 'nightraven@kudagiri.mv', 'admin', 5000, 'static/profile_1.jpg'),
            ('Livv', '2', 'livv@kudagiri.mv', 'user', 1200, 'static/profile_2.jpg'),
            ('Naushyn', '3', 'naushyn@kudagiri.mv', 'user', 850, 'static/profile_3.jpg'),
            ('Jinaah', '4', 'jinaah@kudagiri.mv', 'user', 2000, 'static/profile_4.jpg')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO user (username, password, email, role, balance, profilePicture)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', users)

        # 3. Seed Theme Parks (3 entries)
        theme_parks = [
            ('Fantasy World Maldives', 'An exciting water and adventure park right on the coast.', 45.0, 'Full Day', 'Male Atoll', 'All Ages', 500, 4.8, 'static/theme-park/fantasy_world.jpg'),
            ('Island Thrills Park', 'High-speed roller coasters and tropical zip lines.', 60.0, '6 Hours', 'Hulhumale', '12+', 300, 4.6, 'static/theme-park/island_thrills.jpg'),
            ('Ocean Splash Kingdom', 'A massive inflatable sea park with water slides and obstacle courses.', 35.0, '4 Hours', 'Maafushi', '6+', 250, 4.7, 'static/theme-park/ocean_splash.jpg')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO theme_park (name, description, price, duration, location, ageLimit, capacity, rating, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', theme_parks)

        # 4. Seed Hotels (3 entries)
        hotels = [
            ('Azure Beach Resort', 'Luxury oceanfront resort with pristine beach views.', 250.0, 4.9, 4, '45 sqm', 'King Bed', 'WiFi, Pool, Spa, Breakfast', '10% OFF direct bookings', 'static/hotel/azure_resort.jpg'),
            ('Coral Reef Haven', 'Charming boutique hotel located steps from vibrant dive spots.', 150.0, 4.5, 2, '30 sqm', 'Queen Bed', 'WiFi, Dive Center, Restaurant', 'Free airport shuttle', 'static/hotel/coral_haven.jpg'),
            ('Sunset Lagoon Villa', 'Private overwater bungalows with panoramic sunset vistas.', 450.0, 5.0, 2, '70 sqm', 'King Bed', 'Private Pool, Butler, WiFi', 'Complimentary dinner', 'static/hotel/sunset_lagoon.jpg')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO hotel (name, description, price, rating, capacity, roomSize, bedType, amenities, offers, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', hotels)

        # 5. Seed Ferries (3 entries)
        ferries = [
            ('Express Atoll Cruiser', 'Fast catamaran ferry connecting Male to nearby atolls.', 20.0, '45 Mins', 4.6, 'static/ferry/express_cruiser.jpg'),
            ('Island Hopper Ferry', 'Scenic scheduled ferry for relaxed island hopping.', 12.0, '1.5 Hours', 4.3, 'static/ferry/island_hopper.jpg'),
            ('Night Star Voyager', 'Late-night inter-island passenger and luggage ferry service.', 25.0, '1 Hour', 4.1, 'static/ferry/night_star.jpg')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO ferry (name, description, price, duration, rating, image)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ferries)

        # 6. Seed Promotions (3 entries)
        promotions = [
            ('Summer Special', 'Get $50 off on hotel bookings exceeding $200.', '$50 Off', 'SUMMER50', '2026-06-01', '2026-08-31'),
            ('Ferry Bundle Deal', 'Enjoy 20% discount on all island ferry tickets.', '20% Discount', 'FERRY20', '2026-01-01', '2026-12-31'),
            ('Park Pass Promo', 'Buy 2 Theme Park tickets and get 1 free.', 'Buy 2 Get 1 Free', 'PARK3FOR2', '2026-05-01', '2026-10-31')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO promotion (name, description, offer, promoCode, fromDate, toDate)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', promotions)

        # 7. Seed Events (3 entries)
        events = [
            ('Island Music & Cultural Fest', 'A night of traditional beat drums, local food stalls, and live music.', 'Book Ticket', 'Festival', 'static/event/music_fest.jpg'),
            ('Night Scuba & Bioluminescence Tour', 'Explore glowing night waters and underwater marine life.', 'Reserve Spot', 'Adventure', 'static/event/night_scuba.jpg'),
            ('Culinary Ocean Gala', 'Exclusive 5-course dinner prepared by top international chefs.', 'Register Now', 'Dining', 'static/event/culinary_gala.jpg')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO event (name, description, buttonText, tag, image)
            VALUES (?, ?, ?, ?, ?)
        ''', events)

        # 8. Sample Bookings
        cursor.execute('''
            INSERT OR IGNORE INTO hotel_booking (userId, hotelId, price, checkInDate, checkOutDate, ticketCode, promoCode, numGuests)
            VALUES (2, 1, 250.0, '2026-10-10', '2026-10-12', 'HB-1001', 'SUMMER50', 2)
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO theme_park_booking (userId, themeParkId, price, ticketCode)
            VALUES (3, 1, 45.0, 'TP-2001')
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO ferry_booking (userId, ferryId, price, ticketCode)
            VALUES (4, 2, 12.0, 'FB-3001')
        ''')

        conn.commit()
        print("Database initialized, 100x100 images generated, and records seeded successfully!")

if __name__ == '__main__':
    SeedDatabase()