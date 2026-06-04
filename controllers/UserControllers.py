from services.UserServices import fetch_users,insert_user

def get_users(user_id):
    print(user_id)
    users = fetch_users(user_id)
    print(users)
    return users
def create_user(user):
    result = insert_user(user)
    print(result)
    return result