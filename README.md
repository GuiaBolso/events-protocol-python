<h1 align="center">events-protocol</h1>
<p align="center">
    <a href="https://badge.fury.io/py/events-protocol"><img alt="PyPI version" src="https://badge.fury.io/py/events-protocol.svg"></a>
    <a href='https://events-protocol.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/events-protocol/badge/?version=latest' alt='Documentation Status' /></a>
    <a href="https://github.com/GuiaBolso/events-protocol-python/actions"><img alt="Actions Status" src="https://github.com/GuiaBolso/events-protocol-python/workflows/Black%20Check%20and%20Tests/badge.svg?branch=master"></a>
    <a href="https://github.com/GuiaBolso/events-protocol-python/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="https://pypi.org/project/events-protocol/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/events-protocol.svg"></a>
</p>

### Como usar

#### Client

As informações essenciais para enviar o evento são: *url*, *name*, *version* e *payload*.

Apenas com estas informações já é possivel enviar um evento.

```pyt
from events_protocol.client import EventClient

# Instancia o client
client = EventClient(url="http://example.com/events/")

# Exemplo passando apenas as informações essenciais
response = client.send_event(
	name="event:example",
	version=1,
	payload={
		"example": "example"
	},
)

# Exemplo passando todas as informações
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
```

#### Server

Um server é composto por *handler*, *register* e *EventSchema*.

Abaixo se encontra um exemplo de utilização. 


```pyt
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
    payload={"example": "example"},
    identity={"userId": "USER_ID",},
    metadata={"date": "00-00-0000",},
)
input_body = event_input.to_json()

## Apos todos eventos registrados, registre uma rota "/events" no seu framework web de preferência e processe o body utilizando o seguinte comando
response = EventProcessor.process_event(input_body)

```

