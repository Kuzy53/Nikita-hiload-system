import pika
from cassandra.cluster import Cluster


def db_operations(data):
    cluster = Cluster(["127.0.0.1"])
    con = cluster.connect()

    con.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS my_keyspace WITH REPLICATION = 
        {'class' : 'SimpleStrategy', 'replication_factor' : 1}
        """
    )
    con.execute("USE my_keyspace")

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS parse_result (
            url text PRIMARY KEY,
            person_name text,
            html_code text
        )
        """
    )

    con.execute(
        """
        INSERT INTO parse_result (url, person_name, html_code)
        VALUES (%s, %s, %s)
        """,
        (data["url"], data["person_name"], data["html_code"]),
    )

    cluster.shutdown()


def callback(ch, method, properties, body):
    data = body.decode("utf-8").split("\n")
    parsed_data = {"url": data[0], "person_name": data[1], "html_code": data[2]}

    db_operations(parsed_data)
    print(f"Результат парсинга по {parsed_data['url']} сохранен в базу данных.")


def get_data_from_queue(queue_name="parsed_data_queue"):
    connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1"))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Ожидаю сообщения. Для выхода: CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    get_data_from_queue()
