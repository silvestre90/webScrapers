'''
Created on 14.02.2018

@author: Sylwester
'''
from tkinter import *
from tkinter import ttk

from bs4 import BeautifulSoup as soup
from selenium import webdriver
import sys


def webScraperStart():
    if (combo.get() != ""):
        if (combo.get() == "Krakow"):
            launchWebScraper(0)
        elif (combo.get() == "Katowice"):
            launchWebScraper(2)
        elif (combo.get() == "Rzeszow"):
            launchWebScraper(1)


def launchWebScraper(cityCode):
    webAddresses = ['x', 'y', 'z']
    webAddresses[
        0] = "https://allegro.pl/kategoria/mieszkania-na-sprzedaz-112739?string=mieszkanie%20krak%C3%B3w&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-hou-1-2-1003"
    webAddresses[
        1] = "https://allegro.pl/kategoria/mieszkania-na-sprzedaz-112739?string=mieszkanie%20rzesz%C3%B3w&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-hou-1-2-1003"
    webAddresses[
        2] = "https://allegro.pl/kategoria/mieszkania-na-sprzedaz-112739?string=mieszkanie%20katowice&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-hou-1-2-1003"

    browser = webdriver.Chrome()

    browser.get(webAddresses[cityCode])
    innerHTML = browser.execute_script("return document.body.innerHTML")

    # html parsing
    page_soup = soup(innerHTML, "html.parser")

    containers = page_soup.find_all("div", {"class": "_7cab484"})
    container = containers[0]

    numberOfPages = page_soup.find_all('li', {'class': "quantity"})
    for nOp in numberOfPages:
        lastPage = int(nOp.a.text)
        print(lastPage)

    filename = "mieszkaniaKrakow.csv"
    f = open(filename, 'wb')

    headers = b"Opis, Link, Cena, Powierzchnia, Cena za metr\n"

    f.write(headers)

    for x in range(1, lastPage):

        webPageAddress = webAddresses[cityCode] + '&p=' + str(x)
        browser.get(webPageAddress)
        innerHTML = browser.execute_script("return document.body.innerHTML")

        page_soup = soup(innerHTML, "html.parser")

        containers = page_soup.find_all("div", {"class": "_7cab484"})
        container = containers[0]

        for container in containers:
            flat = container.h2.text
            linkage = container.h2.a.get('href')
            # print(linkage)

            txt = flat.replace(",", "")
            txt = txt + ',' + linkage
            price_container = container.findAll("div", {"class": "ae47445"})
            for pc in price_container:
                price = pc.span.span.text
                commainPrice = price.index(',')
                price = price[0:commainPrice]
                # price = price.replace(',00 zł', '')
                txt = txt + ',' + price
            # print(price_container)

            details_container = container.find_all("div", {"class": "bec3e46"})
            # print(details_container)
            for dc in details_container:
                area = dc.dl.dd.span.text
                txt = txt + ',' + area

                unitPrice = float(price.replace(' ', '')) / float(area)
                txt = txt + ',' + str(unitPrice)
                # dls = dc.find_all('dl')
                # for dl in dls:
                #     print(dl)

            # print(txt)
            txt = txt.encode(sys.stdout.encoding, errors='replace')
            txt = txt + b'\n'
            f.write(txt)

    f.close()
    browser.close()


window = Tk()

combo = ttk.Combobox(window)
combo.place(x=20, y=30)
combo['values'] = ['Krakow', 'Katowice', 'Rzeszow']

btn = ttk.Button(window, text="OK", command=webScraperStart)
btn.place(x=70, y=80)

window.geometry("200x150")
window.mainloop()
















