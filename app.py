import streamlit as st
import sqlite3
import pandas as pd 

def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, age INTEGER)')
    conn.commit()
    conn.close()

def add_user(name, email, age):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(name, email, age) VALUES (?, ?, ?)', (name, email, age))
    conn.commit()
    conn.close()
    
def view_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    data = c.fetchall()
    conn.close()
    return data

def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    
create_table()

st.title("Lourence's User Management App")

menu = ["Add User", "View Users", "Delete User"]
choice = st.sidebar.selectbox("Menu", menu)

st.sidebar.info(f"You selected: **{choice}**")
st.markdown("---")

if choice == "Add User":
    st.subheader("Add New User")
    with st.form(key='add_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1)
        submit_button = st.form_submit_button("Submit User")

    if submit_button:
        if name and email: 
            add_user(name, email, age)
            st.success(f"**{name}** added successfully!")
        else:
            st.error("Please enter yout Name and Email.")

elif choice == "View Users":
    st.subheader("View All Users")
    users = view_users()
    df = pd.DataFrame(users, columns= ["ID", "Name", "Email", "Age"])
    st.dataframe(df, use_container_width=True)

elif choice == "Delete User":
    st.subheader("Delete a User")
    users = view_users()
    df = pd.DataFrame(users, columns=["ID", "Name", "Email", "Age"])

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        user_ids = df['ID'].tolist()

        if user_ids:
            user_id_to_delete = st.selectbox("Enter ID to delete", user_ids)
        else:
            st.warning("No users with that name.")
            user_id_to_delete = None

        if st.button("Delete") and user_id_to_delete:
            delete_user(user_id_to_delete)
            st.success(f"User {user_id_to_delete}** deleted")
            st.rerun()

    else:
        st.info("The user table empty.")
        
