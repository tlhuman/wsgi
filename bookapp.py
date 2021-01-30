import re
import pprint
from bookdb import BookDB

DB = BookDB()


def book(book_id):
    book = DB.title_info(book_id)
    return "\n".join(["<html>",
                      "<head>",
                      f"<title>{book.get('title')}</title>",
                      f"<h1>{book.get('title')}</h1>"
                      "</head>",
                      "<body>",
                      f"<p><b>Author: </b>{book.get('author')}</p>",
                      f"<p><b>Publisher: </b>{book.get('publisher')}</p>",
                      f"<p><b>ISDN: </b>{book.get('isdn')}</p>",
                      "<a href='/'>Home</a>"
                      "</body>",
                      "</html>",
                      ])


def books():
    """get the book titles from the database and put them into html"""
    books = ""
    for b in DB.titles():
        books += f'<li>' \
                 f'<a href="/book/{b.get("id")}">{b.get("title")}</a>' \
                 f'</li>\n'

    return "\n".join(["<html>",
                      "<head>",
                      "<title>A list of some book about stuff</title>",
                      "<h1>Welcome to the books!</h1>"
                      "</head>",
                      "<body>",
                      "<ul>",
                      f"{books}",
                      "</ul>",
                      "</body>",
                      "</html>",
                      ])

def application(environ, start_response):
    status = "200 OK"

    if environ.get('REQUEST_METHOD') == "GET":
        # only two valid path formats
        if environ.get('PATH_INFO') == "/":
            # the root path
            body = books()
        elif re.match("/book/id\d+", environ.get('PATH_INFO')):
            # the book path
            body = book(book_id=environ.get('PATH_INFO').split("/")[-1])
        else:
            # bad path
            status = "404 Not Found"
            body = "NOT FOUND"
    else:
        body = "INVALID REQUEST"

    response_headers = [('Content-Type', 'text/html'),
                        ]
    start_response(status, response_headers)
    return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
