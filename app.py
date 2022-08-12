# import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import country_converter as coco
cc = coco.CountryConverter()

st.set_page_config(
    page_title="Interactive Dashboard about Salary in Data Sciense",
    page_icon="✅",
    layout="wide",
)

@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv('data/data.csv')
    
def data_preprocessing(df):
    map_Level = {'EN':'Entry-level / Junior','MI':'Mid-level / Intermediate','SE':'Senior-level / Expert','EX':'Executive-level / Director'}
    df['experience_level'] = df['experience_level'].map(map_Level)
    map_Company = {'S':'Small','M':'Mid-size','L':'Large'}
    df['company_size'] = df['company_size'].map(map_Company)
    top5 = df[['job_title','salary_in_usd']].groupby(by='job_title')['salary_in_usd'].mean().reset_index().sort_values(['salary_in_usd'],ascending = False)
    salyear = df[['work_year','experience_level','salary_in_usd']].groupby(by=['work_year','experience_level'])['salary_in_usd'].mean().reset_index().sort_values(['salary_in_usd'],ascending = False)
    salyeartotal = df[['work_year','salary_in_usd']].groupby(by=['work_year'])['salary_in_usd'].mean().reset_index().sort_values(['salary_in_usd'],ascending = False)
    salyeartotal['experience_level']='Total'
    salyear = pd.concat([salyear,salyeartotal])
    remote = df[['remote_ratio','company_size','salary_in_usd']].groupby(by=['remote_ratio','company_size'])['salary_in_usd'].mean().reset_index().sort_values(['salary_in_usd'],ascending = False)
    standard_names = cc.convert(names = df['company_location'], to = 'ISO3')
    df['company_location']=standard_names
    mapincome = df[['company_location','salary_in_usd']].groupby(by=['company_location'])['salary_in_usd'].sum().reset_index().sort_values(['salary_in_usd'],ascending = False)
    return [top5,salyear,remote,mapincome]
    
def mean(list):
    total = 0
    count = 0
    for i in list:
        total += i
        count+=1
    return total/count

df = get_data()

# dashboard title
st.title("Interactive Dashboard about Salary in Data Sciense")

# top-level filters
country_filter = st.selectbox("Select the Job", ['All']+list(pd.unique(df["company_location"])),index=0)
job_filter = st.multiselect("Select the Job", pd.unique(df["work_year"]),default=pd.unique(df["work_year"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
if country_filter != 'All':
    df = df[df["company_location"]==country_filter]
df = df[(df["work_year"]).isin(job_filter)]
dflist = data_preprocessing(df)
top5 = dflist[0]
salyear = dflist[1]
remote = dflist[2]
mapincome = dflist[3]

with placeholder.container():

    # Infographic
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Average Salary in k$",
        value=round(mean(df['salary_in_usd'])/1000,2)
    )
    
    kpi2.metric(
        label="Average Work Done Remotely %",
        value=round(mean(df['remote_ratio']),2)
    )
    
    kpi3.metric(
        label="Most of Employees from",
        value=df['employee_residence'].value_counts().index[0]
    )

    # create three columns
    fig_col1,fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Top 5 Highest income Job Titles")
        fig = px.bar(top5.head(), x='job_title', y='salary_in_usd')
        st.write(fig)
        
    with fig_col2:
        st.markdown("### Salary by Level over Priod from 2020-2022")
        fig2 = px.bar(salyear, x="work_year", y="salary_in_usd",color="experience_level", barmode="group")
        st.write(fig2)
    fig_col3,fig_col4 = st.columns(2)
    with fig_col3:
        st.markdown("### Salary Distributed by Remote Ratio and Company Size")
        fig3 = px.density_heatmap(remote, x="remote_ratio", y="company_size", z = 'salary_in_usd', color_continuous_scale="Viridis")
        st.write(fig3)
        
    with fig_col4:
        st.markdown("### Total Salary in World Map")
        fig4 = px.scatter_geo(mapincome, locations="company_location",size="salary_in_usd",projection="natural earth")
        st.write(fig4)

    # View data details
    st.markdown("### Detailed Data View")
    st.dataframe(df)
    
expander = st.expander("More about this project")
expander.write("This is an interactive dashboard project done by  hkfuoc98@gmail.com/n source code: https://github.com/hkfuoc98/Data-Science-Salary-Dashboard.git")