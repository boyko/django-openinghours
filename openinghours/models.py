from django.db import models
from django.utils.translation import ugettext_lazy as _


WEEKDAYS = (
    ('mon', _('Monday')),
    ('tue', _('Tuesday')),
    ('wed', _('Wednesday')),
    ('thu', _('Thursday')),
    ('fri', _('Friday')),
    ('sat', _('Saturday')),
    ('sun', _('Sunday'))
)


class Rule(models.Model):
    open = models.CharField(verbose_name=_('Opening time'), max_length=5,
                            default='00:00')
    close = models.CharField(verbose_name=_('Closing time'), max_length=5,
                             default='24:00')
    day = models.CharField(max_length=3, choices=WEEKDAYS)
    nr = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = _('Opening hours rule')
        verbose_name_plural = _('Opening hours rules')

    def __str__(self):
        return '{0} {1}-{2}'.format(self.get_day_display(), self.open, self.close)
        
    __unicode__ = __str__
