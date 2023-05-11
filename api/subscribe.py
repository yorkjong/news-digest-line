"""
The module implement a Vercel Serverlesss Function to subscrip topics of news.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/05/04 (initial version) ~ 2023/05/10 (last revision)"

__all__ = [
    'handler',
]

import os
import sys
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import JSONDecodeError

import requests

if __name__ == '__main__':
    sys.path.append('../src')
else:
    # on Vercel environment
    sys.path.append(os.path.join(os.getcwd(), 'src'))

from line import token_status, is_invalid_token
from gdrive import TokenTable, Subscriptions


#------------------------------------------------------------------------------
# handler of the Vercel serverless function
#------------------------------------------------------------------------------

class handler(BaseHTTPRequestHandler):
    '''handler of the Vercel Serverless Function.

    Note: The class name must be handler.
    '''

    def _send_error(self, err_code, err_msg):
        '''Send a error page.

        Args:
            err_code (int): error code to send.
            err_msg (str): error message to send.
        '''
        self.send_response(err_code)    # 401, 404
        self.end_headers()
        self.wfile.write(err_msg.encode())

    def _send_html(self, html):
        '''Send a normal (code 200) HTML page.

        Args:
            html (str): a HTML string to send.
        '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)

        token = params.get('token', [''])[0]
        status = token_status(token)
        target = status.get('target', '')

        if not target:
            self._send_error(status['status'], status['message'])
            return

        tbl = TokenTable('access_tokens.yml')
        name = tbl.gen_unique_name(target, token)
        if name != target:
            # check if the old token is invalid.
            if is_invalid_token(tbl[target]):
                tbl[target] = token     # use new token
                try:
                    tbl.save()
                except Exception as e:
                    self._send_error(423, str(e))
                    return
                name = target

        subs_d = Subscriptions('subscriptions_Daily.yml')
        daily_topics = subs_d.subscribable_topics()
        c = {}  # dict for comments to topics
        c['IT'] = ' (AI, Software)'
        sel_d = lambda x: " selected" if x in subs_d.topics(name) else ""
        options_daily = "\n".join(
            f'{" "*12}<option value="{t}"{sel_d(t)}>{t}{c.get(t, "")}</option>'
            for t in daily_topics)

        subs_w = Subscriptions('subscriptions_Weekly.yml')
        weekly_topics = subs_w.subscribable_topics()
        sel_w = lambda x: " selected" if x in subs_w.topics(name) else ""
        options_weekly = "\n".join(
            f'{" "*4}<option value="{t}"{sel_w(t)}>{t} (Weekly)</option>'
            for t in weekly_topics)

        n_options = len(daily_topics) + len(weekly_topics)

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Subscription to news-digest (token: {token})</title>
    <style>
        #topics {{
            height: auto;
            max-height: 500px;
            overflow-y: scroll;
        }}
    </style>
</head>
<body>
    <h1>Subscription to news-digest</h1>
    <form method="post" action="/api/subscribe">
        <label for="topics">請選取分類後按下訂閱（可複選）：</label><br/><br/>
        <select name="topics" id="topics" multiple size="{n_options}">
{options_daily}
{options_weekly}
        </select>
        <input type="hidden" name="token" value="{token}">
        <input type="hidden" name="target" value="{name}"><br/><br/>
        <input type="submit" value="訂閱">
    </form>
    <div style="background-color: #ffffcc; color: #000000; padding: 10px;">
    請將此頁面加入書籤，以利後續更改訂閱主題
    </div>
</body>
</html>
"""
        self._send_html(html)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        post_params = parse_qs(post_data.decode())

        topics = post_params.get('topics', [])
        token = post_params.get('token', [''])[0]
        target = post_params.get('target', [''])[0]

        if not target:
            self._send_error(401, 'Invalid access token')
            return

        tok_tbl = TokenTable('access_tokens.yml')
        if token not in tok_tbl.tokens():
            name = tok_tbl.add_item(token, target)
            try:
                tok_tbl.save()
            except:
                self._send_error(423, str(e))
                return
        else:
            # use original name
            name = tok_tbl.gen_unique_name(target, token)

        subs_w = Subscriptions('subscriptions_Weekly.yml')
        weekly = subs_w.subscribable_topics()
        topics_daily = [t for t in topics if t not in weekly]
        topics_weekly = [t for t in topics if t in weekly]

        subs_d = Subscriptions('subscriptions_Daily.yml')
        if sorted(topics_daily) != sorted(subs_d.topics(name)):
            subs_d.update_topics(name, topics_daily)
            try:
                subs_d.save()
            except:
                self._send_error(423, str(e))
                return
        if sorted(topics_weekly) != sorted(subs_w.topics(name)):
            subs_w.update_topics(name, topics_weekly)
            try:
                subs_w.save()
            except:
                self._send_error(423, str(e))
                return

        html_topics = "\n".join(f"{' '*4}<li>{topic}</li>" for topic in topics)
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Subscription Result (token: {token})</title>
</head>
<body>
"""
        if topics:
            html += "    <h1>訂閱完成！</h1>\n"
        else:
            html += "    <h1>已取消全部訂閱！</h1>\n"
        html += f"""
    <p>name: {name}</p>
    <p>token: {token}</p>
"""
        if topics:
            html += f"""
    <p>你已訂閱的主題如下:</p>
    <ul>
{html_topics}
    </ul>
"""
        html += "</body>\n</html>\n"
        self._send_html(html)


#------------------------------------------------------------------------------
# Test
#------------------------------------------------------------------------------

def test():
    # Start the HTTP server on port 8080
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, handler)
    print('Starting server...')
    httpd.serve_forever()


if __name__ == '__main__':
    import mock_mode
    mock_mode.init_environ_variables()

    test()

