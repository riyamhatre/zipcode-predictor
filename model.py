import pandas as pd
import numpy as np
import math
import streamlit as st
def app():
    st.write('<p style="font-size:33px;"><b>Zip Code Recommendation System</b></p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px;">Welcome! This website is meant to find an ideal zip code in the U.S for you to live in based on your criteria. After answering all the questions on this page and hitting the "Submit" button at the bottom, you can head to the Zip Code Statistics tab on the left to see some relevant data about your recommended zip code. </p>', unsafe_allow_html=True)
    #st.header('Enter your criteria in order')
    all_data = pd.read_csv('all_data.csv')
    all_data = all_data.drop(columns = 'Unnamed: 0')
    weather = pd.read_csv('weather.csv')
    w = weather.copy()
    w = w.drop(columns = 'Unnamed: 0')
    home_val = pd.read_csv('home_val.csv')
    location = pd.read_csv("location.csv")
    def price_city(city, state):
        all_data['state'] = all_data['state'].str.upper()
        all_data['city'] = all_data['city'].str.upper()

        city = city.upper()
        state = state.upper()

        g_latest_date = '2022-12-31'
        c = all_data[(all_data['city'] == city) & (all_data['state'] == state)]
        
        if c.shape[0] == 0:
            return 0
        if  home_val[(home_val['city'] == city) & (home_val['state'] == state)].shape[0] == 0:
            return 0
        mini = c[g_latest_date].min()
        digits = len(str(int(mini))) -2 
        lower_bound = math.floor(int(mini)/int('1'+''.zfill(digits)))*10**digits
        
        maxi = c[g_latest_date].max()
        digit = len(str(int(maxi))) -2 
        upper_bound = math.floor(int(maxi)/int('1'+''.zfill(digit)))*10**digit
        
        price_range = []
        for i in range(lower_bound, upper_bound +10**digit,10**digit ):
            price_range.append(i)
        price_range.append(i+10**digit)
        return price_range
    def weather_stats(state):
        state = state.upper()
        def weather_score(x):
            if x < 25:
                return 0
            if x >= 25 and x < 43:
                return 1
            if x >= 43 and x < 58:
                return 2
            if x >= 58 and x <= 79: 
                return 3
            if x > 79:
                return 4
            
        def weather_label(x):
            if x == 1 or x == 2: 
                return 'cold'
            if x == 3 or x == 4: 
                return 'cool'
            if x == 5: 
                return 'moderate'
            if x ==6:
                return 'warm'
            if x ==7:
                return 'hot'
            
        def prec(x):
            if x < 1: # very dry
                return 'very dry'
            if x >=1 and x< 6: # dry
                return 'dry'
            if x>= 6 and x < 12: # moderate precipitation
                return 'moderate precipitation'
            if x >=12: # heavy precipitation
                return 'heavy precipitation'
            
        w['state'] = w['state'].str.upper()
            
        w['july'] = w['July_Avg'].apply(weather_score)
        w['jan'] = w['Jan_Avg'].apply(weather_score)
        w['temp_score'] = w['july'] + w['jan']
        
        w['temp_label'] = w['temp_score'].apply(weather_label) ####
        
        w['yearly_prec'] = w[['Jan_prec', 'Feb_prec', 'March_prec',
           'April_prec', 'May_prec', 'June_prec', 'July_prec', 'Aug_prec',
           'Sept_prec', 'Oct_prec', 'Nov_prec', 'Dec_prec']].sum(axis = 1)/12
        
        w['yearly_prec'] = w['yearly_prec'].apply(prec)
        
        location = w[w['state'] == state]
        return list(location['temp_label'].unique()), list(location['yearly_prec'].unique()), location

    def factors(city, state, factor, weight, lower,upper, temperature, precipitation): #weight stuff 
        all_data['state'] = all_data['state'].str.upper()
        all_data['city'] = all_data['city'].str.upper()
        
        city = city.upper()
        state = state.upper()
        
        g_latest_date = '2022-12-31'
    # diversity helper
        def race(x):
            if x <= 5:
                return 1
            elif x > 5 and x < 10:
                return 3
            elif x >10 and x <= 27:
                return 7
            elif x > 27 and x <= 35:
                return 6
            elif x>35 and x <= 45:
                return 5
            elif x > 45 and x < 60:
                return 4
            elif x >=60 and x < 75:
                return 3
            elif x >=75 and x < 85:
                return 2
            else:
                return 1

        # house price calculation  
        def house_by_price(city, state, lower,upper):
            c = all_data[(all_data['city'] == city) & (all_data['state'] == state)]
            data = c[['Zip',g_latest_date]].sort_values(by = g_latest_date)
            price_list = pd.DataFrame()
            for i in data[g_latest_date]:
                if i >= lower and i <= upper:
                    a = data.loc[data[g_latest_date] == i]
                    price_list = pd.concat([price_list,a])
            temp = pd.DataFrame()
            b = price_list['Zip'].to_list()
            for i in b:
                f = all_data[all_data['Zip'] == i]
                temp = pd.concat([temp, f])
            return temp
        filtered = house_by_price(city, state, lower,upper).set_index('Zip') ###
        storage = pd.DataFrame()

        ####checking factors
        # age
        if 'retirement' in factor[0] or 'young_people' in factor[0] or 'families' in factor[0]: #age group options young, retirement
            temp = pd.DataFrame()
            temp['families'] = filtered[['% Age | Under 5 years, 2021 [Estimated]','% Age | 5 to 9 years, 2021 [Estimated]','% Age | 10 to 14 years, 2021 [Estimated]','% Age | 15 to 17 years, 2021 [Estimated]','% Age | 35 to 44 years, 2021 [Estimated]','% Age | 45 to 54 years, 2021 [Estimated]']].sum(axis =1)
            temp['young_people'] = filtered[['% Age | 18 and 19 years, 2021 [Estimated]','% Age | 20 to 24 years, 2021 [Estimated]','% Age | 25 to 34 years, 2021 [Estimated]']].sum(axis = 1)
            temp['retirement'] = filtered[['% Age | 55 to 64 years, 2021 [Estimated]','% Age | 65 to 74 years, 2021 [Estimated]','% Age | 75 to 84 years, 2021 [Estimated]','% Age | 85 years and over, 2021 [Estimated]']].sum(axis = 1)
            age_score = []
            for i in range(temp.shape[0]): #temp stores frequency of each category
                if temp.iloc[i][-1] > 30: #retirement
                    age_score.append(1)
                elif temp.iloc[i][0] > temp.iloc[i][1]: #families
                    age_score.append(0)
                elif temp.iloc[i][0] < temp.iloc[i][1]: #young people
                    age_score.append(-1)
                else:
                    age_score.append(-1)
            temp['age'] = age_score
            #temp['Zip'] = filtered['Zip']
            category = []
            if 'retirement' in factor[0]:
                category.append(1)
            if 'young_people' in factor[0]:
                category.append(0)
            if 'families' in factor[0]:
                category.append(-1)
            ages_temp = pd.DataFrame()
            #ages_temp['Zip'] = filtered['Zip'] 
            for i in category:
                ages_temp = temp[temp['age'] == i]
                storage = pd.concat([storage, ages_temp])
            storage = storage[['age']]

        # travel
        storage['travel_score'] = filtered['score']/100


        #diversity score 
        races = filtered[['% Race | White alone, 2021 [Estimated]','% Race | Black or African American alone, 2021 [Estimated]','% Race | American Indian and Alaska Native alone, 2021 [Estimated]',
                              '% Race | Asian alone, 2021 [Estimated]',
                              '% Race | Native Hawaiian and Other Pacific Islander alone, 2021 [Estimated]',
                              '% Race | Some other race alone, 2021 [Estimated]',
                              '% Race | Two or more races, 2021 [Estimated]']]
        storage['diversity'] = (races.applymap(race).sum(axis =1)/39) # max score overall
        # are you particular about living in a highly diverse area? 

        #population 1-low, 2-medium, 3-high
        storage['population'] = filtered['pop_density']
        
        temp_conditions = pd.DataFrame()
        location = weather_stats(state.upper())[2]
        for i in temperature:
            l = location[location['temp_label'] == i]
            temp_conditions = pd.concat([temp_conditions, l])
        
        
        storage['Rank'] = (storage['travel_score'] * weight[0] +
                     storage['population'] * weight[1] + storage['diversity'] * weight[2]).rank().astype('int64')
        output = pd.merge(storage.reset_index(), temp_conditions)
        
        output_table = output.merge(all_data[['Zip','city']], how = 'left', on = 'Zip')
        output_table['state'] = output_table['state'].str.title()
        output_table['city'] = output_table['city'].str.title()

        zips = list(output_table.sort_values(by = 'Rank')["Zip"])
        if len(zips) == 0:
            return "Sorry! There are no zip codes that fit these criteria!" + '<br>' + "Try keeping a wider range and adding more criteria"
        if len(zips) == 1:
            return "Recommended Zip Code: " + str(zips[0])
        if len(zips) > 1 and len(zips) <=3:
            return "Recommended Zip Code: " + str(zips[0]) +'<br>' + "Other Zip Codes to look into: " + str(zips[1:])
        if len(zips) > 3: 
            return "Recommended Zip Code: " + str(zips[0]) +'<br>' +"Other Zip Codes to look into: " + str(zips[1:4])

    state_names =  ["Select a State","Alabama","Alaska","Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana","Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland","Massachusetts","Michigan", "Minnesota","Mississippi", "Missouri", "Montana","Nebraska", "Nevada","New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania","Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont","Virginia","Washington","West Virginia", "Wisconsin", "Wyoming"]
    city = st.text_input('Enter a city (Required)')
    state = st.selectbox('Enter a state (Required)', state_names)
    if len(city) >1 and state != "Select a State": 
        l = price_city(city, state)
        if l == 0:
            st.write("Choose a state that has that city!")
            return
        lower_bound = st.selectbox('Price (Lower Bound)',l)
        limit = l.index(lower_bound) + 1
        upper_bound = st.selectbox('Price (Upper Bound)',l[limit:])
    factor_1 = st.multiselect('Age Demographic (can choose multiple):', ['young_people','retirement', 'families'])
    travel_weight = st.slider('How important is walkability to you?', 0.0, 100.0)
    pop_weight = st.slider('Do you prefer low population density or high? (-1 is low, 1 is high)', -1.0,1.0)
    diversity_weight = st.slider('How important diversity is to you', 0.0, 100.0)
    if True: 
        options = weather_stats
        temperature = st.multiselect('What type of climate do you prefer (can choose multiple)', weather_stats(state.upper())[0])
        precipitation = st.multiselect('What type of environment do you prefer (can choose multiple)', weather_stats(state.upper())[1])


    if st.button('Submit'):
        if len(factor_1) == 0:
            factor_1 = ['young_people','retirement', 'families']
        if len(temperature) == 0:
            temperature = ['cold','cool','moderate','warm','hot']
        if len(precipitation) == 0:
            precipitation = ['very dry','dry','moderate precipitation', 'heavy precipitation']
        if len(city) ==0:
            st.write("Enter a valid city")
            return
        price = factors(city, state, [factor_1],[travel_weight,pop_weight,diversity_weight], lower_bound, upper_bound, temperature, precipitation)
        st.write(price,unsafe_allow_html=True)
