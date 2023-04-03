from fastapi import FastAPI, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status, HTTPException
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from data import data 
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("../saved_models/1")

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

class User(BaseModel):
    HoTen: str
    TenDN: str
    DiaChi: str
    NgaySinh: str
    MatKhau: str
    
@app.post("/login")
async def login_user(TenDN, MatKhau):
    data.create_table_user()
    results = data.Login(TenDN, MatKhau)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this id {id} does not exist",
        )
    return results

@app.delete("/delete_result_by_id/{id}")
async def login_user(id):
    data.create_table_user()
    results = data.deleteResultByID(id)
    # if not results:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"User with this id {id} does not exist exist",
    #     )
    return results

@app.get("/get/{id}")
async def get_user(id):
    data.create_table_user() 
    user = data.getUeserByID(id)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"User with this id {id} does not exist",
    #     )
    return user


# @app.post("/user")
# async def insert_user(UserID, HoTen, TenDN, DiaChi, NgaySinh, MatKhau):
#     data.create_table_user()
#     data.insertTableUser(UserID, HoTen, TenDN, DiaChi, NgaySinh, MatKhau)
#     return {
#         "UserID": UserID,
#         "HoTen": HoTen,
#         "TenDN": TenDN,
#         "DiaChi": DiaChi,
#         "NgaySinh" : NgaySinh,
#         "MatKhau" : MatKhau,
#     }


@app.post("/user")
async def insert_user(HoTen, TenDN, DiaChi, NgaySinh, MatKhau):
    data.create_table_user()
    data.insertTableUser(HoTen, TenDN, DiaChi, NgaySinh, MatKhau)
    return {
        "HoTen": HoTen,
        "TenDN": TenDN,
        "DiaChi": DiaChi,
        "NgaySinh" : NgaySinh,
        "MatKhau" : MatKhau,
    }
    
@app.put("/update_user/{UserID}")
async def update_user(UserID, HoTen, TenDN, DiaChi, NgaySinh, MatKhau):
    data.create_table_user()
    data.update_table_users(UserID, HoTen, TenDN, DiaChi, NgaySinh, MatKhau)
    return {
        "UserID": UserID,
        "HoTen": HoTen,
        "TenDN": TenDN,
        "DiaChi": DiaChi,
        "NgaySinh" : NgaySinh,
        "MatKhau" : MatKhau,
    }
    
def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

class Result(BaseModel):
    UserID: int
    LinkImg: str
    file: UploadFile = File(...)

@app.post("/results")
async def insert_results( UserID, LinkImg, file: UploadFile = File(...)):
    data.create_table_user()
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    
    predictions = MODEL.predict(img_batch)
    today = datetime.now()
    NgayTest = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    TenBenh, DoChinhXac = predicted_class, float(confidence)
    data.insertTableResults(UserID, LinkImg, TenBenh, NgayTest, DoChinhXac)
    return {
        "UserID": UserID,
        "LinkImg": LinkImg,
        "TenBenh": TenBenh,
        "NgayTest": NgayTest,
        "DoChinhXac" : DoChinhXac
    }
# @app.post("/results")
# async def insert_results( item: Result = Body(embed=True)):
#     data.create_table_user()
#     today = datetime.now()
#     NgayTest = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
#     image = read_file_as_image(await item.file.read())
#     img_batch = np.expand_dims(image, 0)
    
#     predictions = MODEL.predict(img_batch)

#     predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
#     confidence = np.max(predictions[0])
#     TenBenh, DoChinhXac = predicted_class, float(confidence)
#     data.insertTableResults(item.UserID, item.LinkImg, TenBenh, NgayTest, DoChinhXac)
#     return {
#         "UserID": UserID,
#         "LinkImg": LinkImg,
#         "TenBenh": TenBenh,
#         "NgayTest": NgayTest,
#         "DoChinhXac" : DoChinhXac
#     }
    

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=5000)

