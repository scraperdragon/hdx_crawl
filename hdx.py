import requests
import lxml.html
import os
auth = (os.environ.get("HDX_USERNAME"),
        os.environ.get("HDX_PASSWORD"))
base_url = "http://data.hdx.rwlabs.org/dataset?page={}"
page = 1

def get_index_page(page):
    html = requests.get(base_url.format(page),auth=auth).content
    root = lxml.html.fromstring(html)
    root.make_links_absolute(base_url)
    return root.xpath("//h3[@class='list-items dataset-heading']/a/@href")

print get_index_page(page)
