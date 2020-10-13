import requests
from bs4 import BeautifulSoup


def fetch_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    return requests.get(url, headers=headers)


def find_links(source):
    items = source.find_all("li", {"class": "s-item"})
    result = []
    for item in items:
        links = item.find_all("a", {"class": "s-item__link"})
        if len(links) < 1:
            continue
        result.append(links[0]['href'])
    return result


def get_title(source):
    result = source.find_all("span", {"id": "vi-lkhdr-itmTitl"})
    if len(result) > 0:
        return result[0].text
    else:
        return ""


def get_condition(source):
    result = source.find_all("div", {"class": "u-flL condText"})
    if len(result) > 0:
        return result[0].text
    else:
        return ""


def get_price(source):
    result = source.find_all("span", {"id": "prcIsum"})
    if len(result) > 0:
        return result[0].text
    else:
        return ""


def get_location(source):
    result = source.find_all("div", {"class": "sh-loc"})
    if len(result) > 0:
        return result[0].text.split(': ')[1]
    else:
        return ""


def get_gender(source):
    table = source.find_all("tr")
    for tr in table:
        if "Reparto" in tr.text or "Department" in tr.text:
            row = tr.find_all("td")
            i = 0
            for td in row:
                if "Reparto" in td.text or "Department" in td.text:
                    break
                i = i + 1
            return row[i + 1].text.strip()
    return ""


def get_id(lnk):
    slash = lnk.rfind('/')
    question = lnk.rfind('?')
    if slash != -1 and question != -1:
        id = lnk[slash + 1:question]
        return id
    return ""


def write_csv(**arguments):
    f = open('results/output.csv', 'a')
    f.write(data)
    f.close()


address = "https://www.ebay.it/sch/i.html?_from=R40&_nkw=diesel+jeans&_sacat=0&LH_TitleDesc=0&_pgn=1"
page = fetch_url(address)
print(page.status_code)
src = page.content
soup = BeautifulSoup(src, 'lxml')
links = find_links(soup)
for link in links:
    product_page = fetch_url(link)
    print(product_page.status_code)
    if product_page.status_code == 200:
        product_src = product_page.content
        product_soup = BeautifulSoup(product_src, 'lxml')
        title = get_title(product_soup)
        print("title: " + title)
        condition = get_condition(product_soup)
        print("condition: " + condition)
        price = get_price(product_soup)
        print("price: " + price)
        location = get_location(product_soup)
        print("location: " + location)
        gender = get_gender(product_soup)
        print("gender: " + gender)
        id = get_id(link)
        print("id: " + id)
        print("")
