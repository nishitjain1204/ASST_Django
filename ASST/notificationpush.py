from pyfcm import FCMNotification
import datetime


def notificationsend(reg_ids, title, body, click_action):

    push_service = FCMNotification(
        api_key='notificationkey')
    message_title = title
    message_body = body

    result = push_service.notify_multiple_devices(
        registration_ids=reg_ids, message_title=message_title, message_body=message_body, click_action=click_action)
    return(result['success'])
