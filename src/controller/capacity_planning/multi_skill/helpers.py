from src.controller.capacity_planning.helpers import ChannelType


class SkillBuilder:

    def add_skill(self, name: str, channel_type: ChannelType, arguments: dict):
        assert isinstance(channel_type, ChannelType)
        for key, value in arguments.items():
            assert isinstance(key, )


