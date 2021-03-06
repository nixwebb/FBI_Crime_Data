# -*- coding: utf-8 -*-
"""Hackathon2020_FBICrimeData_Tutorial.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A7M0AZg13WiXy5A8tcgnFwiBUALFfIWi

# Working with FBI crime data: 2014 - 2018

## Nick Webb (webbn@union.edu) / March, 2020
## HACKATHON Tutorial

In this Jupyter notebook we are going to explore elements of the FBI crime data for the years 2014 - 2018. We have chosen to focus on crimes committed on University and College campuses.

All data was obtained from: https://ucr.fbi.gov/crime-in-the-u.s/

## Data Analysis of Crimes at Colleges and Universities

We're using the following libraries in Python:
- pandas (for data manipulation): https://pandas.pydata.org/
- matplotlib (for plotting): https://matplotlib.org/
- scikit learn (for regression): https://scikit-learn.org/stable/
- plotly (for graphing US states): https://plot.ly/python/

The whole document is a Jupyter notebook: https://jupyter.org/

Jupyter is a browser based interactive environment for coding. In this case we are using Python 3.

Any cell marked with a number, such as:
- [1]

represents a cell of Python code. You can hit the run button next to the box, and it will execute the code, showing the output in the following cell.

Any cell marked
- [->

represents the output of the previous cell, including graphs, tables and basic output.

##2014 Data Analysis

We start with just the crime data for 2014.

I've uploaded the FBI crime data to my github repository directory as a CSV file. Below we load it directly from that repository, using the Pandas data library.

We then show some basic details, and display the first 5 records in the data.
"""

# Import our python libraries
# Pandas is good for data manipulation
# Matplotlib is one of the graphing options we'll use later

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title('Interactive FBI Crime Data')
st.header('Nick Webb: webbn@union.edu')
st.write("In this dashboard, we're going to load and analyze crime data from the FBI for US colleges and universities. All data was obtained from: https://ucr.fbi.gov/crime-in-the-u.s/")

# Read the 2014 data from a CSV stored in a github repository
# and store it in a variable called df_2014
# This stores the information as a DATAFRAME, a data type used by Pandas
# We can use the head() method to take a look at the first 5 rows of
# the dataframe

st.subheader("Loading the data")

year = st.radio("Pick a year:", ('2014','2015','2016','2017','2018'))

filename = "https://raw.githubusercontent.com/nixwebb/Hackathon2020/e464544c903484a9f701f753f90a3604bfa24f82/Data/"+year+"_Crime.csv"

df_data = pd.read_csv(filename)

st.write("Showing the first 5 entries of the year "+year+" as a dataframe")

st.write(df_data.head())

r, c = df_data.shape
st.write('There are',r,'rows and',c,'columns in this data')

st.write("Take a look at the dataframe displayed above. You can scroll to the right, to see the remaining columns. The information presented contains a row for each school in the data, so there are",r,"here. There are ",c,"columns (or features), including the state, the name of the university or college, the student enrollment at that school, and then numbers of different types of crimes for the year", year)


st.subheader("Understanding the data")

st.write("""Let's understand the data a little more. There are""",c,"""columns. Some of these represent:

- ***state***: The state the school is located in
- ***university/college***: The name of the school
- ***campus***: Some colleges have more than one campus. The default is the same as the name of the school, plus the word main.
- ***student_enrollment***: The number of students enrolled at that campus
- ***violent_crime***: The number of violent crimes that were reported at that campus. This is loosely the sum of the next three columns, although there are some additional crimes not included here. The next three columns are TYPES of violent crimes:
-- ***murder_and_nonnegligent_manslaughter***
-- ***robbery***
-- ***aggravated_assault***
- ***property_crime***: The number of crimes against property. This is the sum of the next four columns. Those next four columns are types of property crimes:
-- ***burgalry***
-- ***larceny_theft***
-- ***motor_vehicle_theft***
-- ***arson***""")


# We can also use the describe() method to get some details about the data
# This will include the overall count of entries, the mean, the min and the max values for each column

text = 'Basic Data Descriptions: '+year

st.subheader(text)


st.write("Now we have some data, let's take a look at some statistics. Showing some basic descriptive statistics for the year "+year+" including counts, medians and means.")

st.write(df_data.describe())


st.write("Next, we'll compute the total number of violent crimes in the data, and the total in NY state for the year",year)

# # Compute amount of violent crimes nationwide, and for NYS
# # The number of violent crimes is stored in the column labelled 'violent_crime'
# # I can access that column by using the header as a value, and then calling the sum()
# # method


violent_total_year = df_data['violent_crime'].sum()
st.write('Violent Crime Total ('+year+'):',violent_total_year)


states = pd.read_csv('https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv')
states['State'] = states['State'].str.upper()

listOfStates = list(set(states['State'].tolist()))
#listOfStates = [n for n in listOfStates if n.isalpha()]
listOfStates.sort()

text = 'Crime per state: '+year

st.subheader(text)

st.write("We can do the same thing, but this time ONLY selecting the numbers from the 'violent_crime' column for a chosen state")

#state = st.selectbox('Choose a state', ("NEW YORK", "CALIFORNIA", "TEXAS"))
state = st.selectbox('Choose a state', listOfStates)


state_violent_total_year = df_data.loc[df_data['state'] == state, 'violent_crime'].sum()
st.write(state,'Violent Crime Total ('+year+'):',state_violent_total_year)

# """I want to add a new column (a new variable) that's going to be useful for us later when we want to graph the output. I'm going to add a column representing the state abbreviation for each state (so NEW YORK will have an additional entry, NY).

# To do that I'm going to use another CSV file, that contains the names of states, and their abbreviations. Let's take a look at it:
# """



# states.head()

# """I'm going to use this information to add a new column into my df_2014 dataframe. That column will be called 'abv', and will appear at the end of my dataframe - all the way to the right.

# I'm mapping from the 'state' name in my dataframe, to the corresponding 'State' column in the dataframe above, and then selecting the appropriate value from the 'Abbreviation' column.

# Once complete, I'll again look at the head of my df_2014 dataframe to make sure it added the new column.
# """

df_data['abv'] = df_data['state'].map(states.set_index('State')['Abbreviation'])
# df_2014.head()

# """We're going to start with overall summaries by state.

# We're going to use our new 'abv' column as a way of GROUPING the data frame. There is the groupby() method (the name we give a function that applies to a particular kind of data). We're going to group the data using that abbreviation column.

# What that means is that it will compile the data for us using the abrreviation as a key for the data. I'm then going to get a description of the first five rows...again, giving stats like the max value, the min and the standard deviation.

# Once we've done that, I'm going to create a new dataframe that extracts, from the grouped data, the SUM of the various columns, so we can see how many of each crime occured in each state.
# """

# # Grouping the values by state abbreviation
# # Showing the descriptions of the first five rows

text = 'Summary of crimes by state for '+year

st.subheader(text)

crime_df_year = df_data.groupby('abv')
#st.write(crime_df_year.describe().head())

# # Creating a new dataframe that is summing the values for each entry by state

sum_by_year = crime_df_year.sum()
st.write(sum_by_year)

# """Let's plot these values on a map. We can use the graphing library plotly, which allows us to access a map of the United States. As our dataframe above, sum_by_year already has the state abbreviation as the index, we can pass that to the map, along with the corresponding values from the 'violent_crime' column."""

# # Import the plotly graphing library


import plotly.express as px

# # Use their choropleth function to plot values on a map
# # The locations are stored in the index of the dataframe sum_by_year_2014 (see above).
# # The values are the contents of the 'violent_crime' column, given above.

#@st.cache(hash_funcs={_plot_to_url_or_load_cached_url})


text = 'Graph of crimes by state for '+year

st.subheader(text)

titletext = 'Violent Crime / Colleges and Universities / '+year


#import streamlit as st
import plotly.express as px

#df = px.data.election()
#geojson = px.data.election_geojson()

#fig = px.choropleth(df, geojson=geojson, color="Bergeron",
#                    locations="district", featureidkey="properties.district",
#                    projection="mercator"
#                   )
#fig.update_geos(fitbounds="locations", visible=False)
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#st.plotly_chart(fig)


fig = px.choropleth(locations=sum_by_year.index, locationmode="USA-states", color=sum_by_year['violent_crime'], scope="usa",color_continuous_scale='Reds')
fig.update_layout(title=titletext,title_x=0.5)
st.plotly_chart(fig)

st.write("""So clearly, California and Texas are dangerous states to go to school in.

 But is there a problem with this interpretation?

 """)

# # Let's factor in the number of students

text = 'Summary of crimes by state / per 1000 students / '+year

st.subheader(text)

sum_by_year['violent_crime_per_1000'] = (sum_by_year['violent_crime'] / (sum_by_year['student_enrollment'] / 1000) )
#sum_by_year_2014.head()

# # And now let's graph THOSE results - using our new 'violent_crime_per_1000' column

titletext = 'Violent Crime per 1000 students / Colleges and Universities / '+year

fig = px.choropleth(locations=sum_by_year.index, locationmode="USA-states", color=sum_by_year['violent_crime_per_1000'], scope="usa",color_continuous_scale='Reds')
fig.update_layout(title=titletext,title_x=0.5)
# fig.show()
st.plotly_chart(fig)


# """So now we get a better sense of what's going on, given student population. California isn't so bad. New York looks ok too.

# Let's add that column into our main source dataframe (df_2014) because I think it will be useful.

text = "Comparing school size / "+year

st.subheader(text)



# Ok, what if we look to see if there's a difference between schools of different sizes of student populations.

# A histogram is a good way to see that distributution of values across a variable.
# """

fig, ax = plt.subplots()
ax.hist(df_data['student_enrollment'])

# # Let's generate a histogram
#test = df_data.hist(column='student_enrollment')
st.pyplot(fig)

st.write("""We can see that a large number of schools seem to have under 5000 students. In education,
we often think of small schools as those having less than 2500 students. We'll partition the data using this idea, and show summary median statistics for small schools (True) vs. large schools (False)""")

# # Add the small_school column to my data, based on the school size of 2500

df_data['small_school'] = df_data['student_enrollment'] < 2500
#df_2014.head()

# """Now, just like above when we grouped by state, this time we'll group the original data frame (df_2014) by this small school column."""

school_type_df = df_data.groupby('small_school')
# school_type_df.describe().head()

# """Now we'll output some descriptive statistics. We could use MEAN, but we'll use MEDIAN instead. Why? There's a relatively small number of schools here, and MEANS scores can often be very skewed by one or two very high values. MEDIAN gives us the central tendency instead, and can be more informative. """

school_type_sum = school_type_df.median()
#st.write(school_type_sum)

# """We can see from the dataframe above that the median number of violent crimes for large schools is 3, and for small schools it's 0. Just to check, let's add back in the student enrollment numbers, below:"""

# # Let's add that violent_crime_per_1000 column into our dataframe.
school_type_sum['violent_crime_per_1000'] = (school_type_sum['violent_crime'] / (school_type_sum['student_enrollment'] / 1000) )
st.write(school_type_sum)

st.write("""So here's what we've shown so far: New York is a pretty safe state for students, and small schools are very safe for students. THEREFORE, we have shown that small schools in NY are the best.""")

st.subheader('Law Enforcement at Colleges and Universities Data')

st.write("There are other tables in the data, detailing the number of law enforcement employees at Universities and Colleges. We read in this data, and perform the same data formatting as the crime statistics data.")

# # Load in the Law Enforcement Employee (LEE) data for 2014
file = 'https://raw.githubusercontent.com/nixwebb/Hackathon2020/master/Data/'+year+'_LawEnforcement.csv'
lee_data = pd.read_csv(file)


# # Get some details about how much data there is
r, c = lee_data.shape
st.write('There are',r,'rows and',c,'columns in this data')


# # Show results
# lee_2014.head()

st.write("Note that there aren't the same number of rows in this data as there are in the crime data, indicating a data sparsity issue. \
We're going to add in a new column that represents the number of law enforcement employees per 1000 students.")

lee_data['employees_per_1000'] =  (lee_data['total_law_enforcement__employees'] / (lee_data['student_enrollment'] / 1000) )
st.write(lee_data.head())

st.write("Next let's merge our two data frames. Once contains information on the number of crimes occuring at University and College campuses, the other contains the numbers and types of law enforcement employees at those campuses.")

# # I'm going to use PANDAS to merge the two dataframes - our df_2014 dataframe of crimes
# # and our lee_2014 dataframe of law enforcement employees
# # At the end of the resulting new dataframs (allData_2014), you should now see the columns from the lee_2014 data

df_data['violent_crime_per_1000'] = (df_data['violent_crime'] / (df_data['student_enrollment'] / 1000) )
allData = pd.merge(df_data,lee_data, left_on='campus', right_on='campus')
st.write(allData.head())

# # AND let's get a description of the data. Never a bad idea.
st.write(allData.describe())

st.write("""A scatter plot helps to understand relationships between variables - columns in our data frame. Here's I'm going to plot the relationship between violent_crime_per_1000 students, and employees_per_1000 students""")

fig = px.scatter(allData, x='violent_crime_per_1000', y='employees_per_1000')
st.plotly_chart(fig)
# fig.show()

st.write("You can explore the data points above by hovering over them. \
It looks like there's some sort of weak relationship between the two variables. Let's investigate that, using linear regression.")

# ### Learning relationships

st.subheader("Correlation between law enforcement, and number of violent crimes")

st.write("Up to now we haven't performed any specific predictive analytics. \
I'm going to run a baseline machine learning classifier (ZeroR) on the number of crimes \
(our x value) to see if we can 'predict' the number of employees per 1000 people (our y value). \
ZeroR is a very simple classifier, it simply takes the mean of the number of employees across the data, and predicts that value uniformly. \
To attempt to improve on that, I'm using a linear regression model. Both results are presented as \
RMSE (Root Mean Squared Error), and plotting the lines of best fit. In this instance, the RMSE represents the average number of employees off from the correct \
number of employees our model predicts, so a lower value is better")
# """

# # Import libraries to help
# # These include the scikit-learn machine learning library
# # and the math library

from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import mean_squared_error
import math


# # Create a copy of the columns from our dataframe that I want (effectively creating a smaller dataframe)
# # I also need to drop some problematic values - those that are undefined in the original data

df = allData[['violent_crime_per_1000','employees_per_1000']].copy()
df.dropna(inplace=True)


# # I then extract the values from the dataframe, using a mechanism called slicing

array = df.values
X = array[:,0:1]
y = array[:,1]

# # I create my baseline dummy classifier, called zr (for zeroR)

zR = DummyClassifier(strategy="most_frequent")
zeroR = zR.fit(X,y)
zr_predY = zeroR.predict(X)

# # I then create a linear regression classifier

lr = LinearRegression()
reg = lr.fit(X,y)
predY = reg.predict(X)


# # I can computer the error of both. LOWER values of RMSE are better

lr_rmse = math.sqrt(mean_squared_error(y,predY))
zr_rmse = math.sqrt(mean_squared_error(y,zr_predY))


st.write('Regression RMSE:',round(lr_rmse,2))
st.write('ZeroR RMSE:',round(zr_rmse,2))


# # Then I'm going to plot the lines on the graph.
# # Hopefully one of the lines fits the data better than the other


fig, ax = plt.subplots()
ax.plot(X, y,'b^')
ax.plot(X, predY, 'r',label='Linear Regression')
ax.plot(X, zr_predY, 'g',label='ZeroR Baseline')
#ax.set_title('Relationship between law enforcement employes versus violent crime, per 1000 students')
ax.set_xlabel('Violent Crimes, per 1000 students')
ax.set_ylabel('Law Enforcement Employees, per 1000 students')
fig.legend()
st.pyplot(fig)
#plt.show()

st.write("""As the last thing in this tutorial, we're going to focus on individual state data. First, we select a state, and then show how much data that leaves us with.""")

# # Let's focus on NYS for now.
# # Create a new dataframe with just NY data


#state = st.selectbox('Choose a state', ("NEW YORK", "CALIFORNIA", "TEXAS"))
stateInfo = st.selectbox('Choose a state of interest', listOfStates)

state_df = df_data.loc[df_data['state'] == stateInfo].copy()
st.write(state_df.head())

# # See how much data that leaves us with

r, c = state_df.shape
st.write('There are',r,'rows and',c,'columns in this data')

st.write("We have extracted",r,"rows of",stateInfo,"data - i.e. there are",r,"schools in this data")

st.write("Let's add the column, which represents the number of violent crimes per 1000 registered students at each college. \
We also going to calculate the mean, median, min and max values for this new column, and find the entry with the maximum value.")


st.write("It's worth remembering that because violent crime is so rare, small increases cause significant impact. Certain schools will have \
 a high proportion there may be a small number of violent crimes, but with an equally small population")

# At the end of this section, we'll graph the proportion of crimes per 1000 students across the 2014 NY state data
# """

# # Add a new column to our dataframe, that calculates the number
# # of violent crimes per 1000 student enrollments for just this NYS data

state_df['violent_crime_per_1000'] =  (state_df['violent_crime'] / (state_df['student_enrollment'] / 1000) )
#st.write(state_df.head())

# # Let's find the mean and the median values for crime in NYS
# # And then show the college campus that had the highest value of crime
# # per 1000 students in the state

mean_vcp_2014 = round(state_df['violent_crime_per_1000'].mean(),2)
median_vcp_2014 = round(state_df['violent_crime_per_1000'].median(),2)


st.write('For',stateInfo,'mean average crime per 1000 is',mean_vcp_2014,'( median:',median_vcp_2014,')')
st.write('The entry with highest violent crime per 1000 people is:\n\n',state_df.loc[state_df['violent_crime_per_1000'].idxmax()])

# # And finally let's plot the results




#st.bar_chart()


#import numpy as np
#labels = np.arange(len(state_df['campus']))
#fig, ax = plt.subplots()
#ax.bar(x = state_df['campus'], y = state_df['violent_crime_per_1000'].tolist(), rot=0)
#ax.bar(labels, y = state_df['violent_crime_per_1000'].tolist(), rot=0)
#ax.axhline(y=mean_vcp_2014,linewidth=1, color='k', linestyle='--')
#ax.set_xticks(rotation=90)

# # Let's generate a histogram
#test = df_data.hist(column='student_enrollment')
#st.pyplot(fig)



# state_df.plot.bar(x='campus', y='violent_crime_per_1000', rot=0,figsize=(15,10)))
# plt.title('Violent Crime per 1000 students, 2014')
# plt.axhline(y=mean_vcp_2014,linewidth=1, color='k', linestyle='--')
# plt.xticks(rotation=90)
# plt.show()

# """## Questions

# Now it's your turn. There's lots of things that you can do, with some suggestions below:

# - On my github page, where I download the crime and the law enforcement data, there is also data for the years 2015, 2016, 2017 and 2018. You could choose to look at one or more of these years, and compare the results to 2014

# - You could choose to look at other crimes, not the violent crimes I decided to look at. For instance you could look at property crime, or different categories of the crimes, as given above

# - You could look at other states, instead of NY.
# """
