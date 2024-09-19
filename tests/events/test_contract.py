# from app import events
# from tests.utils import get_published


# async def test_fetch_commitments(make_contract):
#     """Test events.contract.fetch_commitments."""

#     contract = await make_contract()

#     await events.contract.fetch_commitments(contract)

#     published_events = get_published("contract.fetch_commitments")
#     assert 1 == len(published_events)

#     event = published_events[0]
#     assert "v1/contract/" in event["url"]
#     assert str(contract.guid) == event["data"]["contract"]["guid"]


# async def test_new(make_contract):
#     """Test events.contract.new."""

#     contract = await make_contract()

#     await events.contract.new(contract)

#     published_events = get_published("contract.new")
#     assert 1 == len(published_events)

#     event = published_events[0]
#     assert "v1/contract/" in event["url"]
#     assert str(contract.guid) == event["data"]["contract"]["guid"]


# async def test_signed(make_contract):
#     """Test events.contract.signed."""

#     contract = await make_contract(webdox_id="webdox-id")

#     await events.contract.signed(contract)

#     published_events = get_published("contract.signed")
#     assert 1 == len(published_events)

#     event = published_events[0]
#     assert "v1/contract/" in event["url"]
#     assert str(contract.guid) == event["data"]["contract"]["guid"]
#     assert contract.webdox_id == event["data"]["contract"]["webdox_id"]
