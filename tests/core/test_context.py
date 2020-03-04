import asyncio
from collections import ChainMap
from unittest import TestCase
from uuid import uuid4

from events_protocol.core.context import EventContext, EventContextHolder
from tests.utils.sync import make_sync


class TestEventContextHolder(TestCase):
    @make_sync
    async def test_with_context(self):
        test_event = EventContext(id="my_id", flow_id="my_flow_id", name="test")
        async with EventContextHolder.with_async_context(
            test_event.id, test_event.flow_id, test_event.event_name, test_event.event_version
        ) as event_context:
            self.assertEqual(event_context, test_event)
            self.assertEqual(EventContextHolder.get(), test_event)
        self.assertEqual(EventContextHolder.get(), EventContext())

    def test_multiple_async_context_not_interfering_with_each_other(self):
        _events = list()

        async def event_0():
            first_event = EventContext(id=uuid4(), flow_id=uuid4(), name="test")
            async with EventContextHolder.with_async_context(
                first_event.id,
                first_event.flow_id,
                first_event.event_name,
                first_event.event_version,
            ) as event_context:
                assert EventContextHolder.get() == event_context, "EventContext was wrongly set"
                _events.append({0: EventContextHolder.get()})
                await asyncio.sleep(0.2)

        async def event_1():
            second_event = EventContext(id=uuid4(), flow_id=uuid4(), name="test")
            async with EventContextHolder.with_async_context(
                second_event.id,
                second_event.flow_id,
                second_event.event_name,
                second_event.event_version,
            ) as event_context:
                assert EventContextHolder.get() == event_context, "EventContext was wrongly set"
                _events.append({1: EventContextHolder.get()})

        async def event_2():
            _events.append({2: EventContextHolder.get()})

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[event_0(), event_1(), event_2()])
        )
        for index, item in enumerate(_events):
            _items = list()
            self.assertEqual(index, list(item.keys())[0])
            _items.append(item)
        events = dict(ChainMap(*_events))
        self.assertNotEqual(events.get(0), events.get(1))
        self.assertNotEqual(events.get(0), events.get(2))
        self.assertNotEqual(events.get(1), events.get(2))
