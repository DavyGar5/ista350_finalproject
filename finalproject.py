"""""
Name: David Garcia
Date: April 28, 2025
Assignment: FInal Project
Section Leader: Olivia Fernflores
Class: ISTA350
Summary: Create Plots using the baby_names_data.
"""""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import zipfile
import io
import os
from urllib.parse import urljoin
import matplotlib.pyplot as plt


def page(url):
    '''
    Gets the webpage using the URL.
    '''
    r = requests.get(url)
    return r.text

def soup_stuff(html, url):
    '''
    Uses BST to download the baby_names_data.zip file and extract into the project folder.
    '''
    soup = BeautifulSoup(html, "html.parser")
    print(soup)

    for link in soup.find_all("a"):
        href = link.get("href", "")
        if "names.zip" in href:
            zip = urljoin(url, href)
            break

    r = requests.get(zip)
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall("baby_names_data")

def load_data():
    '''
    Takes all the .txt files that were created from the soup_stuff() function and loads them into a dataframe for us to use. Extracting the Year from the file name makes sure that
    the dataframe now includes the year the count was made as ell.
    '''
    folder = r"C:\Users\davyg\OneDrive\Documents\Code_Shit\ISTA350\final_project\baby_names_data"
    babyframe = []

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            df = pd.read_csv(filepath, names=["Name", "Gender", "Count"])
            yr = int(filename[3:7])
            df["Year"] = yr

            babyframe.append(df)
    baby_names = pd.concat(babyframe, ignore_index=True)
    return baby_names

def plot1():
    '''
    Takes the most popular female/male name of 1880 and tracks it's usage from 1880-2023 and plots it in a Scatterplot. Also creates a regression line as well.
    '''
    baby_names = load_data()
    f_1880 = baby_names[(baby_names["Year"] == 1880) & (baby_names["Gender"] == "F")]
    m_1880 = baby_names[(baby_names["Year"] == 1880) & (baby_names["Gender"] == "M")]

    top_f1880 = f_1880.loc[f_1880["Count"].idxmax(), "Name"]
    top_m1880 = m_1880.loc[m_1880["Count"].idxmax(), "Name"]

    fname_data = baby_names[(baby_names["Name"] == top_f1880) & (baby_names["Gender"] == "F")]
    mname_data = baby_names[(baby_names["Name"] == top_m1880) & (baby_names["Gender"] == "M")]

    plt.figure(figsize=(12, 7))
    plt.scatter(fname_data["Year"], fname_data["Count"], label="Name Usage (Female)", color="purple")
    plt.scatter(mname_data["Year"], mname_data["Count"], label="Name Usage (Male)", color="navy")

    f_m,f_b = np.polyfit(fname_data["Year"], fname_data["Count"], 1)
    m_m,m_b = np.polyfit(mname_data["Year"], mname_data["Count"], 1)

    plt.plot(fname_data["Year"], f_m * fname_data["Year"] + f_b, color="red", label="Regression line (Female)", linestyle="--")
    plt.plot(mname_data["Year"], m_m * mname_data["Year"] + m_b, color="blue", label="Regression line (Male)", linestyle="--")

    plt.title(f"Popularity of '{top_f1880}' (Female) and '{top_m1880}' (Male) from 1880 to 2023")
    plt.xlabel("Year (1880-2023)")
    plt.ylabel("Name Count")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot2():
    '''
    Takes the top 5 male/female names from 1880-2023 and plots them onto a histogram alphabetically.
    '''
    baby_names = load_data()

    m_name = baby_names[(baby_names["Gender"] == "M")]
    f_name = baby_names[(baby_names["Gender"] == "F")]

    m_count = m_name.groupby("Name")["Count"].sum()
    f_count = f_name.groupby("Name")["Count"].sum()

    m_top5 = m_count.sort_values(ascending=False).head(5)
    f_top5 = f_count.sort_values(ascending=False).head(5)

    joint = pd.DataFrame({
        "Male": m_top5,
        "Female": f_top5
    })

    f = joint.plot(kind="bar", figsize=(15, 7), color=["Cyan", "Magenta"])
    f.set_title("Top 5 Names (1880-2023)")
    f.set_xlabel("Name")
    f.set_ylabel("Name Count (10^6)")
    f.legend(["Male", "Female"])
    f.grid(axis='y', alpha=0.7)
    plt.xticks(rotation=45)
    plt.show()

def plot3():
    '''
    Creates a trend line to track how many Births happened during a given Year from 1880-2023 to allow us to see what Year has the largest Birth Rate.
    '''

    total = load_data().groupby(["Year", "Gender"])["Count"].sum().unstack()

    plt.figure(figsize=(12, 7))
    plt.plot(total.index, total["M"], label="Male", color="blue")
    plt.plot(total.index, total["F"], label="Female", color="red")

    plt.title("Birth Number by Year (1880–2023)")
    plt.xlabel("Year")
    plt.ylabel("Birth Number")
    plt.legend()
    plt.grid(True)
    plt.show()

    
def main():
    # url = "https://www.ssa.gov/oact/babynames/limits.html"
    # html = page(url)
    # soup_stuff(html,url)

    plot1()
    plot2()
    plot3()

if __name__ == '__main__':
    main()