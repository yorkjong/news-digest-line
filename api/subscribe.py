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

from gdrive import TokenTable, Subscriptions


#------------------------------------------------------------------------------
# Token Status (Line Notify)
#------------------------------------------------------------------------------

def token_status(token):
    '''Check status of a Line Access Token.

    Args:
        token (str): line access token

    Returns:
        (dict): a dictionary of the reponsed JSON
    '''
    url = 'https://notify-api.line.me/api/status'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    resp = requests.get(url, headers=headers)
    try:
        return resp.json()
    except JSONDecodeError:
        print('Response could not be serialized')
        return {}


def token_target(token):
    '''Get target of a Line Access Token.

    Args:
        token (str): line access token

    Returns:
        (str): the target (e.g., the user name or the group name)
    '''
    return token_status(token).get('target', '')


#------------------------------------------------------------------------------
# handler of the Vercel serverless function
#------------------------------------------------------------------------------

class handler(BaseHTTPRequestHandler):
    '''handler of the Vercel Serverless Function.

    Note: The class name must be handler.
    '''

    def _send_error(self, err_code, err_msg):
        self.send_response(err_code)    # 401, 404
        self.end_headers()
        self.wfile.write(err_msg.encode())

    def _send_html(self, html_body):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_body.encode())

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
            # in case of regenerating tokens.
            if token_status(tbl[target]).get('status') != 200:
                tbl[target] = token
                try:
                    tbl.save()
                except Exception as e:
                    self._send_error(423, str(e))
                    return
                name = target

        daily_topics = (
            ("Tesla & SpaceX; Vehicle", ""),
            ("Tech Industry", ""),
            ("Finance", ""),
            ("Taiwan", ""),
            ("Crypto", ""),
            ("IT", " (AI, Software)"),
        )
        weekly_topics = (
            ("Science & Technology", " (Weekly)"),
            ("Health & Food", " (Weekly)"),
        )
        n_options = len(daily_topics) + len(weekly_topics)


        topics = Subscriptions('subscriptions_Daily.yml').topics(name)
        sel = lambda x: " selected" if x in topics else ""
        options_daily = "\n".join(
            f'{" "*12}<option value="{t}"{sel(t)}>{t}{c}</option>'
            for t, c in daily_topics)
        topics = Subscriptions("subscriptions_Weekly.yml").topics(name)
        options_weekly = "\n".join(
            f'{" "*12}<option value="{t}"{sel(t)}>{t}{c}</option>'
            for t, c in weekly_topics)

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Subscription to news-digest (token: {token})</title>
            <style>
                #topics {{
                    height: {n_options+2}em;
                }}
            </style>
        </head>
        <body>
            <h1>Subscription to news-digest</h1>
            <form method="post" action="/api/subscribe">
                <label for="topics">請選取分類後按下訂閱（可複選）：</label><br/><br/>
                <select name="topics" id="topics" multiple>
        {options_daily}
        {options_weekly}
                </select>
                <input type="hidden" name="token" value="{token}">
                <input type="hidden" name="target" value="{name}"><br/><br/>
                <input type="submit" value="訂閱">
            </form>
        </body>
        </html>
        """
        self._send_html(html_body)

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

        weekly = ["Science & Technology", "Health & Food"]
        topics_daily = [t for t in topics if t not in weekly]
        topics_weekly = [t for t in topics if t in weekly]

        subs_d = Subscriptions('subscriptions_Daily.yml')
        if topics_daily != subs_d.topics(name):
            subs_d.update_topics(name, topics_daily)
            try:
                subs_d.save()
            except:
                self._send_error(423, str(e))
                return
        subs_w = Subscriptions('subscriptions_Weekly.yml')
        if topics_weekly != subs_w.topics(name):
            subs_w.update_topics(name, topics_weekly)
            try:
                subs_w.save()
            except:
                self._send_error(423, str(e))
                return

        html_topics = "\n".join(f"{' '*8}<li>{topic}</li>" for topic in topics)
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Subscription Result (token: {token})</title>
        </head>
        <body>
        """
        if topics:
            html_body += "<h1>訂閱完成！</h1>"
        else:
            html_body += "<h1>已取消全部訂閱！</h1>"
        html_body += f"""
            <p>name: {name}</p>
            <p>token: {token}</p>
        """
        if topics:
            html_body += f"""
                <p>你已訂閱的主題如下:</p>
                <ul>
            {html_topics}
                </ul>
            """
        html_body += """
        </body>
        </html>
        """
        self._send_html(html_body)


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

