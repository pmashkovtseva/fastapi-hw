from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', response_model=dict, summary='Root')
def root():
    return {"message": "микросервис для хранения и обновления информации для собак"}


@app.post('/post', response_model=Timestamp, summary='Get Post')
def get_post() -> Timestamp:
    latest_timestamp = max(post_db, key=lambda item: item.id)
    timestamp_id = latest_timestamp.id + 1
    timestamp_entry = Timestamp(id=timestamp_id, timestamp=int(time.time()))
    if timestamp_entry in post_db:
        raise HTTPException(status_code=409, detail='Timestamp already exists')
    post_db.append(timestamp_entry)
    return timestamp_entry


@app.get('/dog', response_model=dict, summary='Get Dogs')
def get_dogs(kind='') -> dict:
    if kind == '':
        return dogs_db
    else:
        dogs_by_kind = {pk: dog for pk, dog in dogs_db.items() if dog.kind == kind}
        return dogs_by_kind


@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(pk: int, name: str, kind: str) -> Dog:
    if pk in dogs_db.keys():
        raise HTTPException(status_code=409, detail='Dog already exists')
    dog_entry = Dog(name=name, pk=pk, kind=kind)
    dogs_db.update({pk: dog_entry})
    return dog_entry


@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Pk')
def get_dog_by_pk(pk: int) -> Dog:
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=404, detail='Dog not found')
    return dogs_db[pk]


@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog')
def update_dog(pk: int, name: str, kind: str) -> Dog:
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=404, detail='Dog not found')
    dog_entry = Dog(name=name, pk=pk, kind=kind)
    dogs_db.update({pk: dog_entry})
    return dog_entry
