import json
import os
import urllib.parse
from datetime import datetime

import boto3
import requests
import services.plan as srv

from app.schema import schemas as dto

NOTIFICATIONS_URL = os.getenv("NOTIFICATIONS_URL")

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = urllib.parse.quote_plus(
    os.getenv("AWS_SECRET_ACCESS_KEY"), safe="/"
)
queue_url = os.getenv("QUEUE_URL")

sqs = boto3.client(
    "sqs",
    region_name="us-east-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)


def receive_messages():
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=20
        )

        messages = response.get("Messages", [])

        if not messages:
            print("No messages in queue.")
            continue

        for message in messages:
            print(f'Received message: {message["Body"]}')

            plan_dict = json.loads(message["Body"])

            plan_metadata = dto.PlanMetadata(
                user_id=plan_dict["user_id"],
                destination=plan_dict["destination"],
                plan_name=plan_dict["plan_name"],
                init_date=datetime.strptime(plan_dict["init_date"], "%d-%m-%Y"),
                end_date=datetime.strptime(plan_dict["end_date"], "%d-%m-%Y"),
            )

            plan_id = srv.create_plan(plan_metadata)
            print(f"Create plan {plan_id}")

            requests.post(
                f"{NOTIFICATIONS_URL}/notifications/notify",
                json={"user_id": plan_id["user_id"], "title": "Plan creado!", "body": f"Tu nuevo plan {plan_dict["plan_name"]} ya ha sido creado. Ve a revisar a tu itinerario!"},
            )

            # Delete the message after processing
            sqs.delete_message(
                QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
            )
            print(f'Message deleted: {message["MessageId"]}')
