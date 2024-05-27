from clickhouse import ch_client

import json


query = "INSERT INTO bot.user_journey VALUES (generateUUIDv4(), '{log_type}', {timestamp}, {user_id}, '{app_ver}', '{event_group}', '{event_name}', '{event_data}')"


async def uj_clickhouse_wrapper(msg, response_producer):
    message = json.loads(msg.value.decode("ascii"))

    ch_client.execute(query.format(**message))
