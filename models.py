import datetime

from pydantic import Field, BaseModel, EmailStr, SecretStr


class Good(BaseModel):
    good_id: int = Field(..., title='good_id')
    name: str = Field(..., title='name', max_length=20)
    description: str = Field(None, title='description', max_length=200)
    price: float = Field(..., title='price')


class GoodIn(BaseModel):
    name: str = Field(..., title='name', max_length=20)
    description: str = Field(None, title='description', max_length=200)
    price: float = Field(..., title='price')


class User(BaseModel):
    user_id: int = Field(..., title='user_id')
    name: str = Field(..., title='name', max_length=20)
    last_name: str = Field(None, title='last_name', max_length=20)
    email: EmailStr = Field(..., title='email', max_length=25)
    password: SecretStr = Field(..., title='password', min_length=6, max_length=12)


class UserIn(BaseModel):
    name: str = Field(..., title='name', max_length=20)
    last_name: str = Field(None, title='last_name', max_length=20)
    email: EmailStr = Field(..., title='email', max_length=25)
    password: SecretStr = Field(..., title='password', min_length=6, max_length=12)


class Order(BaseModel):
    order_id: int = Field(..., title='order_id')
    user_id: int = Field(..., title='user_id')
    good_id: int = Field(..., title='good_id')
    order_date: datetime.datetime = Field(..., title='order_date')
    status: str = Field(..., title='status')


class OrderIn(BaseModel):
    user_id: int = Field(..., title='user_id')
    good_id: int = Field(..., title='good_id')
    order_date: datetime.datetime = Field(..., title='order_date')
    status: str = Field(..., title='status')
