from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.common import GetAllPromotions, CreatePromotion, GetAllEvents, CreateEvent, CreateTicket, ValidateTicket, DeletePromotion, DeleteEvent, UpdatePromotion, UpdateEvent
from services.hotel import GetAllHotels, HotelBooking, CreateHotel, CheckHotelBooked, UpdateHotel, DeleteHotel
from services.ferry import GetAllFerry, FerryBooking, CreateFerry, UpdateFerry, DeleteFerry
from services.themepark import GetThemePark, ThemeParkBooking, CreateThemePark, UpdateThemePark, DeleteThemePark
from schemas import FetchAllHotels, BookHotel, MakeHotels, FetchAllFerry, BookFerry, MakeFerry, FetchAllThemeParks, BookThemeParks, MakeThemeParks, FetchAllPromos, MakePromo, FetchAllEvents, MakeEvents, CheckHotelBooking, GenerateTicket, CheckTicket, UpdateHotels, DeleteHotels, EditFerry, DelFerry, UpdateThemeParks, DeleteThemeParks, UpdatePromo, DeletePromo, UpdateEvents, DeleteEvents 

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

@router.post('/api/hotel/check-booking', tags=['Hotel Page'], status_code=200)
def CheckHotelBookingResponse(data:CheckHotelBooking):
    userId = CheckHotelBooked(data)
    return {'userId': userId}

@router.post('/api/hotel/create', tags=['Manage Hotel Page'], status_code=200)
async def CreateHotelResponse(data:MakeHotels = Depends()):
    hotelName = await CreateHotel(data)
    return {'message': f'Hotel {hotelName} created successfully'}

@router.post('/api/hotel/update', tags=['Manage Hotel Page'], status_code=200)
async def UpdateHotelBookingResponse(data:UpdateHotels = Depends()):
    hotelName = await UpdateHotel(data)
    return {'message': f'Hotel {hotelName} booking updated successfully'}

@router.post('/api/hotel/delete', tags=['Manage Hotel Page'], status_code=200)
def DeleteHotelResponse(data:DeleteHotels):
    hotelName = DeleteHotel(data)
    return {'message': f'Hotel {hotelName} deleted successfully'}

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
    ticketCode = FerryBooking(data)
    return {'ticketCode': ticketCode}

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

@router.post('/api/ferry/create', tags=['Manage Ferry Page'], status_code=200)
async def CreateFerryResponse(data:MakeFerry = Depends()):
    ferryName = await CreateFerry(data)
    return {'message': f'Ferry {ferryName} created successfully'}

@router.post('/api/ferry/update', tags=['Manage Ferry Page'], status_code=200)
async def UpdateFerryResponse(data:EditFerry = Depends()):
    ferryName = await UpdateFerry(data)
    return {'message': f'Ferry {ferryName} updated successfully'}

@router.post('/api/ferry/delete', tags=['Manage Ferry Page'], status_code=200)
def DeleteFerryResponse(data:DelFerry):
    ferryName = DeleteFerry(data)
    return {'message': f'Ferry {ferryName} deleted successfully'}

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
    ticketCode = ThemeParkBooking(data)
    return {'ticketCode': ticketCode}

@router.post('/api/theme-park/generate-ticket', tags=['Theme Park Page'], status_code=200)
def GenerateThemeParkTicket(data:GenerateTicket):
    data.type = 'ThemePark'
    ticketCode = CreateTicket(data)
    return {'ticketCode': ticketCode}

@router.post('/api/theme-park/check-ticket', tags=['Theme Park Page'], status_code=200)
def CheckThemeParkTicket(data:CheckTicket):
    data.type = 'ThemePark'
    userId = ValidateTicket(data)
    return {'userId': userId}

@router.post('/api/theme-park/create', tags=['Manage Theme Park Page'], status_code=200)
async def CreateThemeParkResponse(data:MakeThemeParks = Depends()):
    themeParkName = await CreateThemePark(data)
    return {'message': f'Theme park {themeParkName} created successfully'}

@router.post('/api/theme-park/update', tags=['Manage Theme Park Page'], status_code=200)
async def UpdateThemeParkResponse(data:MakeThemeParks = Depends()):
    themeParkName = await UpdateThemePark(data)
    return {'message': f'Theme park {themeParkName} updated successfully'}

@router.post('/api/theme-park/delete', tags=['Manage Theme Park Page'], status_code=200)
def DeleteThemeParkResponse(data:MakeThemeParks):
    themeParkName = DeleteThemePark(data)
    return {'message': f'Theme park {themeParkName} deleted successfully'}

@router.post('/api/promotion/create', tags=['Manage Promotion Page'], status_code=200)
def CreatePromotionResponse(data:MakePromo):
    promotionName = CreatePromotion(data)
    return {'message': f'Promotion {promotionName} created successfully'}

@router.post('/api/promotion/update', tags=['Manage Promotion Page'], status_code=200)
def UpdatePromotionResponse(data:UpdatePromo):
    promotionName = UpdatePromotion(data)
    return {'message': f'Promotion {promotionName} updated successfully'}

@router.post('/api/promotion/delete', tags=['Manage Promotion Page'], status_code=200)
def DeletePromotionResponse(data:DeletePromo):
    promotionName = DeletePromotion(data)
    return {'message': f'Promotion {promotionName} deleted successfully'}

@router.post('/api/event/create', tags=['Manage Event Page'], status_code=200)
async def CreateEventResponse(data:MakeEvents = Depends()):
    eventName = await CreateEvent(data)
    return {'message': f'Event {eventName} created successfully'}

@router.post('/api/event/update', tags=['Manage Event Page'], status_code=200)
async def UpdateEventResponse(data:UpdateEvents = Depends()):
    eventName = await UpdateEvent(data)
    return {'message': f'Event {eventName} updated successfully'}

@router.post('/api/event/delete', tags=['Manage Event Page'], status_code=200)
def DeleteEventResponse(data:DeleteEvents):
    eventName = DeleteEvent(data)
    return {'message': f'Event {eventName} deleted successfully'}