# This file is used to create the instance of supabase client, so that we can use that client to interact with our supabase database in our project

import streamlit as st

from supabase import create_client, Client
# Here we are imprting the create_client fn from supabase package, which will help us to create the instance of supabase client, so that we can use that client to interact with our supabase database in our project
# so we will use these two functions to create the instance of supabase client, so that we can use that client to interact with our supabase database in our project

# So here we are creating the instance of supabase client, so that we can use that client to interact with our supabase database in our project
supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],   # here streamlit will automatically look for the 'SUPABASE_URL' key in the secrets.toml file inside .streamlit folder and will get the value of that key and will pass it to this create_client function, so that we can use that value to create the instance of supabase client, so that we can use that client to interact with our supabase database in our project
    st.secrets["SUPABASE_KEY"] 
)

