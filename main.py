from webcrawl import scrap
from data_clean import data_cleaning
import pandas as pd
import numpy
import re
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback
from datetime import date, datetime, time, timedelta
import openpyxl
from dash.exceptions import PreventUpdate
import time


app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='My First App with a Graph'),
    html.Hr(),
    dcc.Textarea(
        id='textarea',
        value='Input a city ex. Taipei',
        style={'width': '20%', 'height': 40},
    ),
    dcc.DatePickerSingle(
        id = 'my-date-picker-checkIn',
        min_date_allowed = date(2023, 11, 16),
        max_date_allowed = date(2023, 12, 31),
        initial_visible_month=date(2023, 11, 15),
        date=date(2023, 11, 16)
    ),
    dcc.DatePickerSingle(
        id = 'my-date-picker-checkOut',
        min_date_allowed = date(2023, 11, 17),
        max_date_allowed = date(2023, 12, 31),
        initial_visible_month=date(2023, 11, 15),
        date=date(2023, 11, 17)
    ),
    html.Button('Click here to see the image', id='show-secret'),
    dcc.Graph(id = 'scatter-plot')
])


@callback(
    Output(component_id='scatter-plot', component_property= 'figure'),
    [Input('textarea', 'value'),Input('my-date-picker-checkIn', 'date'),Input('my-date-picker-checkOut', 'date'),Input('show-secret', 'n_clicks')])

def update_output(input_location, date_value, date_out_value, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%Y-%m-%d')

        start_time = time.time()

        date_out = datetime.strptime(date_out_value, '%Y-%m-%d')
        print('start to scrap', date_value, date_out)
        scrap(location = input_location, checkIn = date_value, checkOut = date_out.strftime('%Y-%m-%d'), start= start_time)

        #clean
        print('start to clean')
        data_cleaning(location = input_location, checkIn = date_value)

        #plot
        print('start to plot')
        clean_excel_name = f'{input_location}_hotels_list_clean_{date_value}.xlsx'
        hotel_cleaned = pd.read_excel(clean_excel_name)


        fig = px.scatter(hotel_cleaned, x = "price", y = "distance", color = "rating", hover_data=['name'])

        n_clicks = None
        return fig
        #return string_prefix + date_string + '. \n' + "This is " +f' price for one night in Taipei, {checkIn} on Booking.com.'

if __name__ == '__main__':
    app.run(debug=True)
