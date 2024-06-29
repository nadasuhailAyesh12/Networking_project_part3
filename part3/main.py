 # noqa
import csv
from socket import socket, AF_INET, SOCK_STREAM
from urllib.parse import unquote

# helper functions to  make code neater these helpers to read files as binary ,
# read csv files
# , generate sorted laptops tables ,generate 404 page content


def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


def read_csv_file():
    with open("./laptops.csv", mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        return rows


def generate_sorted_rows_table(sorted_rows, sorting_key, total_price=None):
    html_table = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Laptops Table</title>
                    <style>
                        h1 {{
                            text-align: center;
                        }}
                        table {{
                            width: 40%;
                            border-collapse: collapse;
                            margin: auto;
                        }}
                        th, td {{
                            padding: 10px;
                            text-align: left;
                            border-bottom: 1px solid #ddd;
                        }}
                        td:first-child {{
                            background-color: hsl(195, 65.8%, 64.7%);
                        }}
                        th {{
                            background-color: hsl(195, 65.8%, 64.7%);
                        }}
                    </style>
                    </head>
                    <body>
                    <h1>Sort by {sorting_key}</h1>
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Price</th>
                            </tr>
                        </thead>
                        <tbody>
                    """
    for row in sorted_rows:
        html_table += f"""
                        <tr>
                            <td>{row['name'].upper()}</td>
                            <td>${row['price']}</td>
                        </tr>
            """
    if total_price is not None:
        html_table += f"""
                        <tr>
                            <td style='background-color:gray;'><strong>Total Price:</strong></td>
                            <td style='background-color:gray;'>${total_price}</td>
                        </tr>
        """

    html_table += """
                    </tbody>
                </table>
            </body>
        </html>
        """
    return html_table

def generate_404_content(client_address):
    return f"""
    <html>
        <head>
            <title>Error 404</title>
        </head>
       <body style='display:flex; flex-direction:column;justify-content:center;
       align-items:center;'>
        <div class="container"  style='display:flex; flex-direction:column;
        justify-content:center;align-items:center;text-align:center;'>

        <img src="https://i.postimg.cc/2yrFyxKv/giphy.gif" alt="gif_ing" />

       <div style=' display:flex;flex-direction:column;align-items:center'>
        <h1 style="color:red;">The file is not found.</h1>

            <p><b>Nada Ayesh _220200628</b></p>
            <p><b>Abeer Abu Jayyab _ 220204180/b></p>

            <br>
              <div style='display:flex;'>
            <p> Client IP:{client_address[0]} </p>
            <p> _ Client Port:{client_address[1]} </p>
            </div>
            <br>
            <a href='/main_en.html'>
            <button style="background-color:black;color:white;padding: 15px 32px;"> go Home</button>
            </a>
            </div>
    </div>
        </body>
    </html>
    """.encode('utf-8')

# Function to sort by name ,and by price


def sort_by_name():
    laptops = read_csv_file()
    sorted_laptops = sorted(laptops, key=lambda x: x['name'])
    html_table = generate_sorted_rows_table(sorted_laptops, 'Name')
    return html_table


def sort_by_price():
    laptops = read_csv_file()
    sorted_laptops = sorted(laptops, key=lambda x: float(x['price'].replace('$', '').replace(',', '')))
    total_price = sum(float(laptop['price'].replace('$', '').replace(',', '')) for laptop in sorted_laptops)
    html_table = generate_sorted_rows_table(sorted_laptops, 'Price', total_price)
    return html_table

# Functions to handle all incoming requests and respond depending on the endpoint
# I read the you want me to satisfy rfc2616 so I make the following:
# I add status line with the status code and the status phrase
# I add custom header with content type finsihed with \r\n to sperate from response body
# I add response body

def handle_request(request, client_address):
    headers = request.split('\r\n')
    # first get the first_line which has the method and the endpoint
    if not headers:
        return None

    first_line_parts = headers[0].split(' ')
    if len(first_line_parts) < 2:
        return None
    first_line = headers[0].split()
    # get the endpoint which is the path
    path = unquote(first_line[1])
    # start handeling based on requiremnets
    if path == '/' or path == '/index.html' or path == '/main_en.html' or path == '/en':
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n\r\n'
        response_body = read_file('main_en.html')
    elif path == '/ar':
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Language: ar\r\n\r\n'
        response_body = read_file('main_ar.html')
    # here as what I understood that you need if the file not found send random one
    elif path.endswith('.html'):
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n\r\n'
        try:
            response_body = read_file(path.lstrip('/'))
        except FileNotFoundError:
            response_body = read_file('randomPage.html')
    elif path.endswith('.css'):
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n'
        try:
            response_body = read_file(path.lstrip('/'))
        except FileNotFoundError:
            response_body = read_file('randomPage.css')
    elif path.endswith('.png'):
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n'
        try:
            response_body = read_file(path.lstrip('/'))
        except FileNotFoundError:
            response_body = read_file('randomImage2.png')
    elif path.endswith('.jpg'):
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n'
        try:
            response_body = read_file(path.lstrip('/'))
        except FileNotFoundError:
            response_body = read_file('randomImage1.jpg')
    # Here I want to respond with the generated tables
    elif path == '/SortByName':
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
        response_body = sort_by_name().encode('utf-8')
    elif path == '/SortByPrice':
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
        response_body = sort_by_price().encode('utf-8')
    # Here the redirecting requirements and I set the response body to no-content
    elif path == '/azn':
        response_headers = 'HTTP/1.1 307 Temporary Redirect\r\nLocation: https://www.amazon.com\r\n\r\n'
        response_body = b''
    elif path == '/so':
        response_headers = 'HTTP/1.1 307 Temporary Redirect\r\nLocation: https://www.stackoverflow.com\r\n\r\n'
        response_body = b''
    elif path == '/bzu':
        response_headers = 'HTTP/1.1 307 Temporary Redirect\r\nLocation: https://www.birzeit.edu\r\n\r\n'
        response_body = b''
    # Here not of our custom endpoints so not found
    else:
        response_headers = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
        response_body = generate_404_content(client_address)
    # for all request I send the custom headers and the body
    return response_headers.encode('utf-8') + response_body

# here I start the server by creating TCP socket then bind it to our host ,port
# then I accept the connection , recieve requests and send the response to the client
# I used utf-8 to encoding and decoding
# finally I close the connection and the socket


def start_server(host='localhost', port=44551):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'The server is ready to receive {host}:{port}')

    while True:
        try:
            connection_socket, client_address = server_socket.accept()
            request = connection_socket.recv(2048).decode('utf-8')
            print(f'The HTTP Request  is : {request}')
            response = handle_request(request, client_address)
            if response:
                connection_socket.sendall(response)
        except OSError:
            print("IO error")
        finally:
            connection_socket.close()


if __name__ == '__main__':
    start_server()
