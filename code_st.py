import streamlit as st  
import streamlit_authenticator as stauth  

from code_db import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime
import time
import pandas as pd

## -------------------------------------------------       SetUp with the database

engine = create_engine('sqlite:///database/project_db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()


st.set_page_config(page_title="Diabetes Record", page_icon=":bar_chart:", layout="wide")


# --------------------------------------------------      USER AUTHENTICATION

try: 

    result = sess.query(User).all()

    names = []
    usernames = []
    hashed_passwords = []

    for row in result:
        names.append(row.name)
        usernames.append(row.username)
        hashed_passwords.append(row.password)
    sess.close()
except Exception as error:
    sess.rollback()
    print(error)

credentials = {"usernames":{}}

for un, name, pw in zip(usernames, names, hashed_passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})

authenticator = stauth.Authenticate(credentials, "cookie", "secret_key", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")


# --------------------------------------------------       USER CREDENTIONAL WRONG


if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == True:


# --------------------------------------------------       USER LOGGED-IN

    st.session_state.add_record = 0
    st.session_state.delete_record = 0

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    st.markdown('## Diabetes Record')

# --------------------------------------------------       Sidebar for adding new records
    
    st.sidebar.header("Add New Record")

    date = st.sidebar.date_input("Date")
    time = st.sidebar.time_input("Time")
    blood_sugar_level = st.sidebar.number_input("Blood Sugar Level")
    notes = st.sidebar.text_area("Notes")
    fasting = st.sidebar.checkbox("Fasting")


    if st.sidebar.button("Add Record"):
        st.sidebar.success("Record added successfully!")

        try:
            record = MainData(sugar_level=str(blood_sugar_level), 
                            fasting = fasting,
                            date = str(date),
                            time = str(time),
                            note = notes, 
                            username= username,
                            time_of_entry= datetime.datetime.now())
            sess.add(record)
            sess.commit()
            print("Record Submitted")

        except Exception as error:
            sess.rollback()
            print("error occured: ",error)


# --------------------------------------------------        DISPLAY ALL RECORDS


    try:
        all_records = sess.query(MainData).all()
        df = pd.DataFrame([record.__dict__ for record in all_records])
        st.dataframe(df[['sugar_level', 'date', 'time', 'fasting', 'element_id']])

        if st.button("Delete Record"):
            show_delete_form = not st.session_state.get("show_delete_form", False)
            st.session_state.show_delete_form = show_delete_form


# --------------------------------------------------         DELETE RECORD


        if st.session_state.get("show_delete_form", False):
            st.text("Row Number is written in first column and starts with 0.")

            row_no = st.number_input("Enter Row Number: ")
            submit_button = st.button("Delete")
            if submit_button:
                if int(row_no)<0:
                    st.write("Input not be negative.")
                if int(row_no)>df.shape[0]-1:
                    st.write(f"Input should be less than than the max number of rows available i.e. {df.shape[0]-1}")

                record_no = df['element_id'][int(row_no)]
                try:
                    record_to_delete = sess.query(MainData).filter(MainData.element_id == str(record_no)).first()
                    sess.delete(record_to_delete)
                    sess.commit()
                    print("Record has been delete successfully.")
                    st.write("Deletion Successfully.")
                    # Display a message to indicate that the page is refreshing
                    st.text("Refreshing the page...")
                    # Redirect the user to the same page using a URL query parameter
                    st.experimental_rerun()
                except Exception as error:
                    sess.rollback()
                    print("Error occured: ", error)
                    st.write("Contact Admin: ERROR while deleting from DATABASE.")


    except Exception as error:
        print("error occured: ",error)
