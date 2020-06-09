import rules

from apps.cards.models import Card
from apps.users.models import CustomUser


@rules.predicate
def is_card_owner(user: CustomUser, card: Card):
    return card.user == user


rules.add_perm('apps.cards.is_card_owner', is_card_owner)

