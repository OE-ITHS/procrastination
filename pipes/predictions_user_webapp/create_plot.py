import urllib.parse
import matplotlib.pyplot as plt
import io, urllib, base64

def generate_plot(joined_df):
    
    limited_df = joined_df.iloc[:50]

    X = limited_df['dt']

    Y1 = limited_df['oxygen_d1']
    Y2 = limited_df['temp']

    fig = plt.figure()
    fig.set_facecolor('#212529')
    ax1 = fig.add_subplot(111, label='1')
    ax2 = fig.add_subplot(111, label='2', frame_on=False)

    ax1.plot(X, Y1, 'o-b')
    ax1.tick_params(colors='white', which='both')
    ax1.set_ylabel('Oxygen Content (ml/l)', color='b')
    ax1.tick_params(axis='y', colors='b')
    ax1.grid(True, linestyle='--')

    ax2.plot(X, Y2, 'o-r')
    ax2.yaxis.tick_right()
    ax2.tick_params(colors='white', which='both')
    ax2.set_ylabel('Temperature (C)', color='r')
    ax2.yaxis.set_label_position('right')
    ax2.tick_params(axis='y', colors='r')

    img = io.BytesIO()
    fig.savefig(img, format = 'png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())
    return plot_data