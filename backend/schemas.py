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

class CheckHotelBooking(BaseModel):
    requestId:int
    userId:int

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

@dataclass
class UpdateHotels:
    requestId:int = Form()
    name:str = Form()
    newName:str = Form()
    description:str = Form()
    price:int = Form()
    capacity:int = Form()
    roomSize:str = Form()
    bedType:str = Form()
    amenities:str = Form()
    offers: Optional[str] = Form()
    image:Optional[UploadFile] = File()

class DeleteHotels(BaseModel):
    requestId:int
    name:str

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

@dataclass
class EditFerry:
    requestId:int = Form()
    name:str = Form()
    newName:str = Form()
    description:str = Form()
    price:int = Form()
    duration:str = Form()
    image:Optional[UploadFile] = File()

class DelFerry(BaseModel):
    requestId:int
    name:str

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

@dataclass
class UpdateThemeParks:
    requestId:int = Form()
    name:str = Form()
    newName:str = Form()
    description:str = Form()
    price:int = Form()
    duration:str = Form()
    location:str = Form()
    ageLimit:str = Form()
    capacity:int = Form()
    image:Optional[UploadFile] = File()

class DeleteThemeParks(BaseModel):
    requestId:int
    name:str

class CheckThemeParksBookings(BaseModel):
    requestId:Optional[int] = None
    themeParkId:int

class GenerateTicket(BaseModel):
    requestId:int
    type:Optional[str] = None
    typeId:int
    price:float

class CheckTicket(BaseModel):
    requestId:int
    type:Optional[str] = None
    ticketCode:str

class FetchAllPromos(BaseModel):
    requestId:int

class MakePromo(BaseModel):
    name:str
    description:str
    offer:str
    promoCode:str
    fromDate:str
    toDate:str

class UpdatePromo(BaseModel):
    requestId:int
    name:str
    description:str
    offer:str
    promoCode:str
    fromDate:str
    toDate:str

class DeletePromo(BaseModel):
    requestId:int
    name:str

class FetchAllEvents(BaseModel):
    requestId:int

@dataclass
class MakeEvents:
    name:str = Form()
    description:str = Form()
    buttonText:str = Form()
    tag:str = Form()
    image:UploadFile = File()

@dataclass
class UpdateEvents:
    requestId:int = Form()
    name:str = Form()
    newName:str = Form()
    description:str = Form()
    buttonText:str = Form()
    tag:str = Form()
    image:Optional[UploadFile] = File()

class DeleteEvents(BaseModel):
    requestId:int
    name:str

class Review(BaseModel):
    requestId:int
    type:Optional[str] = None
    typeId:int