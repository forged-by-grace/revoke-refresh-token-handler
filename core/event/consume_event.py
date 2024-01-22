from core.helper.consumer_helper import consume_event
from core.utils.settings import settings
from core.utils.init_log import logger
from core.helper.token_helper import revoke_refresh_token
from core.model.token_models import RevokeToken

# Processing event msg
event_processing_msg = "Processing event"

async def consume_revoke_token_event():
    # consume event
    consumer = await consume_event(topic=settings.api_revoke_refresh_token, group_id=settings.api_revoke_refresh_token)
    
    try:
        # Consume messages
        async for msg in consumer: 
            logger.info('Received revoke refresh token event.') 
            
            # Deserialize event
            revoke_token_data = RevokeToken.deserialize(data=msg.value)
            
            # revoke token
            logger.info(event_processing_msg)
            await revoke_refresh_token(data=revoke_token_data)
    except Exception as err:
        logger.error(f'Failed to process event due to error: {str(err)}')
    finally:
        await consumer.stop()
