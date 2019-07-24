# Importing Libraries
print("Importing required libraries...\n")
import bs4 as bs
import lxml
import urllib.request
import os
import numpy as np
import pandas as pd
print("Successfully imported the required libraries.\n")

# Scraping
sauce=urllib.request.urlopen('https://karki23.github.io/Weather-Data/assignment.html')
srccode=bs.BeautifulSoup(sauce,'lxml')
# file = open("data.html","w")
# file.write(str(srccode))

url = "https://karki23.github.io/Weather-Data/"
try:
	os.mkdir("dataset")
	print("Successfully created folder 'dataset' in the cwd.\n")
except:
	print("'dataset' folder already exists. Now, just updating it...\n")
path = os.getcwd() + "\dataset\\"
# print(path)
cities = []
for i in srccode.find_all('a'):
	cities.append(i.get('href')[:-5])
# print(cities)

def extract(element,n):
	cell_list = tr[n].find_all(element)
	item_list = [i.text for i in cell_list]
	return item_list

print("Scraping data from the web and adding it in the following csv files :")
all_data = []
try:
	for city in cities:
		newpath = path + city + ".csv"
		newurl = url + city + ".html"
		try:
			newsauce=urllib.request.urlopen(newurl)
			newsrccode=bs.BeautifulSoup(newsauce,'lxml')
			table = newsrccode.find("table")
			tr = table.find_all('tr')
			data_list = []
			data_list.append(extract('th',0))
			if len(all_data)==0:
				all_data.append(extract('th',0))
			for i in range(1,len(tr)):
				data_list.append(extract('td',i))
				all_data.append(extract('td',i))
			# print(data_list)
			data_array = np.asarray(data_list)
			data_df = pd.DataFrame(data_array)
			data_df.to_csv(newpath)
			print(cities.index(city)+1, end = ". Successfully created : ")
			print(newpath)
		except:
			print("Couldn't scrape for " + city)
except:
	print("Scraping unsuccessful.\n")
else:
	print("\nCreating a merged csv files for all cities...\n")
	all_data_array = np.asarray(all_data)
	all_data_df = pd.DataFrame(all_data_array)
	all_data_df.to_csv(path+"49_Cities.csv")
	print("Successfully created : " + path + "49_Cities.csv")