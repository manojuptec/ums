from database.connection import get_connection
import bcrypt
from typing import List,Any
#pip install bcrypt
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
    hashed_password = bcrypt.hashpw(
    user.password.encode('utf-8'),
    bcrypt.gensalt()
)
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