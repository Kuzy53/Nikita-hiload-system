import pika
import requests
from bs4 import BeautifulSoup


def parse_to_rmq(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    person_name = soup.find("h1").get_text().strip()

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="parsed_data_queue")

    html_code_bytes = str(soup).encode("utf-8")

    message = f"{url}\n" \
              f"{person_name}\n" \
              f"{html_code_bytes}"

    channel.basic_publish(exchange="", routing_key="parsed_data_queue", body=message)

    print(f"Парсинг  по запросу {url} передан в очередь.")

    connection.close()


if __name__ == "__main__":
    parse_url = "https://career.habr.com/alishermadaminov9717"
    parse_to_rmq(parse_url)
