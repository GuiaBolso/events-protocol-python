 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

 ..   http://www.apache.org/licenses/LICENSE-2.0

Python API Reference
====================

.. _pythonapi:client:

Client
------
Events are sent through the :class:`~events_protocol.client.event_client.EventClient`, so far we can just use HTTP Layer to transport the event.

HTTP Layer
''''''''''
For now we just have Event transport over HTTP, we just use :class:`~events_protocol.client.http.HttpClient`.

.. _pythonapi:server:

Server
------

Event Register
''''''''''

EventRegister: :class:`~events_protocol.server.handler.event_handler_registry.EventRegister`

Event Handler
'''''''''''''

EventHandler: :class:`~events_protocol.server.handler.event_handler.EventHandler`

Event Processor
'''''''''''''''

EventProcessor: :class:`~events_protocol.server.parser.event_processor.EventProcessor`
