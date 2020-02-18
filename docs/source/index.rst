 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at
 ..   http://www.apache.org/licenses/LICENSE-2.0

Events Protocol's Documentation
===========================================

|pypi-version| |build| |docs| |license| |black-codestyle| |pypi-python-version|

.. image:: _static/images/guiabolso-logo.png
    :scale: 100%
    :alt: Guiabolso Logo
    :align: center
    :target: https://www.guiabolso.com.br

Library to be a Client and Server using `Guiabolso's Events Protocol Specification`__, the especification of this implementation can be found here_

.. __: https://www.guiabolso.com.br
.. _here: https://github.com/GuiaBolso/events-protocol

Installation
------------

To install stable version, just download it from  PyPI:

.. code-block:: bash

    pip install events-protocol

To install from source code execute the following command:

.. code-block:: bash

    pip install git+https://github.com/GuiaBolso/events-protocol-python#egg=events-protocol


Basic Usage
===========

Client
------

The essencial information to send an event is:

+-------------+----------------------------------------------+
| Field       | Description                                  |
+=============+==============================================+
| *url*       | URL that was exposed from Event Server       |
+-------------+----------------------------------------------+
| *name*      | Event name registred on Event Server source  |
+-------------+----------------------------------------------+
| *version*   | Event's version                              |
+-------------+----------------------------------------------+
| *payload*   | Payload with necessery event information     |
+-------------+----------------------------------------------+

With this informatons we can send an event.

**Instantiate the client:**

.. code:: python

    from events_protocol.client import EventClient

    client = EventClient(url="http://example.com/events/")


**Send event:**

.. code:: python

    # Exemplo passando apenas as informações essenciais
    response = client.send_event(
        name="event:example",
        version=1,
        payload={
            "example": "example"
        },
    )

**Or you can send the event passing all of the informatons:**

.. code:: python

    response = client.send_event(
        name="event:example",
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
        timeout=1000,
    )

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


Content
-------

.. toctree::
   :maxdepth: 3

   client
   server

.. toctree::
    :maxdepth: 1
    :caption: References

    Python API <_api/index>
    Python API Raw <_api/events_protocol/index>

* :ref:`search`

.. |pypi-version| image:: https://badge.fury.io/py/events-protocol.svg
    :alt: PyPI version
    :target: https://badge.fury.io/py/events-protocol

.. |docs| image:: https://readthedocs.org/projects/events-protocol/badge/?version=latest
    :target: https://events-protocol.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |build| image:: https://github.com/GuiaBolso/events-protocol-python/workflows/Black%20Check%20and%20Tests/badge.svg?branch=master
    :alt: Actions Status
    :target: https://github.com/GuiaBolso/events-protocol-python/actions

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :alt: License
    :target: https://github.com/GuiaBolso/events-protocol-python/blob/master/LICENSE

.. |black-codestyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style: black
    :target: https://github.com/psf/black

.. |pypi-python-version| image:: https://img.shields.io/pypi/pyversions/events-protocol.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/events-protocol/
