import streamlit as st
import requests
import pandas as pd
import base64
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import joblib
import yfinance as yf

# Function to generate HTML for the DataFrame with a clickable link
def generate_html_with_link(df):
    df_copy = df.copy()
    df_copy["URL"] = df_copy["URL"].apply(lambda x: f'<a href="{x}" target="_blank">Open Article</a>')
    return df_copy.to_html(escape=False, index=False, render_links=True)

# Styling
st.markdown("""
    <style>
        body {
            background-color: #033673;
            color: white;
        }
        .custom-container {
            margin: 20px;
            margin-top: 90px;
        }
        /* Add other styles as needed */
    </style>
""", unsafe_allow_html=True)

# Load Model for Movement
current_directory = os.path.dirname(__file__)
model_path_movement = os.path.join(current_directory, 'Logistic Regression_accuracy_0.61.joblib')
loaded_model_movement = joblib.load(model_path_movement)

# Get today's date and format it
today = datetime.now().strftime("%Y-%m-%d")

# Define time intervals for the user
intervals = {'1d': today,
             '1w': (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d"),
             '1m': (datetime.now() - timedelta(weeks=4)).strftime("%Y-%m-%d"),
             '3m': (datetime.now() - timedelta(weeks=12)).strftime("%Y-%m-%d"),
             '6m': (datetime.now() - timedelta(weeks=24)).strftime("%Y-%m-%d")}

st.title('LiveFeed')

ticker = st.text_input('Ticker:')
interval = st.selectbox('Interval:', ['1d', '1w', '1m', '3m', '6m'])

if st.button('Get Articles'):
    st.write('Loading...')

    try:
        # Use code from Database
        # Store stock data
        stock_data = []

        # Use Alpha Vantage API call with ticker and key
        # Get JSON file
        api_key = '9NLUTD6I2QZTR2BZ'
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}&limit=1000'
        response = requests.get(url, verify=True)
        json_request_data = response.json()

        # If there is a feed
        if 'feed' in json_request_data:
            feed_data = json_request_data['feed']

            # For each article in the feed
            for article in feed_data:
                # Try the following (if there is an error, make sure this doesn't stop)
                # Use try and except
                try:
                    # Get the article URL
                    article_url = article.get('url', '')

                    # Store the following as None
                    article_text = None

                    # If there is an article URL
                    if article_url:
                        # Use BeautifulSoup to get the text from the website
                        article_response = requests.get(article_url, verify=True)
                        article_html = article_response.text
                        article_soup = BeautifulSoup(article_html, 'html.parser')
                        article_paragraphs = article_soup.find_all('p')
                        article_text = '\n'.join(paragraph.text.strip() for paragraph in article_paragraphs)

                    # Get the time published for the article
                    published_date = article.get('time_published', '')[:10]

                    # Format date so that we can use it
                    formatted_date = datetime.strptime(published_date, "%Y%m%dT%H").strftime("%Y-%m-%d") if published_date else 'NA'

                    # Skip articles not within the selected interval
                    print(formatted_date, today)
                    if interval == '1d' and formatted_date < intervals['1d']:
                        break
                    elif interval == '1w' and formatted_date < intervals['1w']:
                        break
                    elif interval == '1m' and formatted_date < intervals['1m']:
                        break
                    elif interval == '3m' and formatted_date < intervals['3m']:
                        break
                    elif interval == '6m' and formatted_date < intervals['6m']:
                        break

                    # Store the following as NA
                    article_price_open_stock = 'NA'
                    article_price_close_stock = 'NA'

                    # If there is a date, get article open and close price for stock from Yahoo finance
                    if formatted_date != 'NA':
                        stock = yf.Ticker(ticker)
                        historical_data_stock = stock.history(start=formatted_date, end=(datetime.strptime(formatted_date, "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d"))
                        article_price_open_stock = historical_data_stock.iloc[0]["Close"]
                        article_price_close_stock = historical_data_stock.iloc[-1]["Close"]

                    # Make a print statement stating that prices were collected
                    if article_price_open_stock != 'NA' and article_price_close_stock != 'NA':
                        print(f"For the article on {formatted_date}, stock movement is available.")

                    # Calculate movement of the stock between article_price_open_stock and article_price_close_stock
                    if formatted_date >= today or formatted_date == (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"):
                        actual = "N/A"
                    else:
                        actual_movement = article_price_close_stock - article_price_open_stock
                        if actual_movement > 0:
                            actual = 1
                        elif actual_movement == 0:
                            actual = 'N/A'
                        else:
                            actual = 0

                    # Collect Model Prediction
                    if article_text is None:
                        model_prediction = loaded_model_movement.predict([article.get('summary', '')])[0]
                        likelihood = loaded_model_movement.predict_proba([article.get('summary', '')])[0][1] * 100
                    else:
                        model_prediction = loaded_model_movement.predict([article_text])[0]
                        likelihood = loaded_model_movement.predict_proba([article_text])[0][1] * 100

                    # Record everything
                    record = {
                        "Date Published": formatted_date,
                        "Likelihood": likelihood,
                        "Model Prediction": model_prediction,
                        "Actual": actual,
                        "Open Price": article_price_open_stock,
                        "Close Price": article_price_close_stock,
                        "URL":  article_url  # Store the URL directly
                    }

                    # Append into stock data
                    stock_data.append(record)

                # If there is an error at any point, run an exception so that the program doesn't break
                except Exception as e:
                    print(f"Error occurred: {e}")
                    continue

            # Outside the for loop, modify the DataFrame creation
            df = pd.DataFrame(stock_data, columns=["Date Published", "Likelihood", "Model Prediction", "Actual", "Open Price", "Close Price", "URL"])
            df_excel = pd.DataFrame(stock_data)
            excel_file_path = os.path.join(current_directory, 'test.xlsx')
            df_excel.to_excel(excel_file_path, index=False)

            # Display the table with custom CSS to fit the page
            st.markdown(
                f"""
                <style>
                    table {{
                        width: 100%;
                    }}
                </style>
                """, unsafe_allow_html=True
            )

            # Update the st.write statement to display the modified DataFrame with a clickable link
            st.write(generate_html_with_link(df), unsafe_allow_html=True)

            # Add a button for downloading the table as an Excel file
            if st.button('Download Table as Excel'):
                print(f'Excel file path received: {excel_file_path}')  # Debugging line
                if excel_file_path:
                    excel_file_encoded = base64.b64encode(open(excel_file_path, 'rb').read()).decode()
                    st.markdown(
                        f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_file_encoded}" '
                        f'download="article_table.xlsx">Download Excel File</a>',
                        unsafe_allow_html=True
                    )
                else:
                    st.warning('No Excel file path provided.')

    except requests.exceptions.ConnectionError:
        st.error('Unable to connect to the server. Make sure the server is running.')

    except Exception as e:
        st.error(f'Error fetching articles. Please try again. Error: {e}')
