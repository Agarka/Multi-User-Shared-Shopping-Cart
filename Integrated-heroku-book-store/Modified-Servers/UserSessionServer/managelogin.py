from pymongo import MongoClient
import uuid
import os, base64
import json
import datetime

client = MongoClient('mongodb://localhost:27017/')

# book-store is the database name
db = client['book-store']

# Collections
user_data = db['Users']
sessions_data = db['Sessions']

# Class for user details
class User:
    def __init__(self, first_name, last_name, email, password, id = 0 ):
        if id == 0:
            self.id = generate_userid()
        else:
            self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


# Class for user session
class Session:
    def __init__(self, userID):
        self.userID = userID,
        self.sessionID = generate_session()
        self.expires = datetime.datetime.now() + datetime.timedelta(hours=3)
        print("datetime : " + str(self.expires))


# Generates a new session value
def generate_session():
    return base64.b64encode(os.urandom(16))


# Generates a new user ID
def generate_userid():
    return str(uuid.uuid4())


#----------------------- BASIC CRUD METHODS FOR USER INFORMATION -----------------------------------#

# Creates a user
def create_user(first_name, last_name, email, password):
    new_user = User(first_name, last_name, email, password)
    result = add_user(new_user)
    if result == 0 or result is None:
        return result
    else:
        new_session = Session(result)
        session_id = add_session(new_session)
        if session_id is None:
            return 1
        else:
            session_str = session_id.decode('utf-8');
            return {'id': new_user.id, 'session': session_str}



# Adds user information to the Users table
def add_user(user):
    if verify_unique_email(user.email):
        try:
            user_data.insert_one(
                    {
                        'id': user.id,
                        'firstname': user.first_name,
                        'lastname': user.last_name,
                        'email': user.email,
                        'password': user.password
                    }
                )
            return user.id
        except:
            return None
    else:
        print("Email already exists. Log in or use a new email.")
        return 0


# Fetches user details based on user ID
def get_user(id):
    return user_data.find_one({'id': id})

# Verify the user credentials
def verify_user(email, password):
    result = verify_unique_email(email)
    print(str(result))
    if result is False:
        result = user_data.find_one({'email': email, 'password' : password})
        if result is None:
            return None
        else:
            return result["id"]
    else:
        return 0

# Verify the email for register is unique
def verify_unique_email(email):
    result =  user_data.find_one({'email': email})
    if result is None:
        return True
    else:
        return False

# Delete user based on user ID
def delete_user(id):
    user_data.delete_one({'id': id})


# Update user details
def update_user(user):
    try:
        return user_data.update_one(
            {"id": user.id},
                {
                "$set": {
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'email': user.email,
                    'password': user.password
                }
            }
        )
    except:
        return None

#----------------------- BASIC CRUD METHODS FOR SESSION INFORMATION -----------------------------------#
# Adds a session entry to the Sessions table
def add_session(session):
    try:
        sessions_data.insert_one(
            {
                'userid': session.userID,
                'sessionid': session.sessionID,
                'expires' : session.expires
            }
        )
        return session.sessionID
    except:
        return None;



# Fetches session details based on user ID
def get_session(userID):
    return sessions_data.find_one({'userid': userID})


# Delete session entry based on User ID
def delete_session(userID):
    try:
        return sessions_data.delete_one({'userid': userID})
    except:
        return None


# Update session value for a user
def update_session(session):
    sessions_data.update_one(
        {"userid": session.userID},
            {
                "$set": {
                    'sessionid': session.sessionID
                }
            }
    )

# Verify if the session for the user is valid
def verify_session(id, session_value):
    result = sessions_data.find_one({'userid': id, 'sessionid' : session_value})
    if result is None:
        return False
    else:
        currentdate = datetime.datetime.now()
        print("current : " + str(currentdate))
        if currentdate < result["expires"]:
            return True
        else:
            return False

# Verify login and create session
def verify_login_create_session(email, password):
    id = verify_user(email, password)
    if id == 0:
        return 1
    if id is not None:
        try:
            # if valid create a session, store it and return session value to the client.
            delete_session(id)
            session = Session(id)
            print ("session :" + str(session.sessionID))
            add_session(session)
            session_str = session.sessionID.decode('utf-8')
            user = get_user(id)
            print(str(user))
            return {'id': id, 'firstname': user['firstname'], 'lastname': user['lastname'],'email': user['email'], 'password': user['password'], 'session': session_str}
        except:
            return 0
    else:
        return id

    

