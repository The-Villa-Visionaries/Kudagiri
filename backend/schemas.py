from fastapi import File, Form, UploadFile
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional

class FetchAllHotels(BaseModel):
    requestId:int

class BookHotel(BaseModel):
    requestId:int
    hotelId:int
    price:float
    checkInDate:str
    checkOutDate:str
    numGuests:int
    promoCode:Optional[str] = None

@dataclass
class MakeHotels:
    name:str = Form()
    description:str = Form()
    price:int = Form()
    capacity:int = Form()
    roomSize:str = Form()
    bedType:str = Form()
    amenities:str = Form()
    offers: Optional[str] = Form()
    image:UploadFile = File()

class CheckHotelBooking(BaseModel):
    requestId:int
    userId:int

class UpdateHotel(BaseModel):
    requestId:int
    name:str
    newName:str
    description:str
    price:int
    capacity:int
    roomSize:str
    bedType:str
    amenities:Optional[str] = None
    offers:Optional[str] = None

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
    duration:str = Form()
    image:UploadFile = File()

class FetchAllThemeParks(BaseModel):
    requestId:int

class BookThemeParks(BaseModel):
    requestId:int
    themeParkId:int
    price:float

@dataclass
class MakeThemeParks:
    name:str = Form()
    description:str = Form()
    price:int = Form()
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
    type:Optional[str] = None
    typeId:int
    price:float

class CheckTicket(BaseModel):
    requestId:int
    type:Optional[str] = None
    ticketCode:str
