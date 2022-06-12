import urllib.request as urll, json
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from io import BytesIO

#info=[{"Title":"Dummy Movie","Year":"N/A","Rated":"N/A","Released":"N/A","Runtime":"N/A","Genre":"N/A","Director":"N/A","Writer":"N/A","Actors":"N/A","Plot":"N/A","Language":"N/A","Country":"N/A","Awards":"N/A","Poster":"https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png","Ratings":[{"Source":"Internet Movie Database","Value":"7.9/10"},{"Source":"Rotten Tomatoes","Value":"94%"},{"Source":"Metacritic","Value":"79/100"}],"Metascore":"N/A","imdbRating":"N/A","imdbVotes":"N/A","imdbID":"N/A","Type":"N/A","DVD":"N/A","BoxOffice":"N/A","Production":"N/A","Website":"N/A","Response":"True"}]
info=[{"Response":"False","Error":"No Movie searched for yet."},"","",""]

app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def omdb():

    data = pd.read_csv(r'imdb_top_1000.csv', sep=",")

    data = data.dropna(subset=["Meta_score"])
    x_Meta = []
    y_IMDB = []

    for index, row in data.iterrows():
        x_Meta.append(data._get_value(index, "Meta_score"))
        y_IMDB.append(data._get_value(index, "IMDB_Rating"))

    plt.xlabel("Metascore")
    plt.ylabel("IMDB Rating")
    plt.ylim(7, 10)
    plt.xlim(20, 105)
    plt.title("IMDB Rating compared to Metascore")
    plt.plot(x_Meta, y_IMDB, "r.")
    buf2=BytesIO()
    plt.savefig(buf2,format="png")
    file=base64.b64encode(buf2.getbuffer()).decode("ascii")
    info[2]=(file)
    plt.close()

    data = data.dropna(subset=["Gross"])
    x_Gross = []
    x_Gross2 = []
    y_IMDB = []
    y_Meta = []
    xticks = [0, 250000000, 500000000, 750000000, 1000000000]
    xtickslabels = ["0", "250'000'000", "500'000'000", "750'000'000", "1'000'000'000"]
    index = 0

    for index, row in data.iterrows():
        x_Gross.append(data._get_value(index, "Gross"))
        y_IMDB.append(data._get_value(index, "IMDB_Rating"))
        y_Meta.append(data._get_value(index, "Meta_score"))
        
    for i in x_Gross:
        i = int(i.replace(",",""))
        x_Gross2.append(i)
    for i in y_IMDB:
        i = int(i)
    plt.xlabel("Gross")
    plt.ylabel("Metascore")
    plt.ylim(0, 100)
    plt.xlim(0, 1000000000)
    plt.xticks(xticks, xtickslabels)
    plt.title("Metascore compared to gross revenue")
    plt.plot(x_Gross2, y_Meta, "b.")
    buf3=BytesIO()
    plt.savefig(buf3,format="png")
    file=base64.b64encode(buf3.getbuffer()).decode("ascii")
    info[3]=(file)
    plt.close()
    
    if request.method == 'POST':
        title=request.form['title']
        title=title.replace(' ', "+")
        url="http://www.omdbapi.com/?t={}&apikey=b6630343".format(title)
        response = urll.urlopen(url)
        info[0] = json.loads(response.read())


        film=request.form['title']
        try:    
            index = data.index[data["Series_Title"]==film].tolist()

            x = ("IMDB Rating", "Metascore")
            y = (data._get_value(index[0], "IMDB_Rating"), data._get_value(index[0], "Meta_score")/10) 

            plt.xlim(0, 10)
            plt.barh(x, y)
            buf=BytesIO()
            plt.savefig(buf,format="png")
            file=base64.b64encode(buf.getbuffer()).decode("ascii")
            info[1]=(file)
            plt.close()
        except:
            info[1]=("https://auditivohearing.com/front_assets/img/search.png")

        
        return render_template('omdb.html', info=info)
    elif request.method == 'GET':
        return render_template('omdb.html', info=info)


    