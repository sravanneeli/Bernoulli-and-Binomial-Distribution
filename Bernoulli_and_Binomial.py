from scipy.stats.stats import mode
import streamlit as st
import numpy as np
from scipy.stats import bernoulli
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from math import comb
from plotly.subplots import make_subplots


st.write("""
# [Bernoulli Distribution](https://en.wikipedia.org/wiki/Bernoulli_distribution)
""")

st.sidebar.header("INPUT PARAMETERS")
# Select Success Probability with stream lit slider
prob_success = st.sidebar.slider(label='Select Probability of Success(P)', min_value=0.0, max_value=1.0, step=0.1)

col1, col2 = st.columns(2)

col1.metric("Success Probability", prob_success)
col2.metric("Failure Probability", round(1-prob_success, 1))

# Number of samples to be drawn from bernouli distrubtion
num_samples = st.sidebar.slider(label="Number of Samples", min_value=10, max_value=10000, step=10)

# Bernouli Distribution
R = bernoulli.rvs(prob_success, 1-prob_success, size = num_samples)

# Dataframe for the success and failure counts
rdf = pd.DataFrame(R, columns=['Distribution'])

# Map 0's and 1's to Failure and Success
rdf['Distribution'] = rdf['Distribution'].map({0: 'Failure', 1: 'Sucess'})

# Plot as Probability Density Function 
fig =px.histogram(rdf, x='Distribution', histnorm='probability density', color_discrete_sequence=['blue'])

fig.update_layout(bargap=0.5)

st.plotly_chart(fig)


st.write("""
# [Binomial Distribution](https://en.wikipedia.org/wiki/Binomial_distribution)
""")

# Number of Individual Bernouli Trails
num_trails = st.sidebar.slider(label="Number of Independent Bernoulli Trails", min_value=2, max_value=100, step=1)

pdf_binomial = []

for i in range(num_trails+1):
    pdf_binomial.append(comb(num_trails, i) * (prob_success**i) * ((1-prob_success)**(num_trails-i)))

cumulative_sum = []

temp = 0

for prob in pdf_binomial:
    temp += prob
    cumulative_sum.append(temp)

# print(cumulative_sum)
# Dataframe for the Distribution
pdf_binomial = pd.DataFrame(pdf_binomial, columns=['Distribution'])

# print(pdf_binomial)

# Plot both Probability Density Function and Cummilative Function
fig = make_subplots(rows=1, cols=2, subplot_titles=("Probability Density Function", "Cummilative Density Function"))

fig.add_trace(go.Scatter(x=list(range(0, num_trails+1)), y=pdf_binomial['Distribution'],
                    mode='lines+markers', marker_color='red', marker_line_color='midnightblue'), row=1, col=1)

fig.add_trace(go.Scatter(x=list(range(0, num_trails+1)), y=cumulative_sum,
                    mode='lines+markers', marker_color='blue', marker_line_color='midnightblue'), row=1, col=2)


st.write(fig)
