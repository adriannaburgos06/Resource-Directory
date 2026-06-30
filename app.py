import streamlit as st
import pandas as pd

# -------------------------------------------------
# PAGE SETUP
# -------------------------------------------------
st.set_page_config(page_title="Resource Directory", layout="wide")


st.title("Resource Directory")

# -------------------------------------------------
# LOAD + CLEAN DATA
# -------------------------------------------------
df = pd.read_csv("resources.csv")

# clean column names
df.columns = df.columns.str.strip()

# fill missing values first
df = df.fillna("")

# clean important text columns
for col in ["County", "Type of Service", "Name", "City", "State", "Zip Code"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace("nan", "")

# -------------------------------------------------
# CLEAN FUNCTION
# -------------------------------------------------
def clean(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
st.sidebar.header("Filters")

service_options = sorted(df["Type of Service"].unique())
county_options = sorted(df["County"].unique())

selected_service = st.sidebar.selectbox(
    "Type of Service",
    ["All"] + service_options
)

selected_county = st.sidebar.selectbox(
    "County",
    ["All"] + county_options
)

# -------------------------------------------------
# FILTER DATA
# -------------------------------------------------
filtered = df.copy()

if selected_service != "All":
    filtered = filtered[filtered["Type of Service"] == selected_service]

if selected_county != "All":
    filtered = filtered[filtered["County"] == selected_county]

# -------------------------------------------------
# RESULTS
# -------------------------------------------------
st.write(f"Showing {len(filtered)} resources")

if filtered.empty:
    st.warning("No matching resources found.")

else:
    for _, row in filtered.iterrows():

        # Clean fields
        name = clean(row.get("Name"))
        service = clean(row.get("Type of Service"))
        address = clean(row.get("Address"))
        city = clean(row.get("City"))
        state = clean(row.get("State"))
        zip_code = clean(row.get("Zip Code"))
        county = clean(row.get("County"))
        phone = clean(row.get("Phone"))
        email = clean(row.get("Email"))

        # Detect virtual/flexible
        is_virtual = all([
            address == "",
            city == "",
            state == "",
            zip_code == "",
            county == ""
        ])

        # -------------------------------------------------
        # CARD
        # -------------------------------------------------
        with st.container(border=True):

            # Name
            st.subheader(name)

            # Service
            st.markdown(f"**Type of Service:** {service}")

            # Location logic
            if is_virtual:
                st.success("Virtual / Flexible (Available across all counties)")
            else:
                address_parts = [address, city, state, zip_code]
                full_address = ", ".join([x for x in address_parts if x])

                if full_address:
                    st.markdown(f"{full_address}")

                if county:
                    st.caption(f"County: {county}")

            # Contact
            if phone:
                st.markdown(f"{phone}")

            if email:
                st.markdown(f"{email}")

            st.divider()