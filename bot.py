# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics.aio import TextAnalyticsClient

# Language Resource credentials
endpoint = ""
key = ""    

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        documents = []

        text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        
        documents.append(turn_context.activity.text)

        async with text_analytics_client:
            result = await text_analytics_client.recognize_pii_entities(documents)

        docs = [doc for doc in result if not doc.is_error]

        for idx, doc in enumerate(docs):
            await turn_context.send_activity(f"Document text: {documents[idx]}")
            await turn_context.send_activity(f"Redacted document text: {doc.redacted_text}")
            for entity in doc.entities:
                await turn_context.send_activity ("Entity '{}' with category '{}' got redacted".format(
                    entity.text, entity.category
                ))
        
    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome to the PII Detection Bot")

        