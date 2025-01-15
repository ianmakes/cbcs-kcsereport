import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import os

# Load and clean data
file_name = 'CAMP BRETHREN CHRISTIAN SCHOOL KCSE 2024 ANALYSIS.xlsx'
data_path = os.path.join(os.getcwd(), file_name)

if not os.path.exists(data_path):
    raise FileNotFoundError(f"The file '{file_name}' was not found in the current directory: {os.getcwd()}")

# Read the data
df = pd.read_excel(data_path, sheet_name='Sheet1', skiprows=3)

# Rename columns for easier access
df.columns = [
    'Name', 'Sex', 'English', 'Kiswahili', 'Mathematics', 'Biology', 'Chemistry', 'Physics',
    'Geography', 'History', 'CRE', 'Agriculture', 'Business Studies', 'Home Science', 'Computer', 'Points', 'Grade', 'Position'
]

# Remove any rows with completely empty values (likely footnotes or blank spaces)
df.dropna(how='all', inplace=True)

# Initialize the Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1('KCSE 2024 Results Analysis'),
    
    dcc.Tabs([
        dcc.Tab(label='Overall Performance', children=[
            html.Div([
                html.H2('Grade Distribution'),
                dcc.Graph(
                    figure=px.histogram(df, x='Grade', color='Sex', barmode='group', title='Grade Distribution by Gender')
                ),
                html.H2('Points Distribution'),
                dcc.Graph(
                    figure=px.histogram(df, x='Points', title='Distribution of Total Points')
                )
            ])
        ]),

        dcc.Tab(label='Subject Performance', children=[
            html.Div([
                html.Label('Select a Subject:'),
                dcc.Dropdown(
                    id='subject-dropdown',
                    options=[{'label': subject, 'value': subject} for subject in ['English', 'Kiswahili', 'Mathematics',
                                                                                  'Biology', 'Chemistry', 'Physics', 'Geography',
                                                                                  'History', 'CRE', 'Agriculture', 'Business Studies',
                                                                                  'Home Science', 'Computer']],
                    value='English'
                ),
                dcc.Graph(id='subject-graph')
            ])
        ]),

        dcc.Tab(label='Gender Comparison', children=[
            html.Div([
                html.H2('Performance Comparison by Gender'),
                dcc.Graph(
                    figure=px.box(df, x='Sex', y='Points', title='Total Points Distribution by Gender')
                )
            ])
        ])
    ])
])

# Callback for subject performance graph
@app.callback(
    Output('subject-graph', 'figure'),
    [Input('subject-dropdown', 'value')]
)
def update_subject_graph(selected_subject):
    fig = px.histogram(df, x=selected_subject, color='Sex', barmode='group', title=f'{selected_subject} Performance by Gender')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
