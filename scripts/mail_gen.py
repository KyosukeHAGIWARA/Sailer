import jinja2 as jj
import requests
from bs4 import BeautifulSoup as bs

def generate_html(data):
    env = jj.Environment(loader=jj.FileSystemLoader('./tmpl'))
    # template = env.get_template('tst.html')
    template = env.get_template('sale_weekly.html')

    disp_text = template.render(data)  # 辞書で指定する

    # ファイルへの書き込み
    tmpfile = open("output/generate.html", 'w', encoding="utf-8")  # 書き込みモードで開く
    tmpfile.write(disp_text)
    tmpfile.close()

def get_request(url):
    r = requests.get(url)
    # print(r.status_code)
    soup = bs(r.text, "lxml")
    return soup

def scrape_inst_data(url):
    soup = get_request(url)

    brand = soup.select(".itemDetailInfo")[0].a.string
    item_name = soup.select(".itemDetailInfo")[0].contents[1][1:]
    subject = "{0} / {1}".format(brand, item_name)
    # print("{0} / {1}".format(brand, item_name))
    full_price = int(soup.select(".fixedPrice")[0].span.string)
    down_prince = int(str(soup.select(".itemStateIn")[0].select(".price")[0].contents[0])[1:])
    down_rate = round((1 - down_prince / full_price) * 100)

    return [
        url,
        subject,
        down_rate
    ]


if __name__ == "__main__":

    url_list = [
        "https://www.digimart.net/cat1/shop60/DS04609778/",
        "https://www.digimart.net/cat1/shop1484/DS04476906/",
        "https://www.digimart.net/cat1/shop343/DS04339351/",
        "https://www.digimart.net/cat3/shop2040/DS04621371/",
        "https://www.digimart.net/cat3/shop5050/DS03807594/",
        "https://www.digimart.net/cat3/shop2040/DS04621741/",
        "https://www.digimart.net/cat2/shop5030/DS04626350/",
        "https://www.digimart.net/cat2/shop5090/DS04588822/",
        "https://www.digimart.net/cat2/shop1140/DS04538325/",
        "https://www.digimart.net/cat16/shop1122/DS04624042/",
        "https://www.digimart.net/cat16/shop1122/DS04624045/",
        "https://www.digimart.net/cat16/shop4781/DS04265114/",
        "https://www.digimart.net/cat6/shop4781/DS04628742/",
        "https://www.digimart.net/cat7/shop4781/DS04627726/",
        "https://www.digimart.net/cat6/shop4781/DS04446388/",
        "https://www.digimart.net/cat12/shop343/DS04126088/",
        "https://www.digimart.net/cat12/shop1484/DS02387722/",
        "https://www.digimart.net/cat12/shop4804/DS04629777/",
        "https://www.digimart.net/cat13/shop4773/DS04600519/",
        "https://www.digimart.net/cat13/shop5017/DS03259916/",
        "https://www.digimart.net/cat13/shop1940/DS04134181/",

    ]

    inst_list = []

    for u in url_list:
        inst_list.append(scrape_inst_data(u))
        # sleep(10)


    d = {
        "inst_list": inst_list,
        "column_size": 7,
        "pic_folder_path": "https://www.digimart.net/ad/20180620/",
        "mail_date": "2018/6/20"
    }  # 辞書で指定する

    generate_html(d)


