import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import streamlit as st

def app():
    st.write('<p style="font-size:33px;"><b>Zip Code Statistics</b></p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px;">This section of the website is meant to show you some additional statistics about your recommended zip code. After typing in your zip code, you will see a drop down menu appear, which has different factors you can take a look at.</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px;"><b>Factors:</b></p>', unsafe_allow_html=True)
    st.write('<p style="font-size:15px;"><b>Climate:</b> Average temperature and precipitation for each month in 2022 <br> <b>Housing Prices:</b> The average housing prices from March 2021 to March 2023 <br><b>Diversity:</b> Distribution of each racial group <br><b>Population:</b> Total population and population density <br><b>Traveling:</b> Shows how convenient it is to travel via walking, biking, or transit <br><b>Map Location:</b> General location of zip code on the U.S. map', unsafe_allow_html=True)

    all_data = pd.read_csv('all_data.csv')
    all_data = all_data.drop(columns = 'Unnamed: 0')
    weather = pd.read_csv('weather.csv')
    w = weather.copy()
    w = w.drop(columns = 'Unnamed: 0')
    home_val = pd.read_csv('home_val.csv')
    location = pd.read_csv("location.csv")


    def zip_data(zipcode):
        zipdata = all_data[all_data['Zip'] == zipcode]
        zipcode = str(zipcode)
        
        w['Zip'] = w['Zip'].astype(str)
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
            
        w['july'] = w['July_Avg'].apply(weather_score)
        w['jan'] = w['Jan_Avg'].apply(weather_score)
        w['temp_score'] = w['july'] + w['jan']
        
        w['temp_label'] = w['temp_score'].apply(weather_label) ####
        
        w['yearly_prec'] = w[['Jan_prec', 'Feb_prec', 'March_prec',
           'April_prec', 'May_prec', 'June_prec', 'July_prec', 'Aug_prec',
           'Sept_prec', 'Oct_prec', 'Nov_prec', 'Dec_prec']].sum(axis = 1)/12
        w['yearly_prec'] = w['yearly_prec'].apply(prec)
        
        month_temp = w[list(w.columns[3:15])]
        month_temp['Zip'] = w['Zip']
        month_prec = w[list(w.columns[15:27])]
        month_prec['Zip'] = w['Zip']
        
        a = w[list(w.columns[3:15])]
        a['Zip'] = w['Zip']
        temp = a[a['Zip'] == zipcode].T.reset_index()[:-1].to_numpy()
        vals =[]
        for i in temp:
            vals.append(i[1])
            
        b = w[list(w.columns[15:27])]
        b['Zip'] = w['Zip']
        prec = b[b['Zip'] == zipcode].T.reset_index()[:-1].to_numpy()
        vals2 =[]
        for i in prec:
            vals2.append(i[1])
        
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
              'August', 'September', 'October', 'November', 'December']
        
        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Temperature (F)', color=color)
        ax1.plot(months, vals, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.tick_params(axis='x', rotation = 45)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('Precipitation (Inches)', color=color)  # we already handled the x-label with ax1
        ax2.plot(months,vals2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        st.pyplot(fig)
        
        #RACE
    def race(zipcode):
        zipdata = all_data[all_data['Zip'] == int(zipcode)]
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
        race_cols = ['% Race | White alone, 2021 [Estimated]','% Race | Black or African American alone, 2021 [Estimated]','% Race | American Indian and Alaska Native alone, 2021 [Estimated]',
                              '% Race | Asian alone, 2021 [Estimated]',
                              '% Race | Native Hawaiian and Other Pacific Islander alone, 2021 [Estimated]',
                              '% Race | Some other race alone, 2021 [Estimated]',
                              '% Race | Two or more races, 2021 [Estimated]']
        
        keys = ['White', 'Black or African American', 'American Indian/Alaska Native', 'Asian','Native Hawaiian/Other Pacific Islander', 'Other', 'Two or More races']
        values = np.array(zipdata[race_cols].iloc[0])
        labels= dict(zip(keys, values))

        labels = []
        for i in range(len(keys)):
            labels.append(keys[i] + ' (' + str(values[i]) + '%)')

            

        # plt.subplot(1, 2, 2)
        patches, texts = plt.pie(np.array(zipdata[race_cols].iloc[0]), startangle=90)
        plt.legend(patches,labels, bbox_to_anchor=(0.3,0,1,1), loc="lower right", fontsize=11, 
                   bbox_transform=plt.gcf().transFigure)
        
        plt.tight_layout()
        st.pyplot(plt)
        
        races = zipdata[race_cols]
        zipdata['diversity'] = (races.applymap(race).sum(axis =1)/39) # max score overall
        
        print("Diversity Score: " +  str(zipdata['diversity'].iloc[0]))
    
    def price(zipcode):
        vals = home_val.copy()
        
        vals = vals.drop(columns = {'Unnamed: 0', 'State', 'City', 'CountyName'})
        data = vals[vals['Zip'] == int(zipcode)][list(vals.columns[-25:])]
        data = data.T.reset_index()
        data.columns= ['Date','Price']

        sns.scatterplot(data=data,x="Date", y="Price", color = 'purple')
        plt.xticks(rotation=90)
        plt.ticklabel_format(style='plain', axis='y')
        st.pyplot(plt)
    def travel(zipcode):
        zipdata = all_data[all_data['Zip'] == int(zipcode)]
        zipcode = str(zipcode)
        return "TRAVEL SCORES (OUT OF 100):" + "\n" + '\nWalk Score: ' + str(zipdata['Walk'].iloc[0]) + "\n"+'\nTransit Score: ' + str(zipdata['Transit'].iloc[0]) + "\n"+'\nBike Score: ' + str(zipdata['Bike'].iloc[0])
    
    def climate(zipcode):
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
            
        w['july'] = w['July_Avg'].apply(weather_score)
        w['jan'] = w['Jan_Avg'].apply(weather_score)
        w['temp_score'] = w['july'] + w['jan']
        
        w['temp_label'] = w['temp_score'].apply(weather_label) ####
        
        w['yearly_prec'] = w[['Jan_prec', 'Feb_prec', 'March_prec',
           'April_prec', 'May_prec', 'June_prec', 'July_prec', 'Aug_prec',
           'Sept_prec', 'Oct_prec', 'Nov_prec', 'Dec_prec']].sum(axis = 1)/12
        w['yearly_prec'] = w['yearly_prec'].apply(prec)
        
        if w[w['Zip'] == int(zipcode)].shape[0] == 0:
            return 0
        return "Climate: " + w[w['Zip'] == int(zipcode)]['temp_label'].iloc[0].title() + "\n " + "\nPrecipitation: " + w[w['Zip'] == int(zipcode)]['yearly_prec'].iloc[0].title()

    def pop(zipcode):
        zipdata = all_data[all_data['Zip'] == int(zipcode)]
        zipcode = str(zipcode)
        return 'Population: ' + str(zipdata["population"].iloc[0]) + "\n " + "\nPopulation Density: " + str(zipdata["pop_density"].iloc[0])

    z = st.text_input('Type in a Zip Code to see the stats!')
    
    if len(z) >=1:
        if int(z) not in list(all_data["Zip"]):
            out = "This Zipcode has no data!"
            st.write(out)
        else:
            stat = st.selectbox("",["Choose a Factor","Climate", "Housing Prices","Diversity", "Population", "Traveling",  "Map Location"])
            if "Housing Prices" == stat:
                out = price(z)
            if "Diversity" == stat:
                out = race(z)
            if "Climate" == stat:
                out2 = climate(z)
                if out2 == 0:
                    st.write("This zip code has no climate data!")
                else:
                    st.write(out2)
                    out = zip_data(z)
            if "Population" == stat:
                output = pop(z)
                st.write(output)
            if "Traveling" == stat:
                out = travel(z)
                st.write(out)
            if "Map Location" == stat:
                if len(z) >1:
                    st.map(location[location['ZIP'] == int(z)])
                else: 
                    st.map(location)



