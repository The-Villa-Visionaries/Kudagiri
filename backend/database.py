import sqlite3, os

DATABASE:str = 'database.db'
REQUIRED_DIRECTORIES:list = ['static', 'static/hotel', 'static/ferry', 'static/theme-park', 'static/event']

def ConnectDatabase():
    """
    Tables Schema Overview
    
    user
        userId :INTEGER
        username :STRING
        password :STRING
        email :STRING
        role :STRING
        balance :INTEGER
        profilePicture :STRING

    sessions
        primarySid :STRING
        altSid :STRING
        uid :INTEGER
        expireTime :FLOAT

    page
        pageId :INTEGER
        title :STRING
        description :STRING
        type :STRING

    hotel
        hotelId :INTEGER
        name :STRING
        description :STRING
        price :FLOAT
        rating :FLOAT
        capacity :INTEGER
        roomSize :STRING
        bedType :STRING
        amenities :STRING
        offers :STRING
        image :STRING

    hotel_booking
        bookingId :INTEGER
        userId :INTEGER
        hotelId :INTEGER
        checkInDate :STRING
        checkOutDate :STRING
        ticketCode :STRING
        promoCode :STRING
        numGuests :INTEGER
        price :FLOAT

    ferry
        ferryId :INTEGER
        name :STRING
        description :STRING
        price :FLOAT
        duration :STRING
        rating :FLOAT
        image :STRING

    ferry_booking
        bookingId :INTEGER
        userId :INTEGER
        ferryId :INTEGER
        ticketCode :STRING
        price :FLOAT

    theme_park
        themeParkId :INTEGER
        name :STRING
        description :STRING
        price :FLOAT
        duration :STRING
        location :STRING
        ageLimit :STRING
        capacity :INTEGER
        rating :FLOAT
        image :STRING

    theme_park_booking
        bookingId :INTEGER
        userId :INTEGER
        themeParkId :INTEGER
        ticketCode :STRING
        price :FLOAT

    promotion
        promoId :INTEGER
        name :STRING
        description :STRING
        offer :STRING
        promoCode :STRING
        fromDate :STRING
        toDate :STRING

    event
        eventId :INTEGER
        name :STRING
        description :STRING
        buttonText :STRING
        tag :STRING
        image :STRING
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def CreateDirectory():
    for folder in REQUIRED_DIRECTORIES:
        if not os.path.exists(folder):
            os.makedirs(folder)

def InitializeDatabase():
    CreateDirectory()
    with ConnectDatabase() as conn:
        cursor = conn.cursor()
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
    return None
