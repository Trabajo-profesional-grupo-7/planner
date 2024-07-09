import json
import os
import urllib.parse
from datetime import datetime

import boto3
import requests

import app.services.plan as srv
from app.config import logging
from app.schema import schemas as dto

logger = logging.get_logger()

NOTIFICATIONS_URL = os.getenv("NOTIFICATIONS_URL")


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = urllib.parse.quote_plus(
    os.getenv("AWS_SECRET_ACCESS_KEY"), safe="/"
)
QUEUE_URL = os.getenv("QUEUE_URL")

sqs = boto3.client(
    "sqs",
    region_name="us-east-2",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def receive_messages():
    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL, MaxNumberOfMessages=1, WaitTimeSeconds=20
        )

        messages = response.get("Messages", [])

        if not messages:
            logger.info("No messages in queue.")
            continue

        for message in messages:
            logger.info(f'Received message from queue: {message["Body"]}')

            plan_dict = json.loads(message["Body"])
            plan_metadata = dto.PlanMetadata(
                user_id=plan_dict["user_id"],
                destination=plan_dict["destination"],
                plan_name=plan_dict["plan_name"],
                init_date=datetime.strptime(plan_dict["init_date"], "%Y-%m-%d"),
                end_date=datetime.strptime(plan_dict["end_date"], "%Y-%m-%d"),
            )

            plan_id = srv.create_plan(plan_metadata)
            logger.info(f"Create plan {plan_id}")

            requests.post(
                f"{NOTIFICATIONS_URL}/notifications/notify",
                json={
                    "user_id": plan_dict["user_id"],
                    "title": "Your plan has been created!",
                    "body": f"Your new plan {plan_dict['plan_name']} has been created. Go check your itinerary!",
                },
            )

            sqs.delete_message(
                QueueUrl=QUEUE_URL, ReceiptHandle=message["ReceiptHandle"]
            )
            logger.info(f'Message deleted: {message["MessageId"]}')
