from src.api.helpers import statuscode_endpoint_wrapper

from src.controller.capacity_planning.backoffice import BackOfficeController
from src.controller.capacity_planning.outbound_phone import OutboundPhoneController
from src.controller.capacity_planning.inbound_chat import InboundChatController
from src.controller.capacity_planning.inbound_phone import InboundPhoneController


@statuscode_endpoint_wrapper
def inbound_phone_get_number_agents_for_service_level(body):
    controller = InboundPhoneController()
    res = controller.get_number_agents_for_service_level(**body)
    return res


@statuscode_endpoint_wrapper
def inbound_phone_get_volume_for_service_level(body):
    controller = InboundPhoneController()
    res = controller.get_volume_for_service_level(**body)
    return res


@statuscode_endpoint_wrapper
def inbound_phone_get_number_agents_for_average_waiting_time(body):
    controller = InboundPhoneController()
    res = controller.get_number_agents_for_average_waiting_time(**body)
    return res


@statuscode_endpoint_wrapper
def inbound_phone_get_volume_for_average_waiting_time(body):
    controller = InboundPhoneController()
    res = controller.get_volume_for_average_waiting_time(**body)
    return res


@statuscode_endpoint_wrapper
def inbound_chat_get_number_agents_for_service_level(body):
    controller = InboundChatController()
    res = controller.get_number_agents_for_service_level(**body)
    return res


@statuscode_endpoint_wrapper
def inbound_chat_get_volume_for_service_level(body):
    controller = InboundChatController()
    res = controller.get_volume_for_service_level(**body)
    return res


@statuscode_endpoint_wrapper
def inbound_chat_get_number_agents_for_average_waiting_time(body):
    controller = InboundChatController()
    res = controller.get_number_agents_for_average_waiting_time(**body)
    return res


@statuscode_endpoint_wrapper
def inbound_chat_get_volume_for_average_waiting_time(body):
    controller = InboundChatController()
    res = controller.get_volume_for_average_waiting_time(**body)
    return res


@statuscode_endpoint_wrapper
def outbound_phone_get_number_agents(body):
    controller = OutboundPhoneController()
    res = controller.get_number_agents(**body)
    return res


@statuscode_endpoint_wrapper
def outbound_phone_get_volume(body):
    controller = OutboundPhoneController()
    res = controller.get_volume(**body)
    return res


@statuscode_endpoint_wrapper
def backoffice_get_number_agents(body):
    controller = BackOfficeController()
    res = controller.get_number_agents(**body)
    return res


@statuscode_endpoint_wrapper
def backoffice_get_volume(body):
    controller = BackOfficeController()
    res = controller.get_volume(**body)
    return res