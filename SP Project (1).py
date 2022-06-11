#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[10]:


data = pd.read_csv(r'C:\Users\leuro\OneDrive\ZHAW\Wirtschaftsinformatik\14_Scientific Programming\imdb_top_1000.csv', sep=",")
print(data.tail(5))


# In[5]:


film = input("Title: ")
print(film)

movie = data.loc[data.Series_Title==film]
index = data.index[data["Series_Title"]==film].tolist()
print(movie)


# In[6]:


x = ("IMDB Rating", "Metascore")
y = (data._get_value(index[0], "IMDB_Rating"), data._get_value(index[0], "Meta_score")/10)
print(y)
plt.xlim(0, 10)
plt.barh(x, y)
plt.show()


# In[69]:


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
plt.plot(x_Meta, y_IMDB, "r.")


# In[68]:


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
plt.plot(x_Gross2, y_Meta, "b.")

