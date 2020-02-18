 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at
 ..   http://www.apache.org/licenses/LICENSE-2.0


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
