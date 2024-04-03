# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your Smoothie!")

name_on_order = st.text_input('Name your Smoothie!')

st.write('Choose your fruit to be added to your ' + name_on_order)

cnx = sr.connection("snowflake")
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)

if ingredients_list and name_on_order:
    ingredients = ''

    for each_fruit in ingredients_list:
        ingredients += each_fruit + ' '
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients + """', '"""+name_on_order+"""')"""
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your ' +name_on_order+ 'is ordered!', icon="✅")
