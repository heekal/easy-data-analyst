# easy-data-analyst

This projects is my takes on creating python app for data analyst.<br>
Using streamlit for data visualization. This app able to process data into charts.<br>

## Goal:
Implementing streamlit for data cleaning, processing and visualizing.<br>
I use barchart to simplify connection between datas.<br>
This application aims for people who don't need heavy duty application for data visualization.<br>
**NOTE:** I'm still working on perfecting this app. You can use it but it may not suits on some cases.

## Tools:
1. Python streamlit (UI)
2. Python fastapi (Backend)
3. Python wordcloud (wordcloud visualization)

## Workflow Diagram:
_To be continued_

## How To Instal:
1. Download both frontend and backend
2. Open 2 Terminals
3. On Terminal1 do :
   cd Backend
   pip install -r requirements.txt
   python -m uvicorn backend:app --reload --port 8000
   **DO NOT CLOSE THE TERMINAL**
4. On Terminal2 do :
   cd Frontend
   pip install -r requirements.txt
   python -m streamlit run frontend.py
5. Open the link on from Terminal2
6. You can now use the application

## Documentations:
1. Main Page
   <image src=images/main.png>
   You can send your csv file on the side bar<br>
   
3. Content Preview
   <image src=images/inputdata.png>
   On this table, the data(s) aren't cleaned yet. You can choose any datas you want to clean or connect by selecting the core datas<br>
   
5. Data selection and cleaning
   <image src=images/setting.png>
   You must choose all the columns you have, or the app will raise an error.<br>
   
7. Results
   <image src=images/res1.png>
   <image src=images/res2.png>

   
