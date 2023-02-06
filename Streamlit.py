import streamlit as st
from PIL import Image
from TM1py import TM1Service

st.set_page_config(
    page_title="TM1py App",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://code.cubewise.com/tm1py-help-content',
        'Report a bug': "https://github.com/cubewise-code/tm1py/issues",
        'About': "# Powered by TM1py"
    }
)

image = Image.open('TM1py.png')
st.image(image)

st.subheader("Synchronize Dimensions :blue[**_between_**] TM1 instances :sunglasses:")
# Initialization of streamlit session state
# Reference: https://docs.streamlit.io/library/api-reference/session-state
if "dimensions" not in st.session_state:
    st.session_state["dimensions"] = ""

# 1. Dimension Selection
with st.form("dimension_selection"):
    st.write("1. Step: Get Dimensions From Source Instance")
    submitted = st.form_submit_button("Get All Dimensions From Source Instance")
    if submitted:
        with TM1Service(address='localhost', port=6041, user='admin', password='cwna', ssl=True) as tm1_source:
            # Get all dimensions from source
            dimensions = tm1_source.dimensions.get_all_names()

            # Store dimensions in session state
            st.session_state["dimensions"] = ",".join(dimensions)

# Only show the second step if dimensions are available
if not st.session_state["dimensions"]:
    st.stop()

# 2. Dimension Synchronization
with st.form("dimension_sync"):
    st.write("2. Step: Synchronize Dimension")
    # Get dimensions from session state and display them
    dimension_name = st.selectbox("Select Dimension:", options=st.session_state["dimensions"].split(","))
    submitted = st.form_submit_button("Synchronize Dimension")
    if submitted:
        with st.spinner("Synchronizing dimensions..."):
            with TM1Service(address='localhost', port=6041, user='admin', password='cwna', ssl=True) as tm1_source:
                with TM1Service(address='localhost', port=6047, user='admin', password='cwna',
                                ssl=True) as tm1_target:
                    dimension = tm1_source.dimensions.get(dimension_name=dimension_name)
                    tm1_target.dimensions.update_or_create(dimension)
        st.success("Dimension successfully synchronized")
