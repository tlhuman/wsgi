from bookdb import BookDB

DB = BookDB()


def book(book_id):
    book = DB.title_info(book_id)
    if not book:
        raise NameError
    return "\n".join(["<html>",
                      "<head>",
                      f"<title>{book.get('title')}</title>",
                      f"<h1>{book.get('title')}</h1>"
                      "</head>",
                      "<body>",
                      f"<p><b>Author: </b>{book.get('author')}</p>",
                      f"<p><b>Publisher: </b>{book.get('publisher')}</p>",
                      f"<p><b>ISBN: </b>{book.get('isbn')}</p>",
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


def responce_404():
    return "404 Not Found", "NOT FOUND"


def responce_500():
    "misc errors"
    return "500 Server Error", "INTERNAL SERVER ERROR"


def resolve_path(path):
    funcs = {'': books,
             'book': book,
             }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):

    try:
        request_path = environ.get('PATH_INFO', "")
        if not request_path:
            raise NameError
        func, args = resolve_path(request_path)
        status = "200 OK"
        body = func(*args)
    except NameError:
        status, body = responce_404()
    except Exception as e:
        status, body = responce_500()
        body += f"<span>{str(e)}</span>"

    response_headers = [('Content-Type', 'text/html'),
                        ]
    start_response(status, response_headers)
    return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
