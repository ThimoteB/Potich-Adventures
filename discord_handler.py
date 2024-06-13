"""Logging into a discord server"""

import logging
from discord import SyncWebhook, Embed, Colour


class DiscordLogHandler(logging.Handler):
    """A custom logging handler that sends logs to a discord webhook"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def emit(self, record):
        webhook = SyncWebhook.from_url(
            "https://discord.com/api/webhooks/1250930698047590421/"
            "q2irfgcUiBe7jkgPVmoL5A7joRORUS9YJhzrQFWgeTSaoVd-xP3sfDhJH08yng3-EUi5"
        )

        level = record.levelname
        message = record.getMessage()

        level_colors = {
            "DEBUG": Colour.light_grey(),
            "INFO": Colour.blue(),
            "WARNING": Colour.gold(),
            "ERROR": Colour.red(),
            "CRITICAL": Colour.dark_red(),
        }

        embed = Embed(
            title=level,
            description=message,
            colour=level_colors.get(level, Colour.default()),
        )

        webhook.send(embed=embed)


if __name__ == "__main__":
    logger = logging.getLogger("discord_logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(DiscordLogHandler())
    logger.info("Hello")
