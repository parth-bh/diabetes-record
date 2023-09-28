import streamlit_authenticator as stauth

from code_db import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///database/project_db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()


names = ["XXXX", "XXXXXX"]
usernames = ["XXXX", "XXXX"]
passwords = ["****", "****"]

# Don't run the file again.

hashed_passwords = stauth.Hasher(passwords).generate()

try:
    user1 = User(name=names[0], username=usernames[0], password=hashed_passwords[0])
    user2 = User(name=names[1], username=usernames[1], password=hashed_passwords[1])
    sess.add(user1)
    sess.add(user2)
    sess.commit()
    print("Done")

except Exception as error:
    sess.rollback()
    print(error)

