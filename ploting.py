import plotly.express as px
import plotly.io as pio
import pandas as pd
def plot(X,Y,file_name):
    X=int(X)
    Y=int(Y)
    df=pd.read_csv(file_name)
    fig = px.scatter(df,x=df.iloc[:,X],y=df.iloc[:,Y])
# Save the figure as an image file (e.g., PNG)
    pio.write_image(fig, '/home/sorecaffeine/Desktop/Flasktuto/Graphs/plot.png')
    return True