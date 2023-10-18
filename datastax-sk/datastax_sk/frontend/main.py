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
    df = None

    #File uploader
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

    dataAnalysis = False
    #File uploader
    if df is None:
        st.session_state.df = None
        st.write('Upload your dataset')
    #Logic to trigger dataAnalysis
    else:
        with st.spinner('Analyzing data...'):
            dataQuestions = requests.get(API_URL + "/generateQuestions/", params={"dataframe": df.head().to_json()})
            dataQuestions = dataQuestions.json()
            dataQuestionQueryPair = requests.get(API_URL + "/initQuestionQueryPair/")
            dataInformation = requests.get(API_URL + "/analyzeDataframe/", params={"dataframe": df.head().to_json()})
            dataQuestionQueryPair = dataQuestionQueryPair.json()
            print("Data Question-Query Pair: ", dataQuestionQueryPair)
            print("Data Information: ", dataInformation)
            dataAnalysis = True
            #add code here to analyze data
            st.success('Data Analysis Complete!')
            
    

    #Sidebar
    clickedSidebar = sidebar('DataStax', 'Analyze your data simply smarter', 'Created with Microsoft Semantic Kernel', 'Show Data', 0)
    if clickedSidebar:
        if df is not None:
            st.title('Connected Dataframe')
            st.write(df)
        else:
            st.write('No file uploaded')
        if st.button('Exit'):
            clickedSidebar = False
            st.close()

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
        if dataAnalysis:
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
