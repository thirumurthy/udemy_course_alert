# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


############## Scraper
import json
import logging
import re
import sys
import threading
import traceback

import sqlite as sql
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import parse_qs, unquote, urlsplit

from config import chat_id, tg_message, bot_url

logging.basicConfig(
    handlers=[logging.FileHandler('udemy.log', 'w', 'utf-8')],
    format='%(levelname)s: %(message)s',
    datefmt='%m-%d %H:%M',
    level=logging.INFO  # CRITICAL ERROR WARNING  INFO    DEBUG    NOTSET
)


def discudemy():
    global du_links
    du_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }

    for page in range(1, 4):
        r = requests.get("https://www.discudemy.com/all/" + str(page), headers=head)
        soup = bs(r.content, "html5lib")
        all = soup.find_all("section", "card")
        big_all.extend(all)

    for index, items in enumerate(big_all):
        try:
            print("Processing  discudemy : " + (str(index + 1)) + " / " + str(len(big_all)) + "")
            title = items.a.text
            url = items.a["href"]

            r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            next = soup.find("div", "ui center aligned basic segment")
            url = next.a["href"]
            r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            du_links.append(title + "|:|" + soup.find("div", "ui segment").a["href"])
        except AttributeError:
            continue
    return du_links


def udemy_freebies():
    global uf_links
    uf_links = []
    big_all = []

    for page in range(1, 3):
        r = requests.get(
            "https://www.udemyfreebies.com/free-udemy-courses/" + str(page)
        )
        soup = bs(r.content, "html5lib")
        all = soup.find_all("div", "coupon-name")
        big_all.extend(all)

    for index, items in enumerate(big_all):
        print("Processing  udemy_freebies : " + (str(index + 1)) + " / " + str(len(big_all)) + "")
        title = items.a.text
        url = bs(requests.get(items.a["href"]).content, "html5lib").find(
            "a", class_="button-icon"
        )["href"]
        link = requests.get(url).url
        uf_links.append(title + "|:|" + link)
    return uf_links


def tutorialbar():
    global tb_links
    tb_links = []
    big_all = []

    for page in range(1, 4):
        r = requests.get("https://www.tutorialbar.com/all-courses/page/" + str(page))
        soup = bs(r.content, "html5lib")
        all = soup.find_all(
            "div", class_="content_constructor pb0 pr20 pl20 mobilepadding"
        )
        big_all.extend(all)

    for index, items in enumerate(big_all):
        print("Processing  tutorialbar : " + (str(index + 1)) + " / " + str(len(big_all)) + "")
        title = items.a.text
        url = items.a["href"]

        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        link = soup.find("a", class_="btn_offer_block re_track_btn")["href"]
        if "www.udemy.com" in link:
            tb_links.append(title + "|:|" + link)
    return tb_links


def real_discount():
    global rd_links
    rd_links = []
    big_all = []

    for page in range(1, 4):
        r = requests.get("https://app.real.discount/stores/Udemy?page=" + str(page))
        soup = bs(r.content, "html5lib")
        all = soup.find_all("div", class_="card-body")
        big_all.extend(all)

    for index, items in enumerate(big_all):
        print("Processing  real_discount : " + (str(index + 1)) + " / " + str(len(big_all)) + "")
        title = items.a.h3.text
        url = "https://app.real.discount" + items.a["href"]
        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        try:
            link = soup.select_one(
                "#panel > div:nth-child(4) > div:nth-child(1) > div.col-lg-7.col-md-12.col-sm-12.col-xs-12 > a"
            )["href"]
            if link.startswith("https://www.udemy.com"):
                rd_links.append(title + "|:|" + link)
        except:
            pass
    return rd_links


def coursevania():
    global cv_links
    cv_links = []
    r = requests.get("https://coursevania.com/courses/")
    soup = bs(r.content, "html5lib")
    nonce = soup.find_all("script")[22].text[30:]
    nonce = json.loads(nonce[: len(nonce) - 6])["load_content"]
    r = requests.get(
        "https://coursevania.com/wp-admin/admin-ajax.php?&template=courses/grid&args={%22posts_per_page%22:%2230%22}&action=stm_lms_load_content&nonce="
        + nonce
        + "&sort=date_high"
    ).json()
    soup = bs(r["content"], "html5lib")
    all = soup.find_all("div", attrs={"class": "stm_lms_courses__single--title"})

    for index, item in enumerate(all):
        print("Processing  coursevania : " + (str(index + 1)) + " / " + str(len(all)) + "")
        title = item.h5.text
        r = requests.get(item.a["href"])
        soup = bs(r.content, "html5lib")
        cv_links.append(
            title
            + "|:|"
            + soup.find("div", attrs={"class": "stm-lms-buy-buttons"}).a["href"]
        )
    return cv_links


def idcoupons():
    global idc_links
    idc_links = []
    big_all = []
    for page in range(1, 4):
        r = requests.get(
            "https://idownloadcoupon.com/product-category/udemy-2/page/" + str(page)
        )
        soup = bs(r.content, "html5lib")
        all = soup.find_all("a", attrs={"class": "button product_type_external"})
        big_all.extend(all)

    for index, item in enumerate(big_all):
        print("Processing  coursevania : " + (str(index + 1)) + " / " + str(len(big_all)) + "")
        title = item["aria-label"]
        link = unquote(item["href"]).split("url=")
        try:
            link = link[1]
        except IndexError:
            link = link[0]
        if link.startswith("https://www.udemy.com"):
            idc_links.append(title + "|:|" + link)
    return idc_links


def create_scrape_obj():
    funcs = {
        "Discudemy": threading.Thread(target=discudemy, daemon=True),
        "Udemy Freebies": threading.Thread(target=udemy_freebies, daemon=True),
        "Tutorial Bar": threading.Thread(target=tutorialbar, daemon=True),
        "Real Discount": threading.Thread(target=real_discount, daemon=True),
        "Course Vania": threading.Thread(target=coursevania, daemon=True),
        "IDownloadCoupons": threading.Thread(target=idcoupons, daemon=True),
    }
    return funcs


def escape_markdown(text: str, version: int = 1, entity_type: str = None) -> str:
    """
    Helper function to escape telegram markup symbols.
    Args:
        text (:obj:`str`): The text.
        version (:obj:`int` | :obj:`str`): Use to specify the version of telegrams Markdown.
            Either ``1`` or ``2``. Defaults to ``1``.
        entity_type (:obj:`str`, optional): For the entity types ``PRE``, ``CODE`` and the link
            part of ``TEXT_LINKS``, only certain characters need to be escaped in ``MarkdownV2``.
            See the official API documentation for details. Only valid in combination with
            ``version=2``, will be ignored else.
    """
    if int(version) == 1:
        escape_chars = r'_*`['
    elif int(version) == 2:
        if entity_type in ['pre', 'code']:
            escape_chars = r'\`'
        elif entity_type == 'text_link':
            escape_chars = r'\)'
        else:
            escape_chars = r'_*[]()~`>#+-=|{}.!'
    else:
        raise ValueError('Markdown version must be either 1 or 2!')

    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)


def send_tg_msg(link, course_name):
    try:

        post_data = {
            "chat_id": chat_id,
            "text": tg_message.replace('URL', escape_markdown(link, 2)).replace('Course_Name',
                                                                                escape_markdown(course_name, 2)),
            "parse_mode": "MarkdownV2",
            "reply_markup": json.dumps({
                "inline_keyboard": [[
                    {
                        "url": link,
                        "text": "Open Udemy"
                    }
                ]]
            })
        }
        final_tg_res = requests.post(bot_url, post_data)
        logging.warning('Posted to TG. Response : ' + final_tg_res.text)
        print("Done...!!!")
    except Exception as ex:
        print(ex)
        logging.exception(ex)


def auto(list_st):
    for index, link in enumerate(list_st):
        tl = link.split("|:|")
        link = tl[1]
        print(link)
        if not sql.check_url_exists(link):
            send_tg_msg(link, tl[0])
            sql.add_udemy(1, link)


if __name__ == '__main__':
    try:
        send_tg_msg("http://google.com", "Google")
        if len(sys.argv) > 0:
            sql.unit_db(True)
        links_ls = []
        all_functions = create_scrape_obj()
        for key in all_functions:
            all_functions[key].start()
        for t in all_functions:
            all_functions[t].join()
            try:  # du_links
                links_ls += du_links
            except:
                pass
            try:  # uf_links
                links_ls += uf_links
            except:
                pass
            try:  # tb_links
                links_ls += tb_links
            except:
                pass
            try:  # rd_links
                links_ls += rd_links
            except:
                pass
            try:  # cv_links
                links_ls += cv_links
            except:
                pass
            try:  # idc_links
                links_ls += idc_links
            except:
                pass

            auto(links_ls)
    except:
        e = traceback.format_exc()
