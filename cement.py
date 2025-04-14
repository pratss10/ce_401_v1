import os
import streamlit as st
from groq import Groq
import pandas as pd
from io import StringIO

# Initialize Groq client
client = Groq(
 api_key=os.environ.get("GROQ_API_KEY"),
)

# Define function to generate construction cost estimate
def generate_construction_cost_estimate(params):
 messages = [
 {
 "role": "user",
 "content": f"create a detailed construction cost estimate in CSV format for a hostel with the following specifications:\n"
 f"Project: Hostel\n"
 f"Location: {params['location']}\n"
 f"Quality: {params['quality']}\n"
 f"Floors:{params['floors']}\n"
 f"Rooms/floor:{params['rooms_per_floor']}\n"
 f"Attached bathrooms:{params['attached_bathrooms']}\n"
 f"Common bathrooms:{params['common_bathrooms']}\n"
 f"Mess hall:{params['mess_hall']}\n"
 f"Kitchen:{params['kitchen']}\n"
 f"Common areas:{params['common_areas']}\n"
 f"Staff quarters:{params['staff_quarters']}\n"
 f"Parking:{params['parking']}\n"
 f"Elevator: {params['elevator']}\n"
 f"Security: {params['security']}\n"
 f"Solar: {params['solar']}\n"
 f"Rainwater: {params['rainwater']}\n"
 f"WiFi: {params['wifi']}\n"
 f"CSV format with columns: Category,Item,Unit,Quantity,Rate,Amount\n"
 f"Include all construction components with calculated quantities and appropriate rates.\n"
 f"Add10% contingency. Only output the CSV data with header and consider gst."
 }
 ]

 chat_completion = client.chat.completions.create(
 messages=messages,
 model="llama-3.3-70b-versatile",
 )

 return chat_completion.choices[0].message.content

# Streamlit app
st.title("Construction Cost Estimate Generator")

with st.form("params_form"):
 location = st.selectbox("Location", ["Urban", "Rural"])
 quality = st.selectbox("Quality", ["Low", "Medium", "High"])
 floors = st.number_input("Number of Floors", min_value=1)
 rooms_per_floor = st.number_input("Number of Rooms per Floor", min_value=1)
 attached_bathrooms = st.number_input("Number of Attached Bathrooms", min_value=0)
 common_bathrooms = st.number_input("Number of Common Bathrooms", min_value=0)
 mess_hall = st.checkbox("Mess Hall")
 kitchen = st.checkbox("Kitchen")
 common_areas = st.number_input("Number of Common Areas", min_value=0)
 staff_quarters = st.number_input("Number of Staff Quarters", min_value=0)
 parking = st.number_input("Number of Parking Spaces", min_value=0)
 elevator = st.checkbox("Elevator")
 security = st.checkbox("Security")
 solar = st.checkbox("Solar")
 rainwater = st.checkbox("Rainwater")
 wifi = st.checkbox("WiFi")

 submit_button = st.form_submit_button(label='Generate Estimate')

if submit_button:
 params = {
 "location": location,
 "quality": quality,
 "floors": int(floors),
 "rooms_per_floor": int(rooms_per_floor),
 "attached_bathrooms": int(attached_bathrooms),
 "common_bathrooms": int(common_bathrooms),
 "mess_hall": int(mess_hall),
 "kitchen": int(kitchen),
 "common_areas": int(common_areas),
 "staff_quarters": int(staff_quarters),
 "parking": int(parking),
 "elevator": "Yes" if elevator else "No",
 "security": "Yes" if security else "No",
 "solar": "Yes" if solar else "No",
 "rainwater": "Yes" if rainwater else "No",
 "wifi": "Yes" if wifi else "No",
 }

 estimate = generate_construction_cost_estimate(params)

 # Convert estimate to CSV
 csv_data = StringIO(estimate)
 df = pd.read_csv(StringIO(estimate), 
                      names=['Category', 'Item', 'Unit', 'Quantity', 'Rate', 'Amount'], 
                      skiprows=1)

 # Download CSV
 csv_file = df.to_csv(index=False)
 st.download_button(label="Download CSV", data=csv_file, file_name="construction_cost_estimate.csv")