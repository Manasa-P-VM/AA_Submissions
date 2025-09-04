import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd


#Streamlit App title

st.image("logo.png", caption="Drive Value | Drive Momentum", width=200)

st.header("Submissions prioritization using strike zone")


# Step 1: Generate 1000 normally distributed data points
# Parameters for the Gaussian (normal) distribution for x
mean_x = 0.5  # Mean of x
std_dev_x = 0.20  # Standard deviation of x

# Parameters for the Gaussian (normal) distribution for y
mean_y = 0.5  # Mean of y
std_dev_y = 0.3  # Standard deviation of y

# Number of data points
n_points = 1000

# Generate x and y values from normal distributions
x = np.random.normal(mean_x, std_dev_x, n_points)
y = np.random.normal(mean_y, std_dev_y, n_points)

# Ensure that x and y values are within the range [0.01, 0.99]
x = np.clip(x, 0.01, 0.99)
y = np.clip(y, 0.01, 0.99)

# Step 2: Allow the user to select a segment and randomly select 10 points
segment_options = [
    "Strike Zone (Green)",
    "All Points (Gray)"
]


values_x = st.slider("Select a bind propensity range for strike zone", 0.0, 1.0, (0.5, 1.0))
values_y = st.slider("Select a prospect value range for strike zone", 0.0, 1.0, (0.5, 1.0))


# Step 3: Define the segment ranges
segment_ranges = {
    "Strike Zone (Green)": (values_x[0], values_x[1], values_y[0], values_y[1]),
    "All Points (Gray)": (0, 1, 0, 1)
}


fig = go.Figure()

# Add the "All Points (Gray)" background
fig.add_shape(
    type="rect",
    x0=segment_ranges["All Points (Gray)"][0],
    x1=segment_ranges["All Points (Gray)"][1],
    y0=segment_ranges["All Points (Gray)"][2],
    y1=segment_ranges["All Points (Gray)"][3],
    line=dict(color="gray"),
    fillcolor="gray",
    opacity=0.2,
    layer="below"
)

# Add the "Strike Zone (Green)" background
fig.add_shape(
    type="rect",
    x0=segment_ranges["Strike Zone (Green)"][0],
    x1=segment_ranges["Strike Zone (Green)"][1],
    y0=segment_ranges["Strike Zone (Green)"][2],
    y1=segment_ranges["Strike Zone (Green)"][3],
    line=dict(color="red"),
    fillcolor="green",
    opacity=0.5,
    layer="below"
)

# Add scatter plot with random data
fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker=dict(size=10, color="grey", opacity=0.8),
        name="submissions"
    )
)

# Update layout
fig.update_layout(
    title="Submissions segmented based on Bind Propensity and Prospect Value",
    xaxis_title="Normalized Bind Propensity",
    yaxis_title="Normalized Prospect Value",
    showlegend=False,
    height=600,  # height in pixels
    width=800,    # width in pixels
    template="plotly_dark"
)

#


# Display the scatter plot in Streamlit
st.plotly_chart(fig,use_container_width=True)

st.divider()

st.write("Simulate the impact of submission prioritization")
selected_segment = st.selectbox("Select a segment based on color:", segment_options)


# Get the segment range based on selection
x_min, x_max, y_min, y_max = segment_ranges[selected_segment]

# Step 8: Filter points based on the selected segment
selected_points = [
    i for i in range(n_points)
    if x_min <= x[i] <= x_max and y_min <= y[i] <= y_max
]

# Step 9: Randomly select 10 points from the selected segment
if st.button("Submit"):
    random_selection = np.random.choice(selected_points, 10, replace=False)
    selected_x = np.round(x[random_selection],2)
    selected_y = np.round(y[random_selection],2)
    st.write(f"Randomly selected 10 points from the {selected_segment}:")
    data = {
    'Normalized Bind Propensity Values': selected_x,
    'Normalized Prospect Values': selected_y,
    'Expected Prospect Value': np.round((selected_x * selected_y),2)}
    df=pd.DataFrame(data)
    #st.write("Normalized Bind Propensity Values:", selected_x)
    #st.write("Normalized Prospect Values:", selected_y)
    st.write("Selected values:",df)
    st.subheader(f"Sum of Expected Prospect Value for these points: {round(np.sum(selected_x * selected_y),2)}")
else:
    st.write("No points available in the selected segment.")
