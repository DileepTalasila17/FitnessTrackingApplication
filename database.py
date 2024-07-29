import mysql.connector
from mysql.connector import Error
import streamlit as st

db_config = {
    'user': 'root',
    'password': 'Hexaware@123', 
    'host': 'localhost', 
    'database': 'fitness_tracker_app'
}

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None
