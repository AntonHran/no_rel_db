import pika


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
chanel = connection.channel()

chanel.queue_declare(queue="hello")

message = b"Hello World"
chanel.basic_publish(exchange="", routing_key="hello", body=message)

print(f" [x] Sent '{message}'")
connection.close()
