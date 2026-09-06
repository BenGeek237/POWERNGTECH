import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    import os
    os.system('pip install beautifulsoup4')
    from bs4 import BeautifulSoup

session = requests.Session()
url = "https://powerngtech.onrender.com/admin/login/?next=/admin/"
r = session.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

data = {
    'csrfmiddlewaretoken': csrf,
    'username': 'admin@powerngtech.com',
    'password': 'Admin@PowerNG2026!',
    'next': '/admin/'
}
r2 = session.post(url, data=data, headers={'Referer': url})
print("Status:", r2.status_code)
if r2.status_code >= 400:
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    exc_type = soup2.find('th', string='Exception Type:')
    if exc_type:
        print("TYPE:", exc_type.find_next_sibling('td').text)
    exc = soup2.find('pre', class_='exception_value')
    if exc:
        print("VALUE:", exc.text.strip())
