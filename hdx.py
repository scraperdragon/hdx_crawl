import requests
import lxml.html
import os
import scraperwiki
import requests_cache
requests_cache.install_cache("hdx", allowable_methods=["GET", "HEAD"])
auth = (os.environ.get("HDX_USERNAME"),
        os.environ.get("HDX_PASSWORD"))
base_url = "http://data.hdx.rwlabs.org/dataset?page={}"
detail_example = "http://data.hdx.rwlabs.org/dataset/mortality_rate_adult_male"
xlsx_example = "http://manage.hdx.rwlabs.org/hdx/api/exporter/indicator/xlsx/PVH090/source/world-bank/fromYear/1950/toYear/2014/language/en/PVH090_Baseline.xlsx"

page = 1


def get_index_page(page):
    html = requests.get(base_url.format(page), auth=auth).content
    root = lxml.html.fromstring(html)
    root.make_links_absolute(base_url)
    return root.xpath("//h3[@class='list-items dataset-heading']/a/@href")


def get_detail_page(url):
    html = requests.get(url, auth=auth).content
    root = lxml.html.fromstring(html)
    root.make_links_absolute(url)
    return root.xpath("//a[@title='Download']/@href")


def get_download(url):
    try:
        r = requests.head(url, auth=auth)
    except Exception, e:
        return {"url": url,
                "error-msg": str(e),
                "status-code": -1}
    return {"url": url,
            "content-type": r.headers.get('content-type'),
            "status-code": r.status_code}

for page in range(53):
    for detail_url in get_index_page(page):
        for download_url in get_detail_page(detail_url):
            data = get_download(download_url)
            print page, data
            scraperwiki.sql.save(data=data, unique_keys=['url'])



#print get_download(xlsx_example)
#print get_detail_page(detail_example)
#print get_index_page(page)
