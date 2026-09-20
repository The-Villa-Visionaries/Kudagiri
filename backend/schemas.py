from fastapi import File, Form, UploadFile
from pydantic import BaseModel
from dataclasses import dataclass

class FetchAllHotels(BaseModel):
    requestId:int

class BookHotel(BaseModel):
    requestId:int
    hotelId:int
    price:float
    checkInDate:str
    checkOutDate:str
    numGuests:int
    promoCode:str

@dataclass
class MakeHotels:
    name:str = Form()
    description:str = Form()
    price:int = Form()
    rating:int = Form()
    capacity:int = Form()
    roomSize:str = Form()
    bedType:str = Form()
    amenities:str = Form()
    offers:str = Form()
    guests:int = Form()
    image:UploadFile = File()

class CheckHotelBooking(BaseModel):
    requestId:int
    userId:int

class FetchAllFerry(BaseModel):
    requestId:int

class BookFerry(BaseModel):
    requestId:int
    ferryId:int

@dataclass
class MakeFerry:
    name:str = Form()
    description:str = Form()
    price:int = Form()
    rating:int = Form()
    duration:str = Form()
    image:UploadFile = File()

class FetchAllThemeParks(BaseModel):
    requestId:int

class BookThemeParks(BaseModel):
    requestId:int
    themeParkId:int
    price:float
    ticketCode:str

@dataclass
class MakeThemeParks:
    name:str = Form()
    description:str = Form()
    price:int = Form()
    rating:int = Form()
    duration:str = Form()
    location:str = Form()
    ageLimit:str = Form()
    capacity:int = Form()
    image:UploadFile = File()

class FetchAllPromos(BaseModel):
    requestId:int

class MakePromo(BaseModel):
    name:str
    description:str
    offer:str
    promoCode:str
    fromDate:str
    toDate:str

class FetchAllEvents(BaseModel):
    requestId:int

@dataclass
class MakeEvents:
    name:str = Form()
    description:str = Form()
    buttonText:str = Form()
    tag:str = Form()
    image:UploadFile = File()

class GenerateTicket(BaseModel):
    requestId:int
    type:str 
    typeId:int
    price:float
    ticketCode:str

class CheckTicket(BaseModel):
    requestId:int
    ticketCode:str
    type:str
