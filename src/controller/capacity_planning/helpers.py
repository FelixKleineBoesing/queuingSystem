from aenum import Enum
import inspect
from src.controller.capacity_planning.single_skill.backoffice import BackOfficeController, BackOfficeArguments
from src.controller.capacity_planning.single_skill.helpers import Arguments
from src.controller.capacity_planning.single_skill.inbound_chat import InboundChatController, InboundChatArguments
from src.controller.capacity_planning.single_skill.inbound_phone import InboundPhoneController, InboundPhoneArguments
from src.controller.capacity_planning.single_skill.outbound_phone import OutboundPhoneController, OutboundPhoneArguments


class ChannelType(Enum):
    backoffice = 0
    inbound_chat = 1
    inbound_phone = 2
    outbound_phone = 3


class ChannelTypeToControllerMapper:
    backoffice = BackOfficeController()
    inbound_chat = InboundChatController()
    inbound_phone = InboundPhoneController()
    outbound_phone = OutboundPhoneController()


class ChannelTypeArguments(Arguments):
    backoffice = BackOfficeArguments()
    inbound_chat = InboundChatArguments()
    inbound_phone = InboundPhoneArguments()
    outbound_phone = OutboundPhoneArguments()
