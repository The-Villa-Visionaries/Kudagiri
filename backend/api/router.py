from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.common import GetAllPromotions, CreatePromotion, GetAllEvents, CreateEvent, CreateTicket, ValidateTicket
from services.hotel import GetAllHotels, HotelBooking, CreateHotel, CheckHotelBooked, UpdateHotel
from services.ferry import GetAllFerry, FerryBooking, CreateFerry
from services.themepark import GetThemePark, ThemeParkBooking, CreateThemePark
from schemas import FetchAllHotels, BookHotel, MakeHotels, FetchAllFerry, BookFerry, MakeFerry, FetchAllThemeParks, BookThemeParks, MakeThemeParks, FetchAllPromos, MakePromo, FetchAllEvents, MakeEvents, CheckHotelBooking, GenerateTicket, CheckTicket

router = APIRouter()

class HotelPage(BaseModel):
    requestId:int
@router.post('/api/hotel', tags=['Hotel Page'], status_code=200)
def FetchHotelPage(data:HotelPage):
    hotelList = GetAllHotels(data)
    promotions = GetAllPromotions(data)
    if not hotelList and not promotions:
        raise HTTPException(status_code=404, detail='No content found')
    return {'hotels': hotelList, 'promotions': promotions}

@router.post('/api/hotel/book', tags=['Hotel Page'], status_code=200)
def BookHotelResponse(data:BookHotel):
    HotelBooking(data)
    return {'message': 'Hotel booked successfully'}

@router.post('/api/hotel/create', tags=['Manage Hotel Page'], status_code=200)
async def CreateHotelResponse(data:MakeHotels = Depends()):
    hotelName = await CreateHotel(data)
    return {'message': f'Hotel {hotelName} created successfully'}

@router.post('/api/hotel/check-booking', tags=['Hotel Page'], status_code=200)
def CheckHotelBookingResponse(data:CheckHotelBooking):
    userId = CheckHotelBooked(data)
    return {'userId': userId}

@router.post('/api/hotel/update', tags=['Manage Hotel Page'], status_code=200)
async def UpdateHotelBookingResponse(data:MakeHotels = Depends()):
    hotelName = await UpdateHotel(data)
    return {'message': f'Hotel {hotelName} booking updated successfully'}

class FerryPage(BaseModel):
    requestId:int
@router.post('/api/ferry', tags=['Ferry Page'], status_code=200)
def FetchFerryPage(data:FerryPage):
    ferryList = GetAllFerry(data)
    events = GetAllEvents(data)
    if not ferryList and not events:
        raise HTTPException(status_code=404, detail='No content found')
    return {'ferries': ferryList, 'events': events}

@router.post('/api/ferry/book', tags=['Ferry Page'], status_code=200)
def BookFerryResponse(data:BookFerry):
    FerryBooking(data)
    return {'message': 'Ferry booked successfully'}

@router.post('/api/ferry/create', tags=['Manage Ferry Page'], status_code=200)
async def CreateFerryResponse(data:MakeFerry = Depends()):
    ferryName = await CreateFerry(data)
    return {'message': f'Ferry {ferryName} created successfully'}

@router.post('/api/ferry/generate-ticket', tags=['Ferry Page'], status_code=200)
def GenerateFerryTicket(data:GenerateTicket):
    data.type = 'Ferry'
    ticketCode = CreateTicket(data)
    return {'ticketCode': ticketCode}

@router.post('/api/ferry/check-ticket', tags=['Ferry Page'], status_code=200)
def CheckFerryTicket(data:CheckTicket):
    data.type = 'Ferry'
    isValid = ValidateTicket(data)
    return {'isValid': isValid}

class ThemeParkPage(BaseModel):
    requestId:int
@router.post('/api/theme-park', tags=['Theme Park Page'], status_code=200)
def FetchThemeParkPage(data:ThemeParkPage):
    events = GetAllEvents(data)
    themeParkList = GetThemePark(data)
    if not themeParkList and not events:
        raise HTTPException(status_code=404, detail='No content found')
    return {'themeParks': themeParkList, 'events': events}

@router.post('/api/theme-park/book', tags=['Theme Park Page'], status_code=200)
def BookThemeParkResponse(data:BookThemeParks):
    ThemeParkBooking(data)
    return {'message': 'Theme park booked successfully'}

@router.post('/api/theme-park/create', tags=['Manage Theme Park Page'], status_code=200)
async def CreateThemeParkResponse(data:MakeThemeParks = Depends()):
    themeParkName = await CreateThemePark(data)
    return {'message': f'Theme park {themeParkName} created successfully'}

@router.post('/api/theme-park/generate-ticket', tags=['Theme Park Page'], status_code=200)
def GenerateThemeParkTicket(data:GenerateTicket):
    data.type = 'ThemePark'
    ticketCode = CreateTicket(data)
    return {'ticketCode': ticketCode}

@router.post('/api/theme-park/check-ticket', tags=['Theme Park Page'], status_code=200)
def CheckThemeParkTicket(data:CheckTicket):
    data.type = 'ThemePark'
    isValid = ValidateTicket(data)
    return {'isValid': isValid}

@router.post('/api/promotion/create', tags=['Manage Promotion Page'], status_code=200)
def CreatePromotionResponse(data:MakePromo):
    promotionName = CreatePromotion(data)
    return {'message': f'Promotion {promotionName} created successfully'}

@router.post('/api/event/create', tags=['Manage Event Page'], status_code=200)
async def CreateEventResponse(data:MakeEvents = Depends()):
    eventName = await CreateEvent(data)
    return {'message': f'Event {eventName} created successfully'}
