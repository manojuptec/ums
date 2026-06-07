from services.UserServices import fetch_users,insert_user,login_detail,delete_login_user

def get_users(user_id):
    print(user_id)
    users = fetch_users(user_id)
    print(users)
    return users
def create_user(user):
    result = insert_user(user)
    print(result)
    return result
def login_user(user):
    result = login_detail(user)
    print(result)
    return result
def user_logout(user_id,token):
    print(user_id,token)
    result = delete_login_user(user_id,token)
    # print(result)
    return result