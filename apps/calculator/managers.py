from django.db.models import Manager


class WithoutOtraManager(Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(
            name='-',
        )
