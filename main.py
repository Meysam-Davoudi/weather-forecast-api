import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from datetime import datetime
import functions as func


def requests_history_operation():
    if "history_table" in st.session_state:
        requests_history = func.get_requests_history()
        edited_rows = st.session_state["history_table"]["edited_rows"]

        if edited_rows:
            for index, value in edited_rows.items():
                if "Delete" in value:
                    if value["Delete"]:
                        func.delete_request_history(requests_history[index][0])

                if "Show response" in value:
                    if value["Show response"]:
                        st.session_state["response_json_id"] = requests_history[index][0]


st.set_page_config(
    page_title="Weather Forecast API",
    page_icon="🌤️",
    layout="centered",
)

modal = Modal(
    "JSON Response",
    key="response_modal",
)

if 'response_json_id' not in st.session_state:
    st.session_state["response_json_id"] = {}

requests_history_operation()
current_datetime = datetime.now()

st.markdown("<h1 style='text-align: center;'>🌤️<br/>Weather Forecast API</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>" + current_datetime.strftime("%d %b %Y") + "</div>",
            unsafe_allow_html=True)

st.selectbox('Select the city', func.get_country_list(), key="country_city")

weather_data = None

current_tab, forecast_tab, history_tab = st.tabs(["Current", "Forecast", "Request history"])

with current_tab:
    if st.button("Show the current weather", key="current_button"):
        weather_status = func.get_weather_status(st.session_state["country_city"])

        if "location" in weather_status:
            weather_data = ({
                                "image_url": weather_status["current"]["condition"]["icon"],
                                "temperature": weather_status["current"]["temp_c"],
                                "description": weather_status["current"]["condition"]["text"],
                                "date": current_datetime.strftime("%Y-%m-%d")
                            },)

with forecast_tab:
    st.selectbox("Number of days of weather forecast. Value ranges from 1 to 3",
                 options=["1", "2", "3"], key="forecast_days")

    if st.button("Show weather forecast", key="forecast_button"):
        weather_status = func.get_weather_status(st.session_state["country_city"], st.session_state["forecast_days"])

        if "location" in weather_status:
            weather_data = ()
            for weather in weather_status["forecast"]["forecastday"]:
                data = {
                    "image_url": weather["day"]["condition"]["icon"],
                    "temperature": f'<small>Avg</small>{weather["day"]["avgtemp_c"]}',
                    "description": weather["day"]["condition"]["text"],
                    "date": weather["date"]
                }
                weather_data += (data,)

with history_tab:
    show_res_btn_col, reset_btn_col = st.columns(2)

    with show_res_btn_col:
        json_data = ""
        if st.session_state["response_json_id"]:
            json_data = func.get_request_json_data(st.session_state["response_json_id"])

        if st.button("Show Response", key="show_response_button"):
            modal.open()

        if modal.is_open():
            with modal.container():
                if st.session_state["response_json_id"]:
                    st.json(json_data)

    with reset_btn_col:
        if st.button("Clear history", key="clear_history_button", type="primary"):
            func.clear_requests_history()

    df = pd.DataFrame([(hist[1], hist[2], hist[3], func.convert_unix_to_string(hist[4]), False, False)
                       for hist in func.get_requests_history()],
                      columns=["Location", "lat,lon", "Request type", "Request time", "Show response", "Delete"])
    df_config = st.data_editor(
        df,
        column_config={
            "Location": st.column_config.TextColumn(
                width="medium",
                disabled=True
            ),
            "lat,lon": st.column_config.TextColumn(
                disabled=True,
            ),
            "Request type": st.column_config.TextColumn(
                disabled=True,
            ),
            "Request time": st.column_config.TextColumn(
                disabled=True,
            )
        },
        hide_index=True,
        key="history_table"
    )

st.markdown(func.weather_card_html_layout(weather_data), unsafe_allow_html=True)

footer = """
<style>
    div[data-modal-container='true'][key='response_modal'] {
        top: 0 !important;
    }
    div[data-testid="column"]:nth-of-type(1){
        text-align:left !important;
    } 

    div[data-testid="column"]:nth-of-type(2){
        text-align:right !important;
    } 
</style>

<div class="st-emotion-cache-h5rgaw ea3mdgi1" style="text-align:center;margin-top:30px">
    &#169;2024 Meysam Davoudi, All Rights Reserved.
    <a href="https://github.com/Meysam-Davoudi/weather-forecast-api" target="_blank" style="text-decoration:none;">
        (GITHUB)
    </a>
</div>
"""
# Display the footer
st.markdown(footer, unsafe_allow_html=True)
