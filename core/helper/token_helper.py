from core.model.update_model import UpdateFieldAvro, UpdateAvro
from core.model.token_models import RevokeToken
from core.event.produce_event import produce_event

from core.utils.settings import settings
from core.utils.init_log import logger

from core.enums.token_enum import Role
from datetime import datetime


  
async def emit_update_event(account_updates: UpdateAvro) -> None:
    # Serialize    
    account_updates_event = account_updates.serialize()

    # Emit event
    logger.info('Emitting update account event')
    await produce_event(topic=settings.api_update_account, value=account_updates_event)


async def revoke_refresh_token(data: RevokeToken) -> None:
    # Create database field objs
    tokens_field = UpdateFieldAvro(action='$pull', value={'tokens': data.token})
    last_update_field = UpdateFieldAvro(action='$set', value={'last_update': datetime.utcnow().isoformat()})
    is_active_field = UpdateFieldAvro(action='$set', value={'is_active': False})
    active_device_count_field = UpdateFieldAvro(action='$set', value={'active_device_account': -1})
    active_devices_field = UpdateFieldAvro(action='$pull', value={'active_devices': data.device_ip})
    role_field = UpdateFieldAvro(action='$set', value={'role': {'name': Role.anonymouse.value}})

    # Create update list
    account_updates = UpdateAvro(
        db_metadata={'provider': 'mongoDB', 
                     'database': 'account_db', 
                     'collection': 'accounts'},
        db_filter={'_id': data.id},
        updates=[
            tokens_field, 
            is_active_field, 
            active_device_count_field, 
            active_devices_field, 
            role_field, 
            last_update_field
        ]
    )

    # Emit update event
    await emit_update_event(account_updates=account_updates)
