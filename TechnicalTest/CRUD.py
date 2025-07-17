import pytest #framework testing bawaan python
import requests #untuk melakukan CALL HTTP (GET, POST, PUT, DELETE)
import os #untuk membaca API TOKEN dari file .env
from dotenv import load_dotenv #untuk membaca API TOKEN dari file .env
import random #untuk membuat eam

load_dotenv() #membaca isi file env
BASE_URL = "https://gorest.co.in/"
TOKEN = os.getenv("API_TOKEN") #mengambil token dari .env
HEADERS = {
    "Authorization": TOKEN, #token bearer
    "Content-Type": "application/json" #sebagai tanda yang dikirim adalah JSON
}

user_id = None #tempat menyimpan ID yang akan dibuat

#==========================POSITIVE=============================
def test_create_user():
    global user_id
    payload = {
        "name": "Test User",
        "gender": "male",
        "email": f"testuser{random.randint(1000, 9999)}@example.com",
        "status": "active"
    }

    response = requests.post(BASE_URL + "/public/v2/users", headers=HEADERS, json=payload)
    assert response.status_code == 201
    user_id = response.json()["id"]
    print ("Test 1: Created user ID:", user_id)

def test_get_user():
    global user_id
    assert user_id is not None
    response = requests.get(f"{BASE_URL}/public/v2/users/{user_id}", headers=HEADERS)
    assert response.status_code == 200
    print("Test 2: Get user => ",response.json())

def test_update_user():
    global user_id
    assert user_id is not None
    payload = {
        "name": "Name Updated",
        "status": "inactive"
    }
    response = requests.put(f"{BASE_URL}/public/v2/users/{user_id}", headers=HEADERS, json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Name Updated"
    print("Test 3: Update User to " + response.json()["name"] + " and " + response.json()["status"])

def test_delete_user():
    global user_id
    assert user_id is not None
    response = requests.delete(f"{BASE_URL}/public/v2/users/{user_id}", headers=HEADERS)
    assert response.status_code == 204
    print ("Test 4: Delete User => Successfully deleted")

def test_get_delete_user():
    global user_id
    assert user_id is not None 
    response = requests.get(f"{BASE_URL}/public/v2/users/{user_id}", headers=HEADERS)
    assert response.status_code == 404
    print("Test 5: Get Deleted User => Data deleted")


#=================CASE NEGATIVE===============
def test_invalid_email():
    payload = {
        "name": "Invalid email user",
        "gender": "male",
        "email": "", #email blank
        "status": "active" 
    }
    response = requests.post(BASE_URL + "public/v2/users/", headers=HEADERS, json=payload)
    assert response.status_code == 422 #Unprocessable entity
    assert "email" in str(response.text).lower()
    #print ("Email must not be blank!")

def test_user_without_token():
    payload = {
        "name": "Unauthorized User",
        "gender": "female",
        "email": f"unauth{random.randint(1000, 9999)}@example.com",
        "status": "active" 
    }
    response = requests.post(BASE_URL + "public/v2/users", json=payload) #No headers
    assert response.status_code == 401 #Unauthorized
    #print ("Unauthorized user!")

def test_non_existing_user():
    fake_id = 9999999
    payload = {
        "name": "Not exist",
        "status": "inactive"
    }
    response = requests.put(f"{BASE_URL}/public/v2/users/{fake_id}", headers=HEADERS, json=payload)
    assert response.status_code == 404 #Not found
    #print ("User not found!")

def already_deleted_user():
    global user_id
    assert user_id is not None
    response = requests.delete(f"{BASE_URL}/public/v2/users/{user_id}", headers=HEADERS)
    assert response.status_code == 404 or response.status_code == 410
    #print ("User tidak ditemukan!")