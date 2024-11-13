#!/usr/bin/env python3

from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
#import pandas as pd
import json
import os

import mysql.connector
from mysql.connector import Error

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "mge9dn"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}

@app.get("/")  # zone apex
def zone_apex():
    return {"Good Day": "User"}

@app.get('/songs')
def get_songs():
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, songs.image, genres.genre FROM songs LEFT JOIN genres ON songs.genre=genres.genreid ORDER BY id;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}


#@api.get("/sum/{a}/{b}")
#def add(a: int, b: int):
#    return {"sum": a + b}

#@api.get("/multiply/{c}/{d}")
#def multiply(c: int, d: int):
#    return {"product": c * d}

#@api.get("/square/{e}")
#def square(e: int):
#    return {"square": e * e}

#@api.get("/subtract/{f}/{g}")
#def subtract(f: int, g: int):
#    return {"difference": f - g}

#@api.get("/customer/{idx}")
#def customer(idx: int):
    # read the data into a df
#    df = pd.read_csv("customers.csv")
    # filter the data based on the index
#    customer = df.iloc[idx]
#    return customer.to_dict()

#@api.post("/get_body") 
#async def get_body(request: Request):
#    response = await request.json()
#    first_name = response["fname"]
#    last_name = response["lname"]
#    favorite_number = response["favnu"]
#    return {"first_name": first_name, "last_name": last_name, "favorite_number": favorite_number}
    ##return await request.json()
