from database.connection import get_connection
import bcrypt
import hashlib
from typing import List,Any
from fastapi import HTTPException
import psycopg2
from fastapi.responses import JSONResponse
SECRET_KEY = "@Man#Key$%2026"
#pip install bcrypt
def hash_password(password):
    return hashlib.sha256(
        f"{password}{SECRET_KEY}".encode()
    ).hexdigest()
#def fetch_users(name=None, age=None):
    # users = [
    #     {"name": "manoj", "age": 24},
    #     {"name": "rahul", "age": 25},
    #     {"name": "manoj", "age": 30}
    # ]
    # # result = []
    # # for u in users:
    # #     if u["name"] == name:
    # #         result.append(u)
    # #     elif u["age"] == age:
    # #         result.append(u)   
    # # return result;     
    # if name:
    #     users = [u for u in users if u["name"] == name]

    # if age:
    #     users = [u for u in users if u["age"] == age]

    # return users

def fetch_users(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT *
    FROM public.get_user_details(%s)
    """,
    (user_id,)
)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(rows) != 0:
        print("hhshs")
        rows = rows[0]
    # convert to list of dict
        users = {
            "name": rows[0],
            "email": rows[1],
            "id":rows[2],
            "status":rows[3],
            "added_date":rows[4].isoformat()
        }
        return {"data":users,"message":"User found successfully","status":200}
    else : 
       print("no data")
       return {"data":None,"message":"User not found","status":404}
       
def insert_user(user):
    conn = get_connection()
    cursor = conn.cursor()
#     hashed_password = bcrypt.hashpw(
#     user.password.encode('utf-8'),
#     bcrypt.gensalt()
# )
    hashed_password = hash_password(user.password)
    cursor.execute(
        """
        SELECT public.user_aud(
        %s::integer,
        %s::CHARACTER varying,
        %s::CHARACTER varying,
        %s::CHARACTER varying,
        %s::smallint,
        %s::CHARACTER varying
    )
        """,
        (
            None,
            user.name,
            user.email,
            hashed_password,
            1,
            "add"
        )
    )
    result = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    # print(result)
    return {
        "message": result["message"],
        "status": 201
    }
def login_detail(user):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        hashed_password = hash_password(user.password)
        token = hash_password(user.email)
        #     print(hashed_password) 
        #     token = bcrypt.hashpw(
        #     user.email.encode('utf-8'),
        #     bcrypt.gensalt()
        # )
    
        query ="""
        SELECT * from public.user_login_logout(
            %s::integer,
            %s::CHARACTER varying,
            %s::CHARACTER varying,
            %s::CHARACTER varying,
            %s::text[],
            %s::CHARACTER varying
            )
        """

        params = (
        None,
        user.email,
        hashed_password,
        token,
        None,
        "login"
        )

        print(cursor.mogrify(query, params).decode("utf-8"))

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.commit()
       
        if len(rows) != 0:
            print("hhshs")
            rows = rows[0]
            rows = rows[0]
            print(rows["name"])
        # convert to list of dict
            users = {
                "id": rows["id"],
                "name": rows["name"],
                "email": rows["email"],
                "status":rows["status"],
                "added_date":rows["added_date"]
            }
            return {"data":users,"message":"User found successfully","status":200}
        else : 
         print("no data")
        return {"data":None,"message":"User not found","status":404}
    except psycopg2.Error as e:

        print("DB Error:", e)

        raise HTTPException(
            status_code=400,
            detail=str(e).split("\n")[0]
        )

    finally:
        cursor.close()
        conn.close()   

def delete_login_user(user_id,token):
    conn = get_connection()
    cursor = conn.cursor()
    query ="""
    SELECT * from public.user_login_logout(
        %s::integer,
        %s::CHARACTER varying,
        %s::CHARACTER varying,
        %s::CHARACTER varying,
        %s::text[],
        %s::CHARACTER varying
        )
     """
    params = (
    user_id,
    None,
    None,
    token,
    None,
    "logout"
    )

    print(cursor.mogrify(query, params).decode("utf-8"))

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if len(rows) != 0:
        print("hhshs")
        rows = rows[0]
        rows = rows[0]
        print(rows)
        return {"data":None,"message":rows["message"],"status":201}
    else : 
       print("no data")
       return {"data":None,"message":"User not found","status":404}   