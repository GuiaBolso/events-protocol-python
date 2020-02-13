<h1 align="center">events-protocol</h1>
<p align="center">
    <a href="https://github.com/GuiaBolso/events-protocol-python/actions"><img alt="Actions Status" src="https://github.com/GuiaBolso/events-protocol-python/workflows/Black%20Check%20and%20Tests/badge.svg?branch=master"></a>
    <a href="https://github.com/GuiaBolso/events-protocol-python/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
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

