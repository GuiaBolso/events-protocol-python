 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at
 ..   http://www.apache.org/licenses/LICENSE-2.0


Server
------

An Event Server is composed by:

+-----------------+------------------------------------------------------------+
| Component       | Description                                                |
+=================+============================================================+
| *handler*       | Class that will receive and process the event              |
+-----------------+------------------------------------------------------------+
| *register*      | Class that will register the handler to Event Discovery    |
+-----------------+------------------------------------------------------------+
| *EventSchema*   | Event Schema will be accepted in the *payload* attribute   |
+-----------------+------------------------------------------------------------+

Example:

.. code:: python

    from events_protocol.server.handler.event_handler_registry import EventRegister
    from events_protocol.core.builder import EventBuilder, Event
    from events_protocol.core.model.base import CamelPydanticMixin
    from events_protocol.core.model.event import Event, ResponseEvent
    from events_protocol.server.handler.event_handler import EventHandler
    from events_protocol.server.parser.event_processor import EventProcessor


    class MyEventSchema(CamelPydanticMixin):
        example: str


    class MyHandler(EventHandler):
        _SCHEMA = MyEventSchema

        @classmethod
        def handle(cls, event: Event) -> ResponseEvent:
            payload = cls.parse_event(event)
            response = {"MyEventPayload": payload.example}
            return EventBuilder.response_for(event, response)


    class MyEventRegister(EventRegister):
        event_name = "get:event:example"
        event_version = 1
        event_handler = MyHandler


    MyEventRegister.register_event()

    event_input = Event(
        name="get:event:example",
        version=1,
        id="9230c47c-3bcf-11ea-b77f-2e728ce88125",
        flow_id="a47830ca-3bcf-11ea-a232-2e728ce88125",
        payload={
            "example": "example"
        },
        identity={
            "userId": "USER_ID",
        },
        metadata={
            "date": "00-00-0000",
        },
    )
    input_body = event_input.to_json()

    response = EventProcessor.process_event(input_body)
