import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def get_df() -> pd.DataFrame:
    hsis_df = pd.read_csv("data/accident.csv")
    return hsis_df

# Define how columns will be displayed
with st.echo(code_location='below'):
    "Define Configuration for columns"
    column_configuration = {"COUNTYNAME": st.column_config.TextColumn("County",help="County in Washington State"),
                                "FATALS": st.column_config.NumberColumn("Fatal Crashes", help="Total fatal crashes"),
                                 "young": st.column_config.NumberColumn("Young Driver", help="Crashes where driver was under 21",min_value=0,),
                                   "old": st.column_config.NumberColumn("Old Driver",help="Crashes where driver was 65+",min_value=0),
                                 "drink": st.column_config.NumberColumn("Drunk Driver",help="Crashes where driver was impaired", min_value=0),
                                "truck": st.column_config.NumberColumn("Truck Driver",help="Crashes involving a truck",min_value=0),
                              "old_car": st.column_config.NumberColumn("Old Vehicle",help="Crashes involving a vehicle 20+ years old", min_value=0),
                                 "list": st.column_config.BarChartColumn("Crash Emphasis Areas",help="Crashes delineated by emphasis area",width="medium",y_min=0,y_max=137),
    }
    df=get_df()
    
    # Make it pretty: add multiple tabs
    select, compare = st.tabs(["Select counties", "Compare selected"])
    
    with select: # Add select tab #############################################
        st.header("All counties")
    
        df = get_df()
        df=df.iloc[:,-7:]
        df = df.groupby(['COUNTYNAME']).sum().reset_index().sort_values("FATALS",ascending=False)
        columns_to_ls = ['FATALS','young','old','drink','truck','old_car']
        df['list'] = df[columns_to_ls].values.tolist()
    
        event = st.dataframe(
            df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
        )
    
        st.header("Selected counties")
        counties = event.selection.rows
        filtered_df = df.iloc[counties,:7]
        st.dataframe(
            filtered_df,
            column_config=column_configuration,
            use_container_width=True,
        )
    st.markdown("Calling `event.selection.rows`:")
    counties

    
    with compare: # Add compare tab ###########################################
        if len(counties) > 1:
            st.header("Crash data comparison: Bar Chart")
            st.bar_chart(filtered_df,x="COUNTYNAME", horizontal=True,use_container_width=True,stack=False)
            st.header("Crash data comparison: Line Chart")
            st.line_chart(filtered_df,x="COUNTYNAME")
        elif len(counties) > 0:
            st.header("Crash data comparison: Bar Chart")
            st.bar_chart(filtered_df,x="COUNTYNAME", horizontal=True,use_container_width=True,stack=False)
        else:
            st.markdown("No counties selected.")
    

