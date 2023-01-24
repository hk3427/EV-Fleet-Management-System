import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser


"EV Fleet Management System"

@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df


"## Read individual tables"

sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
try:
    all_table_names = query_db(sql_all_table_names)["relname"].tolist()
    table_name = st.selectbox("Choose a table", all_table_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if table_name:

    sql_table = f"SELECT * FROM {table_name};"
    try:
        df = query_db(sql_table)
        st.dataframe(df)
    except:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )
        
# Customer Vehicle Type 
"## Select customers to display what vehicle item have they bought "

sql_customer_names = "select distinct(name) from customer;"
try:
    customer_names = query_db(sql_customer_names)["name"].tolist()
    customer_name = st.selectbox("Choose a customer", customer_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if customer_name:
    sql_customer = f"""select c.name as customer_name, s.sales_desc as Sales_Description,s.sales_date as sales_date, v.item_name as vehicle
                        from Customer c, Customer_Sales s, vehicle_item v
                        where c.customer_id = s.c_id 
                        and s.it_code = v.item_code 
                        and c.name = '{customer_name}'
                        order by customer_name;"""
    
    try:
        df = query_db(sql_customer)
        st.dataframe(df)
    except:
        st.write(
                "Sorry! Something went wrong with your query, please try again."
        )
    

# Charging Station Count and location
"## Select location and count of charging stations for different EV type"
sql_ev_type = "select distinct(vehicle_type) from charging_stations;"
try:
    ev_type = st.radio("Choose a vehicle type",query_db(sql_ev_type)["vehicle_type"].tolist())
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if sql_ev_type:
    sql_ev = f"""select vehicle_type, STRING_AGG(location,',') as locations, count(vehicle_type) as num_charging_stations 
                 from charging_stations
                 where vehicle_type = '{ev_type}'
                 group by vehicle_type;"""
    
    try:
        df = query_db(sql_ev)
        st.dataframe(df)
    except:
        st.write(
                "Sorry! Something went wrong with your query, please try again."
        )

# Vehicle not Ready for Sale
"## Display the vehicles from a given company that are not yet ready for sale"
sql_company_names = "select distinct(company_name) from company;"
try:
    company_names = query_db(sql_company_names)["company_name"].tolist()
    company_name = st.selectbox("Choose a company name", company_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if sql_ev_type:
    sql_company = f"""select c.company_name, ev.ev_name, ev.ev_range, ev.ev_type, ev.launch_year 
    from company c,electric_vehicle ev 
    where c.company_id = ev.c_id 
    and ev.launch_year >  date_part('year', now()) 
    and c.company_name = '{company_name}'
    order by ev.launch_year;"""
    
    try:
        df = query_db(sql_company)
        st.dataframe(df)
    except:
        st.write(
                "Sorry! Something went wrong with your query, please try again."
        )


# Query Customer Service reservation Info
"## Select number of service reservations by a customer to show customer details"
sql_cust_names = "select distinct(name) from customer;"
try:
    assignments = st.slider('Select number of service reservations in respect to the customer.', 1, 4, 1)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if sql_ev_type:
    sql_service = f"""select c.name,c.email,c.city,count(*) reservation_count_total
                      from customer c,service_reservation s 
                      where c.customer_id = s.c_id
                      group by c.name,c.email,c.city 
                      having count(*) = '{assignments}';"""
    
    try:
        df = query_db(sql_service)
        st.dataframe(df)
    except:
        st.write(
                "Sorry! Something went wrong with your query, please try again."
        )


# Customer pair of cars
"## Display pairs of cars purchased by the selected customer"
sql_cust_pair_select = "select distinct(name) from customer;"
try:
    cust_names = query_db(sql_cust_pair_select)["name"].tolist()
    cust_name = st.selectbox("Please select a customer", cust_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if cust_name:
    sql_cust_name = f"""select temp1.item_name car1,temp2.item_name car2 
                    from (select * from Customer c, Customer_Sales s, vehicle_item v where c.customer_id = s.c_id and s.it_code = v.item_code) temp1, (select * from Customer c, Customer_Sales s, vehicle_item v where c.customer_id = s.c_id and s.it_code = v.item_code) temp2
                    where temp1.name = temp2.name
                    and temp1.item_name < temp2.item_name
                    and temp1.name = '{cust_name}'
                    order by car1,car2;"""
    try:
        df = query_db(sql_cust_name)
        st.dataframe(df)
    except:
        st.write(
                "Sorry! Something went wrong with your query, please try again."
        )

# Vendor Sold Vehicles
"## Display the vehicle item and its quantity sold by a given vendor"
sql_vendor_names = "select distinct(vendor_name) from vendor;"
try:
    vendor_names = query_db(sql_vendor_names)["vendor_name"].tolist()
    vendor_name = st.selectbox("Choose a vendor", vendor_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if cust_name:
    sql_vendor_name = f"""select v.vendor_name as vendor_name, vi.item_name as vehicle, sum(curr_stock) num_vehicle_sold
                        from Vendor v, vendor_transactions vt, vehicle_item vi
                        where vt.v_code = v.vendor_code
                        and vt.it_code = vi.item_code
                        group by v.vendor_name,vi.item_name
                        having v.vendor_name = '{vendor_name}';"""
    
    try:
        df = query_db(sql_vendor_name)
        st.dataframe(df)
    except:
        st.write(
                "Sorry! Something went wrong with your query, please try again."
                )
