from ast import Try
import pika


class Mqtt:
    def __init__(self, host: str, port: int = 5672) -> None:
        parameters = pika.ConnectionParameters(host=host, port=port)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close(self):
        self.channel.close()
        self.connection.close()


class Listner(Mqtt):
    def callback(self, ch, method, properties, body):
        self.sim(body)

    def listen(self, queue_name: str):
        try:
            self.channel.basic_consume(
                queue=queue_name, on_message_callback=self.callback, auto_ack=True
            )
            self.channel.start_consuming()

        except Exception as e:
            print(e)
            print("could not connect to queue !!!")

    def sim(self, body):
        pass


class Emitter(Mqtt):
    def declare_queue(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name)

    def publish(self, body: str, routing_key: str):
        self.channel.basic_publish(exchange="", routing_key=routing_key, body=body)
