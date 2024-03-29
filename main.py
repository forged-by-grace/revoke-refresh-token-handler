from core.event.consume_event import consume_revoke_token_event
import asyncio

async def main():
    await asyncio.gather(        
        consume_revoke_token_event(), 
    )

asyncio.run(main=main())
