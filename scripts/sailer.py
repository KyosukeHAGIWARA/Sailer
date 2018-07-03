import requests
from bs4 import BeautifulSoup as bs
from bottle import route, run, request, static_file
from bottle import TEMPLATE_PATH, jinja2_template as template
from datetime import date
from os import listdir, environ

TEMPLATE_PATH.append("../tmpl")


@route('/')
@route('/first_input')
def prepare():
    print(listdir("./"))

    return template(
        'first_input_page.html',
        today=date.today().strftime("%Y/%m/%d"),
        pic_folder_path="https://www.digimart.net/ad/{0}/".format(date.today().strftime("%Y%m%d")),
        tmpl_list=[f for f in listdir("../tmpl/gen_tmpl")]
    )


@route('/static/<file_path:path>')
def server_static(file_path):
    # print("aaa")
    # print(file_path)
    return static_file(file_path, root='../static/')


@route('/input_fix', method="post")
def input_fix():
    url_list = request.forms.getunicode("url_list").split()
    mail_date = request.forms.getunicode("date")
    pic_folder_path = request.forms.getunicode("pic_folder_path")
    tmpl = request.forms.getunicode("tmpl_select")

    inst_list = [scrape_inst_data(url) for url in url_list]
    print(inst_list)

    return template(
        'input_fix_page.html',
        item_num=len(inst_list),
        inst_list=inst_list,
        date=mail_date,
        pic_folder_path=pic_folder_path,
        tmpl=tmpl
    )


@route('/generate', method="post")
def generate():
    mail_date = request.forms.getunicode("date")
    tmpl = request.forms.getunicode("tmpl")
    item_num = request.forms.getunicode("item_num")
    pic_folder_path = request.forms.getunicode("pic_folder_path")
    print(pic_folder_path)

    inst_list = []
    for i in range(int(item_num)):
        url = request.forms.getunicode("url_{}".format(str(i+1)))
        print(url)
        subject = request.forms.getunicode("subject_{}".format(str(i+1)))
        price_down = request.forms.getunicode("price_down_{}".format(str(i+1)))
        print(price_down)
        inst_list.append([url, subject, price_down])

    return template(
        "gen_tmpl/{}".format(tmpl),
        inst_list=inst_list,
        column_size=int(item_num) // 3,
        pic_folder_path=pic_folder_path,
        mail_date=mail_date
    )


def scrape_inst_data(url):
    r = requests.get(url)
    print(r.status_code)
    soup = bs(r.text, "lxml")

    brand = soup.select(".itemDetailInfo")[0].a.string
    item_name = soup.select(".itemDetailInfo")[0].contents[1][1:]
    subject = "{0} / {1}".format(brand, item_name)
    # print("{0} / {1}".format(brand, item_name))
    full_price = int(soup.select(".fixedPrice")[0].span.string)
    down_prince = int(str(soup.select(".itemStateIn")[0].select(".price")[0].contents[0])[1:])
    down_rate = round((1 - down_prince / full_price) * 100)
    sumb_url = soup.select(".mainPhotoBlock")[0].p.a.get("href")
    print(sumb_url)
    return [
        url,
        subject,
        down_rate,
        sumb_url
    ]


print(environ.get('APP_LOCATION') )

# if environ.get('APP_LOCATION') == 'heroku':
#     run(host="0.0.0.0", port=int(environ.get("PORT", 5000)))
# else:
#     run(host='localhost', port=8080, debug=True)

run(host="0.0.0.0", port=int(environ.get("PORT", 5000)))
