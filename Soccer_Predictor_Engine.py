import urllib.request
import pandas as pd

"""
Everytime I run this program, I will download the csv file with the latest results.
I will base my analysis on up-to-date results to maximize my prediction engine's accuracy
The csv file will be saved in the same directory as this python file
"""
urllib.request.urlretrieve("http://www.football-data.co.uk/mmz4281/1617/E0.csv", "2016-17.csv")