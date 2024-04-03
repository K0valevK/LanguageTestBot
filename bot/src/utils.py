from logs import log, get_current_time


class MockResponse:
    status_code = 500


async def safe_request(f, user_id, *args):
    try:
        return await f(*args)

    except:
        log("errors", timestamp=get_current_time(), user_id=user_id,
            meta_info="WhoKnows", reason="connect", category="database_service")
        return MockResponse()