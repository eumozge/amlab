from bots.core.telegram.commands import Help, Start
from bots.core.telegram.amlab.settings import AMLAB_WELCOME_MESSAGE_SLUG, AMLAB_HELP_MESSAGE_SLUG
from challenges.core.challenge import enqueue_challenge
from bots.models import TelegramUser


class AmlabStart(Start):
    template_slug = AMLAB_WELCOME_MESSAGE_SLUG

    def run(self, write_log=True):
        value = super().run(write_log)
        auth_telegram = TelegramUser.objects.get(user=self.user, bot=self.bot)
        enqueue_challenge(self.user, auth_telegram)
        return value


class AmlabHelp(Help):
    template_slug = AMLAB_HELP_MESSAGE_SLUG
