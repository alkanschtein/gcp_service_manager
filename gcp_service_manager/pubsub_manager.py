from google.cloud import pubsub_v1


class PubSubPublisher:
    def __init__(self, project_id, topic_id):
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def publish_message(self, message, **attributes):
        """Publishes a message to the Pub/Sub topic."""
        message_bytes = message.encode("utf-8")
        future = self.publisher.publish(self.topic_path, message_bytes, **attributes)
        print(f"Published message ID: {future.result()}")


class PubSubSubscriber:
    def __init__(self, project_id, subscription_id):
        self.project_id = project_id
        self.subscription_id = subscription_id
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)

    def callback(self, message):
        """Process the received message."""
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()

    def listen_for_messages(self):
        """Start listening for messages on the subscription."""
        streaming_pull_future = self.subscriber.subscribe(self.subscription_path, callback=self.callback)
        print(f"Listening for messages on {self.subscription_path}...")

        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()

