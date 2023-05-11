import streamlit as st
import numpy as np
import pandas as pd
import time
import os
import altair as alt
import pydeck as pdk
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="Matrix Arc for people taking bus on Monday, March 6th, 2023", page_icon=":taxi:")

st.title("Matrix Arc for people taking bus on Monday, March 6th, 2023. Galbadral Dashzeveg")

DATA_URL = "for_arc.csv"
# A bounding box for downtown San Francisco, to help filter this commuter data

df = pd.read_csv(DATA_URL)
# Filter to bounding box

GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

# Specify a deck.gl ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_width="freq * 0.05",
    get_source_position=["X", "Y"],
    get_target_position=["d_X", "d_Y"],
    get_tilt=20,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude= np.average(df['Y']),
    longitude=np.average(df['X']),
    bearing=0,
    pitch=50,
    zoom=10,
)


TOOLTIP_TEXT = {"html": "{freq} frequency <br /> Sit on bus in red; Out of bus in green"}
st.write(pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT))


DATA_URL1 = "for_arc_hour.csv"

df1 = pd.read_csv(DATA_URL1)


def update_query_params():
    hour_selected = st.session_state["pickup_hour"]
    st.experimental_set_query_params(pickup_hour=hour_selected)
row11_1, row11_2, row11_3 = st.columns((3,3,1))


with row11_1:
    hour_selected = st.slider(
                "Select time:", 0, 23, key="pickup_hour", on_change=update_query_params
                )
# A bounding box for downtown San Francisco, to help filter this commuter data


def filter_df(df,hour_selected):
    df=df.loc[df['hour']==hour_selected]
    return df

# Filter to bounding box
#filter_df(df1,hour_selected)

GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]
df1=filter_df(df1,hour_selected)
# Specify a deck.gl ArcLayer
arc_layer1 = pdk.Layer(
    "ArcLayer",
    data=df1,
    get_width="freq * 0.1",
    get_source_position=["X", "Y"],
    get_target_position=["d_X", "d_Y"],
    get_tilt=20,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude= np.average(df['Y']),
    longitude=np.average(df['X']),
    bearing=0,
    pitch=50,
    zoom=10,
)


TOOLTIP_TEXT2 = {"html": "{freq} frequency<br />{hour} o'clock <br /> Sit on bus in red; Out of bus in green"}
st.write(pdk.Deck(arc_layer1, initial_view_state=view_state, tooltip=TOOLTIP_TEXT2))