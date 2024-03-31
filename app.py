from fastapi import FastAPI
from sqlalchemy import create_engine
from typing import List
import databases
import sqlalchemy
from models import User, UserIn, Good, GoodIn, Order, OrderIn

DATABASE_URL = 'sqlite:///test_database.db'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = create_engine(DATABASE_URL)

app = FastAPI()

goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column('good_id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(20)),
    sqlalchemy.Column('description', sqlalchemy.Text(200)),
    sqlalchemy.Column('price', sqlalchemy.Float)
)

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(20)),
    sqlalchemy.Column('last_name', sqlalchemy.String(20)),
    sqlalchemy.Column('email', sqlalchemy.String(25)),
    sqlalchemy.Column('password', sqlalchemy.String(12))
)

orders = sqlalchemy.Table(
    'orders',
    metadata,
    sqlalchemy.Column('order_id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.user_id')),
    sqlalchemy.Column('good_id', sqlalchemy.ForeignKey('goods.good_id')),
    sqlalchemy.Column('order_date', sqlalchemy.DateTime()),
    sqlalchemy.Column('status', sqlalchemy.String(15))
)

metadata.create_all(engine)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.post('/add_user/', response_model=User)
async def add_user(user: UserIn):
    query = users.insert().values(
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        password=user.password.get_secret_value())
    last_record_id = await database.execute(query)
    return {**user.dict(), 'user_id': last_record_id}


@app.post('/add_good/', response_model=Good)
async def add_good(good: GoodIn):
    query = goods.insert().values(**good.dict())
    last_record_id = await database.execute(query)
    return {**good.dict(), 'good_id': last_record_id}


@app.post('/add_order', response_model=Order)
async def add_order(order: OrderIn):
    query = orders.insert().values(**order.dict())
    last_record_id = await database.execute(query)
    return {**order.dict(), 'order_id': last_record_id}


@app.get('/get_users/', response_model=List[User])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@app.put('/update_user/{user_id}/', response_model=User)
async def update_user(user_id: int, user: UserIn):
    query = users.update().where(users.c.user_id == user_id).values(
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        password=user.password.get_secret_value())
    await database.execute(query)
    return {**user.dict(), 'user_id': user_id}


@app.delete('/delete_user/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.user_id == user_id)
    await database.execute(query)
    return {'message': "User deleted!"}
