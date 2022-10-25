from events_protocol.core.views.aiohttp import AIOHTTPHealthCheckView

from events_protocol.core.views.event import EventView

URL_PATTERNS = [(EventView, r"/events"), (AIOHTTPHealthCheckView, r"/health")]