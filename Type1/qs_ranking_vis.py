import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
from dataclasses import field
import datetime
from matplotlib.colors import ListedColormap
plt.rcParams['axes.edgecolor']='#FA6E4F'
plt.rcParams['font.family'] = 'monospace'
import re
from vega_datasets import data

# Author: Dragon Xu
# Description: This is a Streamlit app that visualizes the QS World University Rankings data.
# The app allows users to filter the data by year, university type, university size, and region.


# page setup
st.set_page_config(
    layout="wide"
)
# Read in the data from csv file
qs_data = pd.read_csv("https://raw.githubusercontent.com/CristoDragon/CSE5544-Lab3/main/QS_ranking.csv", encoding='ISO-8859-1')
# Drop rows with more than 4 missing values
# Reference: https://www.kaggle.com/code/padhmam/qs-world-university-rankings-eda-visualization
drop_index = qs_data[qs_data.isnull().sum(axis=1) > 4].index.tolist()
qs_data.drop(drop_index, inplace=True)
# Drop the socre column since it contains too many missing values
# qs_data.drop(['score'], axis=1, inplace=True)
# Convert these columns to numerical and remove all special characters
qs_data['research_output'] = qs_data['research_output'].replace('Very high', 'Very High')
qs_data['international_students'] = qs_data['international_students'].apply(lambda x: float(str(x).replace(',','')))
qs_data['faculty_count'] = qs_data['faculty_count'].apply(lambda x: float(str(x).replace(',','')))
qs_data['rank_display'] = qs_data['rank_display'].apply(lambda x: float(re.sub(r'\W+', '', str(x))))



# Create interface
st.markdown("<div style='background:#e6e6e6'><h3 style='font-weight:bold; color:#ac2217'>QS Ranking Dashboard</h3></div>", unsafe_allow_html=True)
#st.dataframe(qs_data.head(5))

# Create the first panel 
panel1 = st.container()
with panel1:
    # Create 3 widgets to change conditions to filter data
    columns = st.columns([1.6, 0.3, 2.6, 0.3, 2.1, 0.3, 2.1])
    # For the first widget, we create a slider to select years
    with columns[2]:
        df1 = qs_data.copy()
        df1["log(international_students)"] = np.log(df1["international_students"])
        df1["log(student_faculty_ratio)"] = np.log(df1["student_faculty_ratio"])
        df1["log(faculty_count)"] = np.log(df1["faculty_count"])
        start_year = st.slider("Select the year", 2017, 2022, 2017)
        current_data = df1.loc[df1['year'] == start_year]
    # For the second widget, we create a selectbox to select university type
    with columns[0]:
        type = st.radio('Choose the university type', ('Public', 'Private'))
        type_data = current_data.loc[df1['type'] == type]
    # For the third widget, we create a selectbox to select university size
    with columns[4]:
        size = st.selectbox('Choose the university size', ('XL', 'L', 'M', 'S'))
        size_data = type_data.loc[df1['size'] == size]
    # For the fourth widget, we create a selectbox to select university region
    with columns[6]:
        REGION = st.selectbox('Select continent', options = ['Global','North America','Europe','Asia','Oceania','Latin America','Africa']) 


    # Create 2 plots
    chart1, chart2 = st.columns([2,1])
    # For chart1 we put a multiple-line chart
    with chart1:
        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['faculty_count'], empty='none')
        # Draw the basic line chart
        t = alt.TitleParams("The Relationship Between Student_Faculty_Ratio & Score", subtitle=["Multiple-Line Tooltip"])
        line = alt.Chart(current_data, title=t).mark_line(interpolate='basis').encode(
            x = alt.X('faculty_count:Q'),
            y = alt.Y('student_faculty_ratio:Q'),
            color='region:N'
        )
        # Transparent selectors across the chart. This is what tells us the x-value of the cursor
        selectors = alt.Chart(current_data).mark_point().encode(
            x = alt.X('faculty_count:Q'),
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )
        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )
        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'student_faculty_ratio:Q', alt.value(' '))
        )
        # Draw a rule at the location of the selection
        rules = alt.Chart(current_data).mark_rule(color='gray').encode(
            x='faculty_count:Q',
        ).transform_filter(
            nearest
        )
        # Put the five layers into a chart and bind the data
        alt.layer(
            line, selectors, points, rules, text
        )
        st.altair_chart((line+selectors+points+rules+text).interactive(), use_container_width = True)

    # For chart2 we put a redial chart
    with chart2:
        # Create a readial chart to show the composition of public & private universities
        t = alt.TitleParams("The Composition of Research Output Levels", subtitle=["Donut Chart"])
        donut = alt.Chart(type_data, title=t).mark_arc(innerRadius=95).encode(
            theta = alt.Theta("count(research_output):Q"),
            color = alt.Color("research_output:N"),
            tooltip = ['research_output','count(research_output)']
        )
        st.altair_chart(donut, use_container_width = True)



# Create the second panel 
panel2 = st.container()
with panel2:
    # Partition the second panel to 3 parts
    columns = st.columns([1, 2, 2])
    # For the first column, we create a static information panel
    with columns[0]:
        st.markdown("<div style='background:#e6e6e6; text-align: center;'><span style='color: #ac2217; font-weight:bold'>Quick Information</span></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><span style='color: #000000; font-size:1.0rem; font-weight:bold'>Average Research Output</span></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><span style='color: #681a49; font-size:1.5rem; font-weight:bold'>13.264</span></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><span style='color: #000000; font-size:1.0rem; font-weight:bold'>Average International Students</span></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><span style='color: #681a49; font-size:1.5rem; font-weight:bold'>1989</span></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><span style='color: #000000; font-size:1.0rem; font-weight:bold'>Public:Private</span></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><span style='color: #681a49; font-size:1.5rem; font-weight:bold'>4.5:1</span></div>", unsafe_allow_html=True)
    # For the second column, we create a barplot
    with columns[2]:
        t = alt.TitleParams("# of Universities in All Continents", subtitle=["Bar Chart"])
        bar = alt.Chart(type_data, title=t).mark_bar().encode(
            x = alt.X('count(region):Q', axis=alt.Axis(labelAngle=45)),
            y = alt.Y('region:N', sort='-x'),
            color = alt.Color('count(region):Q'),
            tooltip = ['region','count(region)']
        )
        st.altair_chart(bar, use_container_width = True)
    # For the third column, we create a layered histogram
    with columns[1]:
        # Create a histogram to show the distribution of faculty_count
        t = alt.TitleParams("The Distribution of faculty_count", subtitle=["Layered Histogram"])
        hist1 = alt.Chart(type_data, title=t).mark_bar(
            opacity=0.3,
            binSpacing=0
        ).encode(
            alt.X('log(faculty_count):Q', bin=alt.Bin(maxbins=80)),
            alt.Y('count(faculty_count):Q', stack=None),
            alt.Color('region:N')
        )
        st.altair_chart(hist1.interactive(), use_container_width = True)



# Set Up
country_codes = pd.read_csv('https://raw.githubusercontent.com/CristoDragon/Visualization_Projects/refs/heads/main/Type1/Data/country_codes.csv' ,sep=',', encoding='latin-1')
country_codes.set_index('English short name', inplace = True)


#Reading file 
university_df = pd.read_csv('https://raw.githubusercontent.com/Dr-Banana/CSE5544/main/Zhang_10419_lab4_code/qs-world-university-rankings-2017-to-2022-V2.csv' ,sep=',', encoding='latin-1')


def draw_map(mtype,y):
    
    COLOR_THEME = {'count':"lighttealblue"}
    d['num'] = d[mtype]
    source = alt.topo_feature(data.world_110m.url, "countries")
    
    world_map = (
        alt.Chart(source, title=f'Universities in QS World University Rankings {y} ')
        .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
            color=alt.Color(
                "num:N", 
                scale=alt.Scale(scheme=COLOR_THEME[mtype]), 
                legend = None),
            tooltip=[
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip("num:Q", title="Number of College"),
            ],
        )
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(d, "id", ["country", "num"]),
        )
    ).configure_view(strokeWidth=0).properties(width=1000, height=400).project("naturalEarth1")
    
    
    return world_map

               
if(REGION == 'Global'):
    year_university_df = university_df.loc[(university_df['year'] == start_year)]
else:
    year_university_df = university_df.loc[(university_df['year'] == start_year) & (university_df['region'] == REGION)]
        
d = pd.DataFrame(year_university_df.pivot_table(columns=['country'], aggfunc='size'))
d.columns = ['count']
d['id'] = country_codes['Numeric']
d['country'] = d.index
st.altair_chart(draw_map('count',start_year), use_container_width=True)
    