#Checks for the quality of data received and can it answer the input/query for us. If found unsatisfactory then modify the query
#It assumes you have a category wise list or a list of suggested apps if any
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
import openai
import json
from langchain_core.documents import Document

key1=st.secrets["OPENAI_API_KEY"]
API_KEY = os.getenv("OPENAI_API_KEY", key1)  # Replace if testing locally
OPENAI_API_KEY = key1
openai.api_key = key1

with open('categories_no_hyphens.txt', 'r') as file:
    content = file.read()

# st.markdown(content)

query=st.text_input("Input a query that you want to ask")
list_of_software=st.text_input("Input the hypothetical softwares that are retrieved by the retreival engine for the given query")

if st.button("Show me the insights"): 
    system_prompt=f'''
            You are given a query and a list of software names for which information has been retrieved. 

            Your task is:  
            1. If the query can be answered using the retrieved software information, output:  
            - "Ok, good for analysis"  
            - Additionally, explain **how** the query can be answered using the provided software data.  
            2. If the query **cannot** be answered using the retrieved software, output:  
            - "No"  
            - Provide insights on the type of software or specific product names that might answer the query better.  

            ### Example Categories  
            {content}  

            ### Guidelines:  
            - Base your analysis **only** on the information retrieved for the listed software.  
            - Do **not** assume any knowledge beyond the provided list of software.  
            - Suggest categories or product names that align with the query if the current software doesn't suffice.  

            ### Your Task  
            Query: {query}  
            List of retrieved software: {list_of_software}  
            Based on the provided data, analyze and output the response as per the guidelines above.
        '''

    #General template for question answering for openai using api
    response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use "gpt-3.5-turbo" or "gpt-4" based on your need
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.2
        )
    st.markdown(response['choices'][0]['message']['content'])
    st.markdown(list_of_software)
