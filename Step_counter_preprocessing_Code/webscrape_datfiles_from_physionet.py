import requests
from bs4 import BeautifulSoup

url = "https://physionet.org/content/ltmm/1.0.0/LabWalks/#files-panel"
r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc,"lxml")
src = []
panel = soup.find("table",class_="files-panel").find_all("a",class_="download")
for p in panel:
    a = p['href']
    a = a.lstrip("/files/")
    a = "https://physionet.org/content/l"+a
    src.append(a)
#print(src)
src_dat = []
for z in src:
    if z.endswith("dat?download"):
        src_dat.append(z)
    else:
        continue
print(src_dat)

for x in src_dat:
    filename = x.split("/")[7].rstrip("?download")
    req = requests.get(x)
    with open(filename,"wb") as f:
        for data in req.iter_content():
            f.write(data)



