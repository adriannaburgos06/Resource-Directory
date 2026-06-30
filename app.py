import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="Resource Directory",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* App */
.stApp {
    background: transparent;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0B2E59;
    padding-top: 20px;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: white !important;
}

[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600;
}

/* Resource cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFF7CC !important;
    border: 1px solid #E6D58C !important;
    border-radius: 12px !important;
    padding: 18px !important;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Selectboxes */
.stSelectbox div[data-baseweb="select"] > div {
    background: white !important;
    color: #0B2E59 !important;
    border: 2px solid #0B2E59 !important;
    border-radius: 6px !important;
}

/* Dropdown */
div[data-baseweb="menu"] {
    background: white !important;
    border: 2px solid #0B2E59 !important;
}

div[data-baseweb="menu"] div[role="option"] {
    color: #0B2E59 !important;
}

div[data-baseweb="menu"] div[role="option"]:hover {
    background: #FFF8D6 !important;
}

/* Sidebar toggle */
[data-testid="stSidebarCollapsedControl"] {
    display: block !important;
    background: white !important;
    border: 2px solid #0B2E59 !important;
    border-radius: 6px;
}

[data-testid="stSidebarCollapsedControl"] svg {
    fill: #0B2E59 !important;
}

/* Hide Streamlit extras */
#MainMenu, footer {
    visibility: hidden;
}

hr {
    border-color: #D8C870 !important;
}

/* Logo */
.header-logo {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

.header-logo img {
    width: 280px;
}

</style>
""", unsafe_allow_html=True)

df = pd.read_csv("resources.csv")
df.columns = df.columns.str.strip()
df = df.fillna("")
df = df.astype(str).apply(lambda x: x.str.strip().replace("nan", ""))

logo = base64.b64encode(open("logo.png", "rb").read()).decode()

st.markdown(f"""
<div class="header-logo">
    <img src="data:image/png;base64,{logo}">
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align:center;color:#0B2E59;'>Resource Directory</h2>",
    unsafe_allow_html=True
)

st.sidebar.title("Filters")

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

filtered = df.copy()

if selected_service != "All":
    filtered = filtered[filtered["Type of Service"] == selected_service]

if selected_county != "All":
    filtered = filtered[filtered["County"] == selected_county]

st.markdown(f"### Showing {len(filtered)} resource(s)")

if filtered.empty:
    st.warning("No matching resources found.")

else:

    grouped = []

    for name, group in filtered.groupby("Name", sort=True):

        grouped.append({
            "Name": name,
            "Services": sorted(set(group["Type of Service"])),
            "Counties": sorted(set(group["County"])),
            "Phones": sorted(set(group["Phone"])),
            "Emails": sorted(set(group["Email"])),
            "Locations": [
                ", ".join([r["Address"], r["City"], r["State"], r["Zip Code"]]).strip(", ")
                for _, r in group.iterrows()
                if any(r[col] for col in ["Address","City","State","Zip Code"])
            ]
        })

    for resource in grouped:

        with st.container(border=True):

            st.subheader(resource["Name"])

            st.markdown("#### Type(s) of Service")
            for s in resource["Services"]:
                st.markdown(f"• {s}")

            if resource["Locations"]:
                st.markdown("#### Locations")
                for loc in resource["Locations"]:
                    st.markdown(f"{loc}")
            else:
                st.success("Virtual / Flexible (Available across all counties)")

            if resource["Phones"]:
                st.markdown("#### Phone")
                for p in resource["Phones"]:
                    st.markdown(p)

            if resource["Emails"]:
                st.markdown("#### Email")
                for e in resource["Emails"]:
                    st.markdown(e)

            st.divider()