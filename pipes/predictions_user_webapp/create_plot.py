import urllib.parse, io, base64
import matplotlib.pyplot as plt
from datetime import datetime

def generate_plot(joined_df):
    
    limited_df = joined_df.iloc[:50]

    X = [datetime.fromtimestamp(dt) for dt in limited_df['dt']]

    Y1 = [o for o in limited_df['oxygen_d1']]
    Y2 = [(t-273.15) for t in limited_df['temp']]

    fig = plt.figure()
    fig.set_facecolor('#212529')
    ax1 = fig.add_subplot(111, label='1')
    ax2 = fig.add_subplot(111, label='2', frame_on=False)

    ax1.plot(X, Y1, 'o-b')
    ax1.tick_params(colors='white', which='both')
    ax1.set_ylabel('Oxygen Content (ml/l)', color='b')
    ax1.tick_params(axis='y', colors='b')
    ax1.tick_params(axis='x', rotation=30)
    ax1.grid()

    ax2.plot(X, Y2, 'o-r')
    ax2.yaxis.tick_right()
    ax2.tick_params(colors='white', which='both')
    ax2.set_ylabel('Temperature (\N{DEGREE SIGN}C)', color='r')
    ax2.yaxis.set_label_position('right')
    ax2.tick_params(axis='y', colors='r')
    ax2.set_xticklabels([])

    img = io.BytesIO()
    fig.savefig(img, format = 'png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())
    return plot_data