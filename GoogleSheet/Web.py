from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Open connection, grabbing the page
my_url = 'https://www.finder.com.au/home-loans/best-home-loans'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#html parsing
# page_soup = soup(page_html, "html.parser")
page_soup = soup(page_html, "html.parser")

# Grab each bank information
dados = {}
for k, body in enumerate(page_soup.findAll('tbody')):
    dados['table' + str(k)] = []
    for tr in body.find_all('tr'):
        tmp = tuple()
        th = tr.find('th')
        if th:
            th = tr.find('th').text.strip()
            tmp += (th,)
        for td in tr.find_all('td'):
            # Only get bank name
            # TODO

            # Get all data
            tmp += (td.text.strip(),)
        dados['table' + str(k)].append(tmp)

print(dados)

# Push data to Googlesheets

