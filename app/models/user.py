from datetime import date
import datetime
import time
import uuid
from typing import Optional, Dict, Any, Union
from pydantic import BaseModel, Field, Json

time = datetime.datetime.now()
# class Device(BaseModel):
#     category: str = Field(...)
#     mobile_brand_name: str = Field(...)
#     mobile_model_name: str = Field(...)
#     is_limited_ad_tracking: bool = Field(...)
#     time_zone_offset_seconds: int = Field(...)

class UserSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    device: Dict[str, Union[int,bool,str]]
    geo: Dict[str,Union[int,bool,str]]
    user_install_timestamp: int = Field(...)
    user_first_touch_timestamp: int = Field(...)
    user_properties: Dict[str,Union[int,bool,str]]

    class Config:
        user_profile = {
            "device": {
                "category": "mobile",
                "mobile_brand_name": "Xiaomi",
                "mobile_model_name": "ABC-123",
                "is_limited_ad tracking": True,
                "time_zone_offset_seconds": 84500
            },
            "geo":{
                "continent": "Asia",
                "sub-continent": None,
                "country": "Vietnam",
                "region":  "Southeast",
                "city": "Ho Chi Minh"
            },
            "user_install_timestamp": 1677986918644000,
            "user_first_touch_timestamp": 1677986918645000,
            "user_properties": {
                "ga_session_number": 0,
                "ga_level": 0,
                "ga_arrow_level": 0,
                "ga_gold_income_level": 0,
                "ga_gold": 500,
                "ga_arrow_type_use": "Default"
            }
        }

class EventSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    event_date:  str = Field(...)
    event_timestamp: str = Field(...)
    event_previous_timestamp: str = Field(...)
    event_name: str = Field(...)
    event_parameters: Dict[str,Union[int,bool,str]]
    user_id: str = Field(...)
    user_properties: Dict[str,Union[int,bool,str]]

    class Config:
         event = {
            "event_date" : date.today().strftime("%Y%m%d"),
            "event_timestamp": time.time(),
            "event_previous_timestamp": time.time(),
            "event_name": "session_start",
            "event_parameters": {
                "session_engaged": 1,
                "ga_session_id": 1686298318,
                "engaged_session_event": 1
            },
            "user_id": "6498f76fd2c13f2f3eb9cf8a",
            "user_properties": {
                "ga_session_number": 40,
                "ga_level": 10,
                "ga_arrow_level": 3,
                "ga_gold_income_level": 5,
                "ga_gold": 5000,
                "ga_arrow_type_use": "AK-47"
            }
        }
        

class UpdateUserSchema(BaseModel):
    device: Optional[Dict[str,Union[str,bool,int]]]
    geo: Optional[Dict[str,Union[str,bool,int]]]
    user_install_timestamp: Optional[int]
    user_first_touch_timestamp: Optional[int]
    user_properties: Optional[Dict[str,Union[str,bool,int]]]

    class Config:
        user_profile = {
            "device": {
                "category": "mobile",
                "mobile_brand_name": "Xiaomi",
                "mobile_model_name": "ABC-123",
                "is_limited_ad tracking": True,
                "time_zone_offset_seconds": 84500
            },
            "geo":{
                "continent": "Asia",
                "sub-continent": None,
                "country": "Vietnam",
                "region":  "Southeast",
                "city": "Ho Chi Minh"
            },
            "user_install_timestamp": 1677986918644000,
            "user_first_touch_timestamp": 1677986918645000,
            "user_properties": {
                "ga_session_number": 0,
                "ga_level": 0,
                "ga_arrow_level": 0,
                "ga_gold_income_level": 0,
                "ga_gold": 500,
                "ga_arrow_type_use": "Default"
            }
        }