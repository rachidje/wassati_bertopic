import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# p = open("data/graphs/topic_merged_per_class_sentiment.html")
# components.html(p.read())
st.set_page_config(layout="wide")

st.title("Schneider Electric Verbatim Analysis")

@st.cache_data
def load_data():
    data = pd.read_csv('/media/cattiaux/DATA/Wassati/team_data/schneider/df_all_labelled.csv')
    return data

st.write("""
Here you will find many ways to investigate the schneider data through several forms of data visualization

**Have fun :)**
""")

st.header("Clustering des data")

col1, col2 = st.columns([1,1.7])
with col1:
    st.subheader('Many very precise topics')
    with open('data/graphs/topic_visualize_topics.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)
with col2:
    st.subheader('''Let's see the best 12 topics''')
    with open('data/graphs/topics_barchart_viz.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)

st.subheader('''Let's ordered all those topics hierarchicaly''')
with open('data/graphs/topic_hierarchy.html', 'r') as f:
    html_code = f.read()
components.html(html_code, height=1100)

st.subheader('''Let's regroup them in relative topics''')
with open('data/graphs/topic_merged_visualize_reduced_docs.html', 'r') as f:
    html_code = f.read()
components.html(html_code, height=750)

st.subheader('''And check their evolution in time''')
with open('data/graphs/topic_merged_topics_over_time_months.html', 'r') as f:
    html_code = f.read()
components.html(html_code, height=500)

st.subheader('''How the topics are related to each other ?''')
col1, col2 = st.columns(2)
with col1:
    st.subheader('The global topics relations')
    with open('data/graphs/topic_merged_heatmap.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)
with col2:
    st.subheader('''The sub-topics relations''')
    with open('data/graphs/topic_heatmap.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)


st.header("Topic Repartition")

# Giving user options for selecting the class repartition
st.subheader('Select the repartition information :')
option = st.selectbox(
    'By which class do you want to see the topic repartition?',
    ('By Year', 'By Zone', 'By Cluster','By Country', 'By Market'))

# Produces topic_per_class viz 
if option == 'By Year':
    with open('data/graphs/topic_merged_per_class_year.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)

if option == 'By Zone':
    with open('data/graphs/topic_merged_per_class_zone.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)

if option == 'By Cluster':
    with open('data/graphs/topic_merged_per_class_cluster.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)

if option == 'By Country':
    with open('data/graphs/topic_merged_per_class_country.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)

if option == 'By Market':
    with open('data/graphs/topic_merged_per_class_market.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)


st.header("Sentiment Analysis")

col1, col2 = st.columns([1,2.3])
with col1:
    st.subheader('By Sentiment')
    with open('data/graphs/topic_merged_per_class_sentiment.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)

with col2:
    st.subheader('By Emotions')
    with open('data/graphs/topic_merged_per_class_emotion.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)


shorter_names={
    "single_emotion_label":"emotion",
    "sentiment_label":"sentiment",
    "Market Segment":"market",
    "Account Country":"country",
    "Zone":"zone",
    "Clusters":"cluster",
    "year":"year"
}

def generate_value_options(df, class_name, sublcass_name):
    code = ""
    for value in df[class_name].unique():
        code += f'''if option == '{value}':
    with open(f'data/graphs/topics_per_class/topic_model_merged/per_{shorter_names[sublcass_name]}/for_{shorter_names[class_name]}/{value}.html', 'r') as f:
        html_code = f.read()
    components.html(html_code, height=750)
'''
    return code


st.subheader("Repartition of the subclass within an emotion")

emotions = ('disappointment','admiration','neutral','approval','disapproval', 
            'gratitude','caring','realization','desire','annoyance', 
            'confusion','surprise','joy','optimism','nervousness', 
            'love','fear','curiosity','excitement','amusement','relief',
            'sadness','remorse','disgust','embarrassment','anger')
option = st.selectbox(
    'Which emotion do you want to see the repartition ?',emotions)

groups = ('Zone','Clusters','Account Country','Market Segment','year')
group_option = st.selectbox(
        'By which Market value do you want to see the emotion topic repartition?',groups)

emotion_option_code = generate_value_options(load_data(),"single_emotion_label",group_option)
exec(emotion_option_code)





st.subheader("Repartition of the emotions within a subclass")

option = st.selectbox(
    'By which class do you want to see the emotion topic repartition?',
    ('By Year', 'By Zone', 'By Cluster','By Country', 'By Market'))

markets=('Machinery', 'Industrial Manufacturing and Commercial', 'Water',
       'MMM', 'Energies and Chemicals', 'Food & Beverage', 'Healthcare',
       'Public Access, Education, Research, Finance Buildings',
       'IT Equipment and Professional Services',
       'Automotive & E-Mobility', 'Marine & Shore Power', 'Power & Grid',
       'Transportation', 'Unknown', 'Residential', 'Semiconductor',
       'Real Estate', 'LifeSciences', 'Cloud & Service providers',
       'Wholesale & Retail Trade', 'Household & Personal Care',
       'Education & Research', 'Hotels', 'Finance')
if option == 'By Market':
    option = st.selectbox(
        'By which Market Segment do you want to see the emotion topic repartition?',markets)

market_option_code = generate_value_options(load_data(),"Market Segment","single_emotion_label")
exec(market_option_code)

zones=('Italy', 'Nordic & Baltics', 'DACH', 'Iberia', 'East Asia Japan',
       'Greater India', 'US', 'France', 'Middle East and Africa', 'CEEI',
       'China & HK', 'South America', 'Pacific', 'BeNe', 'UK and Ireland',
       'Canada', 'Mexico & Central America')
if option == 'By Zone':
    option = st.selectbox(
        'By which Zone do you want to see the emotion topic repartition?',zones)

zone_option_code = generate_value_options(load_data(),"Zone","single_emotion_label")
exec(zone_option_code)

clusters=('Italy', 'Sweden', 'Germany', 'Spain', 'North East Asia',
       'Switzerland', 'India', 'USA', 'France', 'South East Asia',
       'Portugal', 'Finland & Baltics',
       'Turkey Central Asia and Pakistan', 'Denmark',
       'Middle Eastern Europe', 'China',
       'Argentina, Uruguay and Paraguay', 'Norway', 'Australia', 'Brazil',
       'Chile', 'Belgium', 'United Kingdom', 'Canada', 'Southeast Europe',
       'Austria', 'Netherlands', 'New Zealand', 'Israel',
       'Andean Cluster', 'Anglophone Africa', 'Mexico', 'Ireland',
       'Saudi Arabia & Yemen', 'North East Africa and Levant',
       'Francophone Africa', 'Gulf', 'Liechtenstein', 'Hong Kong & Macao')
if option == 'By Cluster':
    option = st.selectbox(
        'By which Cluster do you want to see the emotion topic repartition?',clusters)

cluster_option_code = generate_value_options(load_data(),"Clusters","single_emotion_label")
exec(cluster_option_code)

countries=('Italy', 'Sweden', 'Germany', 'Spain', 'Japan', 'Switzerland',
        'India', 'USA', 'France', 'Thailand', 'Vietnam', 'Portugal',
        'Finland', 'Turkey', 'Denmark', 'Poland', 'Korea, Republic of',
        'Czech Republic', 'China', 'Argentina', 'Norway', 'Indonesia',
        'Australia', 'Brazil', 'Chile', 'Singapore', 'Belgium',
        'United Kingdom', 'Slovakia', 'Canada', 'Romania', 'Austria',
        'Taiwan', 'Pakistan', 'Netherlands', 'New Zealand', 'Israel',
        'Colombia', 'Kazakhstan', 'Bulgaria', 'South Africa', 'Mexico',
        'Croatia', 'Ireland', 'Saudi Arabia', 'Greece', 'Malaysia',
        'Lithuania', 'Serbia', 'Egypt', 'Morocco', 'Hungary', 'Peru',
        'Estonia', 'United Arab Emirates', 'Lebanon', 'Dominican Republic',
        'Latvia', 'Jordan', 'Liechtenstein', 'Slovenia', 'San Marino',
        'Paraguay', 'Hong Kong', 'Kuwait', 'Qatar', 'Oman')
if option == 'By Country':
    option = st.selectbox(
        'By which Country do you want to see the emotion topic repartition?',countries)

country_option_code = generate_value_options(load_data(),"Account Country","single_emotion_label")
exec(country_option_code)

years=("2023", "2022", "2021", "2020", "2019", "2018")
if option == 'By Year':
    option = st.selectbox(
        'By which year do you want to see the emotion topic repartition?',years)

year_option_code = generate_value_options(load_data(),"year","single_emotion_label")
exec(year_option_code)









# Custom footer workaround to overide default streamlit footer
footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Model constructed by <a href="https://wassati.com" >Wassati - Engaging Organizations </a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)