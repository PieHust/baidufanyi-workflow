# _*_ coding=utf-8 _*_
# A tool for translating.

import sys
import os
import md5
import random
import urllib
from workflow import Workflow, ICON_WEB, web


def get_url(wf):
    """ A function to get the request url."""
    url = 'http://fanyi-api.baidu.com/api/trans/vip/translate'
    appid = os.environ.get('fy_appid') or 'appid'
    secret_key = os.environ.get('fy_secret_key') or 'secret_key'
    from_lang = 'en'
    to_lang = 'zh'
    q = wf.args[0].strip().replace("\\", "")
    if not isinstance(q, unicode):
        q = q.decode('utf8')
    salt = random.randint(32768, 65535)
    sign = appid + q + str(salt) + secret_key
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    url = url + '?appid=' + appid + '&q=' + \
        urllib.quote(q) + '&from=' + from_lang + '&to=' + to_lang + \
        '&salt=' + str(salt) + '&sign=' + sign
    return url


def parse_json(wf, url):
    """ Parse the response content."""
    r = web.get(url)
    result = r.json()
    if 'error_code' in result:
        wf.add_item(title=result['error_msg'],
                    subtitle=result['error_code'],
                    icon=ICON_WEB)
    else:
        wf.add_item(title=result['trans_result'][0]['dst'],
                    subtitle=result['trans_result'][0]['src'],
                    icon=ICON_WEB)
    wf.send_feedback()


def main(wf):
    url = get_url(wf)
    parse_json(wf, url)


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
