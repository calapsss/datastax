import streamlit as st
import pandas as pd
import time
from components.sidebar import sidebar
import core.utils as utils
import requests
import json

#Define API URL
API_URL = "http://127.0.0.1:8000"



def main():
    st.set_page_config(page_title="DataStax", page_icon="🧠", layout="wide")
    st.header("DataStax 🧠")

    #Sidebar
    sidebar('DataStax', 'Analyze your data simply smarter', 'Created with Microsoft Semantic Kernel', 'Show Data', 0)
    
  
    #File uploader
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        #Trigger data analysis
        dataInformation = requests.get(API_URL + "/analyzeDataframe/", params={"dataframe": df.head().to_json()})
        dataQuestions = requests.get(API_URL + "/generateQuestions/", params={"dataframe": dataInformation.content.decode("utf-8")})
        dataQuestions = dataQuestions.json()
        dataQuestionQueryPair = requests.get(API_URL + "/initQuestionQueryPair/")
        dataQuestionQueryPair = dataQuestionQueryPair.json()
        print("Data Question-Query Pair: ", dataQuestionQueryPair)
        print("Data Information: ", dataInformation.content)
        #add code here to analyze data
        st.success('Data Analysis Complete!')
        
    # #Upload file
    # print("Uploading file to backend server...")
    # response = requests.post(API_URL + "/uploadfile/", files={"file": uploaded_file})
    # print("Response: ", response.content)
    # file_name = response.content.decode("utf-8").split('"')[3]
            
        
    #PromptHandler Frontend
    with st.form(key="qa_form"):
        prompt = st.text_area("Ask a question about the document")
        submit = st.form_submit_button("Submit")

    if submit:
        if not utils.is_valid_query(prompt):
            st.error("Please enter a valid prompt. Prompt cannot be empty.")
        if df is None:
            st.error("Please upload a file first.")
    
        #Logic for promptHandler handles graph, table and explanations.

        st.write('To add interpret prompt logic')
    else:
        st.write('Suggested Prompts: ')
        x=0 
        if uploaded_file is not None:
            for question in dataQuestions:
                if x < 3: 
                    st.write(question)
                else: 
                    break
                x+=1
        else:
            st.write('No data analysis done yet')
        


    

    




    


import streamlit as st
import pandas as pd
import time
from components.sidebar import sidebar
import core.utils as utils
import requests
import json

#Define API URL
API_URL = "http://127.0.0.1:8000"

#Global variable for uploaded file
uploaded_file = None

def main():
    global uploaded_file
    st.set_page_config(page_title="DataStax", page_icon="🧠", layout="wide")
    st.header("DataStax 🧠")

    #Sidebar
    sidebar('DataStax', 'Analyze your data simply smarter', 'Created with Microsoft Semantic Kernel', 'Show Data', 0)
    
  
    #File uploader
    if uploaded_file is None:
        uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        print("Uploading file to backend server...")
        response = requests.post(API_URL + "/uploadfile/", files={"file": uploaded_file})
        print("Response: ", response.content)
        file_name = response.content.decode("utf-8").split('"')[3]
        #Trigger data analysis
        with st.spinner('Analyzing data...'):
            dataInformation = requests.get(API_URL + "/analyzeDataframe/", params={"dataframe": df.head().to_json()})
            dataQuestions = requests.get(API_URL + "/generateQuestions/", params={"dataframe": dataInformation.content.decode("utf-8")})
            dataQuestions = dataQuestions.json()
            dataQuestionQueryPair = requests.get(API_URL + "/initQuestionQueryPair/")
            dataQuestionQueryPair = dataQuestionQueryPair.json()
            print("Data Question-Query Pair: ", dataQuestionQueryPair)
            print("Data Information: ", dataInformation.content)
            #add code here to analyze data
            st.success('Data Analysis Complete!')
            
        
    #PromptHandler Frontend
    with st.form(key="qa_form"):
        prompt = st.text_area("Ask a question about the document")
        submit = st.form_submit_button("Submit")

    if submit:
        if not utils.is_valid_query(prompt):
            st.error("Please enter a valid prompt. Prompt cannot be empty.")
        if uploaded_file is None:
            st.error("Please upload a file first.")
    
        #Logic for promptHandler handles graph, table and explanations.

        st.write('To add interpret prompt logic')
    else:
        st.write('Suggested Prompts: ')
        x=0 
        if uploaded_file is not None:
            for question in dataQuestions:
                if x < 3: 
                    st.write(question)
                else: 
                    break
                x+=1
        else:
            st.write('No data analysis done yet')

if __name__ == "__main__":
    main()

