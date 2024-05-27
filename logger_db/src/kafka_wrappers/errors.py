from clickhouse import ch_client

import json


query = "INSERT INTO bot.errors VALUES (generateUUIDv4(), '{log_type}', {timestamp}, {user_id}, '{app_ver}', '{meta_info}', '{reason}', '{category}')"


async def errors_clickhouse_wrapper(msg, response_producer):
    message = json.loads(msg.value.decode("ascii"))

    ch_client.execute(query.format(**message))
