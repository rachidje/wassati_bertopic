#!/usr/bin/env python3.9
import streamlit as st
# import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml

st.set_page_config(layout="wide")

from dashboard.v1.streamlit_pages import descriptive_analysis, topic_analysis, sentiment_analysis, homepage, global_sentiment, sentiment_by_topic, specific_sentiment

def main():
    SENTIMENT_PAGES = {
        "--------- 1. global sentiment": global_sentiment,
        "--------- 2. sentiment by topic": sentiment_by_topic,
        "--------- 3. specific sentiment": specific_sentiment
    }

    PAGES = {
        "Home": homepage,
        "Descriptive Analysis": descriptive_analysis,
        "Topic Analysis": topic_analysis,
        "Sentiment Analysis": sentiment_analysis
    }

    st.sidebar.title('Menu')
    selection = st.sidebar.radio("", list(PAGES.keys()))
    page = PAGES[selection]

    # Check if the selected page is "Sentiment Analysis"
    if selection == "Sentiment Analysis":
        # Display a new radio button for the subpages
        sentiment_selection = st.sidebar.radio("Sections from 'Sentiment Analysis'", list(SENTIMENT_PAGES.keys()))
        sentiment_page = SENTIMENT_PAGES[sentiment_selection]
        sentiment_page.app()
    else:
        page.app()
    # Custom footer workaround to overide default streamlit footer
    footer = """
            <div class="footer">
                <style>
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
                <p>Model constructed by <a href="https://wassati.com" >Wassati - Engaging Organizations </a></p>
            </div>
    """
    st.markdown(footer, unsafe_allow_html=True)


# with open('credentials.yaml') as file:
#     config = yaml.load(file, Loader= SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

# if'key' not in st.session_state:
#     st.session_state['key'] = config['cookie']['key']

# name, authentication_status, username = authenticator.login()

# if authentication_status:
#     authenticator.logout('Logout', 'main', key= 'unique_key')
#     st.title(f"Welcome {name}")
#     main()
# elif authentication_status == False:
#     st.error('Username/Password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')

main()


