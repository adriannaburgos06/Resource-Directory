import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="Resource Directory",
    layout="wide"
)

st.markdown("""
<style>
.stApp{
    background:#FFFFFF;
    color:#0B2E59;
}
[data-testid="stSidebar"]{
    background:#0B2E59;
    padding-top:20px;
}

[data-testid="stSidebar"] *{
    color:white !important;
}

[data-testid="stSidebar"] label{
    color:white !important;
    font-weight:600;
}

h1,h2,h3,h4,h5,h6{
    color:#0B2E59 !important;
}

.stSelectbox div[data-baseweb="select"] > div{
    background:white !important;
    color:#0B2E59 !important;
    border:2px solid #0B2E59 !important;
    border-radius:0px !important;
}

.stSelectbox span{
    color:#0B2E59 !important;
}

.stSelectbox input{
    color:#0B2E59 !important;
    background:white !important;
}

.stSelectbox svg{
    fill:#0B2E59 !important;
}

/* Dropdown */

div[data-baseweb="popover"]{
    background:white !important;
}

div[data-baseweb="menu"]{
    background:white !important;
    border:2px solid #0B2E59 !important;
}

div[data-baseweb="menu"] div[role="option"]{
    background:white !important;
    color:#0B2E59 !important;
}

div[data-baseweb="menu"] div[role="option"]:hover{
    background:#FFF8D6 !important;
}

div[data-baseweb="menu"] div[data-highlighted="true"]{
    background:#FFF8D6 !important;
    color:#0B2E59 !important;
}

div[data-baseweb="menu"] div[aria-selected="true"]{
    background:#FFF2B3 !important;
    color:#0B2E59 !important;
}

[data-testid="stVerticalBlockBorderWrapper"]{
    background:#FFF8D6 !important;
    border:2px solid #E6D58C !important;
    border-radius:0px !important;
    padding:18px !important;
    margin-bottom:18px;
}

/* ===========================
   DIVIDER
=========================== */

hr{
    border-color:#D8C870 !important;
}

/* ===========================
   LOGO
=========================== */

.header-logo{
    display:flex;
    justify-content:center;
    margin-bottom:20px;
}

.header-logo img{
    width:280px;
}

/* ===========================
   HIDE STREAMLIT MENU
=========================== */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}
/* Make the sidebar toggle visible */
[data-testid="stSidebarCollapsedControl"] {
    background-color: white !important;
    border: 2px solid #0B2E59 !important;
    border-radius: 6px;
}

[data-testid="stSidebarCollapsedControl"] svg {
    fill: #0B2E59 !important;
    stroke: #0B2E59 !important;
}
</style>

""", unsafe_allow_html=True)

df = pd.read_csv("resources.csv")

df.columns = df.columns.str.strip()

df = df.fillna("")

for col in [
    "Name",
    "Type of Service",
    "County",
    "Address",
    "City",
    "State",
    "Zip Code",
    "Phone",
    "Email"
]:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .replace("nan","")
        )


def clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()

with open("logo.png","rb") as f:
    logo = base64.b64encode(f.read()).decode()

st.markdown(f"""
<div class="header-logo">
    <img src="data:image/png;base64,{logo}">
</div>
""", unsafe_allow_html=True)


st.sidebar.title("Filters")

service_options = sorted(
    [x for x in df["Type of Service"].unique() if x]
)

county_options = sorted(
    [x for x in df["County"].unique() if x]
)

selected_service = st.sidebar.selectbox(
    "Type of Service",
    ["All"] + service_options
)

selected_county = st.sidebar.selectbox(
    "County",
    ["All"] + county_options
)

filtered = df.copy()

if selected_service != "All":
    filtered = filtered[
        filtered["Type of Service"] == selected_service
    ]

if selected_county != "All":
    filtered = filtered[
        filtered["County"] == selected_county
    ]

st.markdown(f"### Showing {len(filtered)} resource(s)")

if filtered.empty:
    st.warning("No matching resources found.")

else:

    grouped = []

    for name, group in filtered.groupby("Name", sort=True):

        services = sorted(
            set(
                x for x in group["Type of Service"]
                if x
            )
        )

        counties = sorted(
            set(
                x for x in group["County"]
                if x
            )
        )

        phones = sorted(
            set(
                x for x in group["Phone"]
                if x
            )
        )

        emails = sorted(
            set(
                x for x in group["Email"]
                if x
            )
        )

        locations = []

        for _, r in group.iterrows():

            pieces = [
                clean(r["Address"]),
                clean(r["City"]),
                clean(r["State"]),
                clean(r["Zip Code"])
            ]

            location = ", ".join(
                [x for x in pieces if x]
            )

            if location and location not in locations:
                locations.append(location)

        grouped.append({
            "Name": name,
            "Services": services,
            "Counties": counties,
            "Locations": locations,
            "Phones": phones,
            "Emails": emails
        })
        

    for resource in grouped:

        with st.container(border=True):

            st.subheader(resource["Name"])

            st.markdown("#### Type(s) of Service")

            for service in resource["Services"]:
                st.markdown(f"• {service}")

            if resource["Locations"]:

                st.markdown("#### Locations")

                for location in resource["Locations"]:
                    st.markdown(f"📍 {location}")

            else:
                st.success(
                    "Virtual / Flexible (Available across all counties)"
                )


            if resource["Counties"]:

                st.caption(
                    "Counties: " +
                    ", ".join(resource["Counties"])
                )

            if resource["Phones"]:

                st.markdown("#### Phone")

                for phone in resource["Phones"]:
                    st.markdown(phone)

            if resource["Emails"]:

                st.markdown("#### Email")

                for email in resource["Emails"]:
                    st.markdown(email)

            st.divider()