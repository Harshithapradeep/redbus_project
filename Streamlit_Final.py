
#Styling and adding menu pages on side 
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import time
import pandas as pd
import pandasql as ps
import numpy as np
from sqlalchemy import create_engine,text
from urllib.parse import quote

#Function for establishing MYSQL connection 
def get_mysqldata(query):
    # Set database credentials.
    creds = {'usr': 'root',
                'pwd': quote('admin@123'),
                'hst': 'localhost',
                'prt': 3306,
                'dbn': 'redbus'}
    # MySQL conection string.
    connstr = 'mysql+mysqlconnector://{usr}:{pwd}@{hst}:{prt}/{dbn}'
    # Create sqlalchemy engine for MySQL connection.
    engine = create_engine(connstr.format(**creds))
    df = pd.read_sql(query, con=engine)

    return df


#Page layout set for wide
st.set_page_config(layout="wide")

#HTML script for image display in Home page 
html_string = """
<style>
    .background {
        position: relative;
        height: 60vh;
        background: url('https://s3.rdbuz.com/images/webplatform/india/HomeBannerNew.png') no-repeat center center;
        background-size: cover;
    }
    .header-text {
        position: absolute;
        top: 10%;
        left: 20%;
        transform: translate(-50%, -50%);
        color: white;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        text-align: lrft;
    }
    .paragraph-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: yellow;
        font-size: 1.5em;
        text-align: center;
    }
</style>
<div class="background">
    <div class="header-text">Redbus project 1.0</div>
</div>
"""

#Styling info----Sidebar menu 
with st.sidebar:
    selected=option_menu(
        menu_title="",
        options=['Homepage','APSRTC', 'ASTC', 'BSRTC', 'CTU RTC', 'HRTC','JKSRTC', 'KAAC', 'KSRTC_KERALA', 'KTCL', 'NBSTC', 'PEPSU', 'WBTC'],
        icons=["bus-front","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill","arrow-right-circle-fill",],
        default_index=0,
    )


#fetching data from sql database of red bus routes

df = get_mysqldata("""SELECT * FROM redbus.bus_routes WHERE departing_time is not null order by route_name""")

df = df.replace({np.nan: ''})

if selected=="Homepage":  
    st.markdown(html_string, unsafe_allow_html=True) 
    st.markdown(""":red[Thank you for choosing us!!]""")
    st.markdown(""":blue[Please click on the desired RTC to start your booking journey!!]""")
    

#Adding divider line -Streamlit styling option 
st.write('<style>div[data-baseweb="select"] > div { width: 400px; }</style>',unsafe_allow_html=True)



#Adding required filters for selecting Departure,Destination,seat type,actype,Star-rating,seat availability

def route_name_filter(df,rtc_name):
    df = ps.sqldf(f"SELECT * FROM df WHERE upper(rtc_name) = '{rtc_name}'")
    #adding specific size for select boxes --->contanier function for select drop down added
    with st.container():
        departure,col_spacer,destination,col_spacer,seattype=st.columns(spec=[5,0.2,5,0.2,5],gap="small", vertical_alignment="center") 
        actype,col_spacer,startingtime,col_spacer,starrating=st.columns(spec=[5,0.2,5,0.2,5],gap="small", vertical_alignment="center")
        Busfarerange,col_spacer=st.columns(spec=[2,0.2],gap="small", vertical_alignment="center")

    st.markdown(""":red[Finding available bus services as per your selection]""")
        
    #Styling streamlit function signature for selectbox added 
    st.write('<style>div[data-baseweb="select"] > div { width: 230px; }</style>',unsafe_allow_html=True)

    # departure_list
    departure_list = ['']
    dp_list = ps.sqldf("SELECT DISTINCT SUBSTRING(route_name, 1, INSTR(route_name,' to ')-1) as Departure FROM df ")
    departure_list += dp_list['Departure'].tolist()
    departure_list = sorted(departure_list)
    with departure :
        departure_option=st.selectbox("Select Departure", departure_list)
    
    # destination_list
    destination_list=['']
    dt_list = ps.sqldf("SELECT DISTINCT SUBSTRING(route_name, INSTR( route_name,' to ') + 4, LENGTH(route_name)) as Destination FROM df ")
    dt_list = dt_list['Destination'].tolist()
    destination_list += dt_list
    destination_list = sorted(destination_list)
    
    with destination:
        destination_option=st.selectbox("Select Destination", destination_list)
       

    #adding departure and destination to get route name
    route_name_clause = ''
    if departure_option and destination_option:
        route_name_clause = f"AND route_name = '{departure_option}'||' to '||'{destination_option}'"


    #add filter for seat_type_selection
    seat_type_list=['','Sleeper','Seater']
    with seattype :
        seat_type_option=st.selectbox("Seat type", seat_type_list)
    seat_type_clause=''
    if seat_type_option:
        seat_type_clause=f" AND bustype LIKE '%{seat_type_option}%'"
       

    #add filter for ac_type selection
    ac_type_list=['','AC','NON AC']
    with actype:
        ac_type_option=st.selectbox("AC type", ac_type_list)
    ac_type_clause=''
    if ac_type_option:
        if ac_type_option=='AC':
            ac_type_clause=f" AND (UPPER(bustype) like ('%AC%') OR UPPER(bustype) like ('%A%/C%')  OR UPPER(bustype) like ('%A.C%')) AND UPPER(bustype) NOT like ('%NON%A%C%')"
        elif ac_type_option=='NON AC':
            ac_type_clause=f" AND UPPER(bustype) like ('%NON%A%C%')"
            

    #adds filter for departing time 
    starting_time_list=['','Before 6am','6am to 12pm','12pm to 6pm','6pm to 11pm','after 11pm'] 
    with startingtime:
        starting_time_option=st.selectbox("Starting time",starting_time_list)
    starting_time_clause=''
    if starting_time_option:
        if starting_time_option == 'Before 6am':
            starting_time_clause= f" AND departing_time BETWEEN '01:00' AND '06:00'"   
        elif starting_time_option == '6am to 12pm':
            starting_time_clause = f" AND departing_time BETWEEN '06:00' AND '12:00'"
        elif starting_time_option == '12pm to 6pm':
            starting_time_clause = f" AND departing_time BETWEEN '12:00' AND '18:00'"
        elif starting_time_option == '6pm to 11pm':
            starting_time_clause = f" AND departing_time BETWEEN '18:00' AND '23:00'"
        elif starting_time_option == 'after 11pm':
            starting_time_clause = f" AND departing_time BETWEEN '23:00' AND '23:59' OR departing_time BETWEEN '00:00' AND '01:00'"

    #adds filter for star_rating
    star_rating_list=['','0-1','1-2','2-3','3-4','4-5']
    with starrating:
        star_rating_option=st.selectbox("Star rating", star_rating_list)
    star_rating_clause=''
    if star_rating_option:
        if star_rating_option == '0-1':
            star_rating_clause = f" AND star_rating BETWEEN 0 AND 1"
        elif star_rating_option == '1-2':
            star_rating_clause = f" AND star_rating BETWEEN 1 AND 2"
        elif star_rating_option == '2-3':
            star_rating_clause = f" AND star_rating BETWEEN 2 AND 3"
        elif star_rating_option == '3-4':
            star_rating_clause = f" AND star_rating BETWEEN 3 AND 4"
        elif star_rating_option == '4-5':
            star_rating_clause = f" AND star_rating BETWEEN 4 AND 5"

    # add busfare range slider for range of values 
    BusFare_range_list=['','0-500','500-1000','1000-2000','3000-4000','Others'] 
    with Busfarerange:
        BusFare_range_option = st.selectbox("Bus fare range", BusFare_range_list)
    BusFare_range_clause=''
    if BusFare_range_option:
        if BusFare_range_option == '0-500':
            BusFare_range_clause = f" AND price BETWEEN 0 AND 500"
        elif BusFare_range_option == '500-1000':
            BusFare_range_clause = f" AND price BETWEEN 500 AND 1000"
        elif BusFare_range_option == '1000-2000':
            BusFare_range_clause = f" AND price BETWEEN 1000 AND 2000"
        elif BusFare_range_option == '2000-3000':
            BusFare_range_clause = f" AND price BETWEEN 2000 AND 3000"
        elif BusFare_range_option == '3000-4000':
            BusFare_range_clause = f" AND price BETWEEN 3000 AND 4000"
        elif BusFare_range_option=='Others':
            BusFare_range_clause = f" AND price >4000"


    
#Select query to run all the filters in route_name_filter function
    query=f"SELECT * FROM df WHERE 1=1 {route_name_clause} {seat_type_clause} {ac_type_clause} {star_rating_clause} {BusFare_range_clause} {starting_time_clause}"
    # st.write(query)
    df=ps.sqldf(query,locals())

#Display message if no service available 
    if (len(df) == 0):
        st.write(f"No Routes Available for selected route")
    return df


#Getting the rtc_bus service names 
rtc_bus_list=['APSRTC', 'ASTC', 'BSRTC', 'CTU RTC', 'HRTC','JKSRTC', 'KAAC', 'KSRTC_KERALA', 'KTCL', 'NBSTC', 'PEPSU', 'WBTC']
if selected in (rtc_bus_list):
    st.subheader(f"{selected}", anchor=None,  help=None, divider="red")
    st.dataframe(route_name_filter(df,selected))
    
