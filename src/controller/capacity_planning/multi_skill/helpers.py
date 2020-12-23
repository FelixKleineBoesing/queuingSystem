from src.controller.capacity_planning.helpers import ChannelType, ChannelTypeArguments


class Skill:

    def __init__(self, name: str, channel_type: ChannelType, arguments: dict):
        assert isinstance(channel_type, ChannelType), "The channel type is not defined!"
        assert isinstance(name, str)
        for key, value in arguments.items():
            assert ChannelTypeArguments[channel_type].check_if_item_has_attr(key), \
                "The parameter {} is not possible in channel type: {}".format(key, channel_type)
        self.name = name
        self.channel_type = channel_type
        self.arguments = arguments
