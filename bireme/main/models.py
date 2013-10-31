#! coding: utf-8
from django.utils.translation import ugettext_lazy as _, get_language
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models

from utils.models import Generic, Country

from main import choices

DECS = 'DeCS'
GENERAL = 'general'
PENDING = 0

# Auxiliar table Type of source [318]
class SourceType(Generic):

    class Meta:
        verbose_name = _("source type")
        verbose_name_plural = _("source types")

    acronym = models.CharField(_("Acronym"), max_length=25, blank=True)
    language = models.CharField(_("Language"), max_length=10, choices=choices.LANGUAGES_CHOICES)
    name = models.CharField(_("Name"), max_length=255)

    def get_translations(self):
        translation_list = ["%s^%s" % (self.language, self.name.strip())]
        translation = SourceTypeLocal.objects.filter(source_type=self.id)
        if translation:
            other_languages = ["%s^%s" % (trans.language, trans.name.strip()) for trans in translation]
            translation_list.extend(other_languages)
        
        return translation_list

    def __unicode__(self):
        lang_code = get_language()
        translation = SourceTypeLocal.objects.filter(source_type=self.id, language=lang_code)
        if translation:
            return translation[0].name
        else:
            return self.name


class SourceTypeLocal(models.Model):

    class Meta:
        verbose_name = _("Translation")
        verbose_name_plural = _("Translations")

    source_type = models.ForeignKey(SourceType, verbose_name=_("Source type"))
    language = models.CharField(_("language"), max_length=10, choices=choices.LANGUAGES_CHOICES)
    name = models.CharField(_("name"), max_length=255)


# Auxiliar table Language of source [317]
class SourceLanguage(Generic):

    class Meta:
        verbose_name = _("Source language")
        verbose_name_plural = _("Source languages")

    acronym = models.CharField(_("Acronym"), max_length=25, blank=True)
    language = models.CharField(_("Language"), max_length=10, choices=choices.LANGUAGES_CHOICES)
    name = models.CharField(_("Name"), max_length=255)

    def get_translations(self):
        translation_list = ["%s^%s" % (self.language, self.name.strip())]
        translation = SourceLanguageLocal.objects.filter(source_language=self.id)
        if translation:
            other_languages = ["%s^%s" % (trans.language, trans.name.strip()) for trans in translation]
            translation_list.extend(other_languages)
        
        return translation_list

    def __unicode__(self):
        lang_code = get_language()
        translation = SourceLanguageLocal.objects.filter(source_language=self.id, language=lang_code)
        if translation:
            return translation[0].name
        else:
            return self.name
    

class SourceLanguageLocal(models.Model):

    class Meta:
        verbose_name = _("Translation")
        verbose_name_plural = _("Translations")

    source_language = models.ForeignKey(SourceLanguage, verbose_name=_("Source language"))
    language = models.CharField(_("Language"), max_length=10, choices=choices.LANGUAGES_CHOICES)
    name = models.CharField(_("Name"), max_length=255)

# Auxiliar table LIS type [302]
class ThematicArea(Generic):

    class Meta:
        verbose_name = _("Thematic area")
        verbose_name_plural = _("Thematic areas")

    acronym = models.CharField(_("Acronym"), max_length=25, blank=True)
    language = models.CharField(_("Language"), max_length=10, choices=choices.LANGUAGES_CHOICES)
    name = models.CharField(_("Name"), max_length=255)

    def get_translations(self):
        translation_list = ["%s^%s" % (self.language, self.name.strip())]
        translation = ThematicAreaLocal.objects.filter(thematic_area=self.id)
        if translation:
            other_languages = ["%s^%s" % (trans.language, trans.name.strip()) for trans in translation]
            translation_list.extend(other_languages)
        
        return translation_list

    def __unicode__(self):
        lang_code = get_language()
        translation = ThematicAreaLocal.objects.filter(thematic_area=self.id, language=lang_code)
        if translation:
            return translation[0].name
        else:
            return self.name

class ThematicAreaLocal(models.Model):

    class Meta:
        verbose_name = _("Translation")
        verbose_name_plural = _("Translations")

    thematic_area = models.ForeignKey(ThematicArea, verbose_name=_("Thematic area"))
    language = models.CharField(_("Language"), max_length=10, choices=choices.LANGUAGES_CHOICES)
    name = models.CharField(_("Name"), max_length=255)



# Main table
class Resource(Generic):

    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")

    STATUS_CHOICES = (
        (0, _('Pending')),
        (1, _('Admitted')),
        (2, _('Refused')),
        (3, _('Deleted')),
    )

    # status (399)
    status = models.SmallIntegerField(_('Status'), choices=STATUS_CHOICES, null=True, default=0)
    # title (311)
    title = models.CharField(_('Title'), max_length=510, blank=False)
    # link (351)
    link = models.TextField(_('Link'), blank=False)
    # originator (313)
    originator = models.TextField(_('Originator'), max_length=255, blank=False)
    # originator_location (314)
    originator_location = models.ManyToManyField(Country, verbose_name=_('Originator location'), blank=False)
    # author (315)
    author = models.TextField(_('Authors'), max_length=255, blank=True, help_text=_("Enter one per line"))
    # language of resource (317)
    source_language = models.ManyToManyField(SourceLanguage, verbose_name=_("Source language"), blank=False)
    # source type (318)
    source_type = models.ManyToManyField(SourceType, verbose_name=_("Source type"), blank=False)
    # abstract (319)
    abstract = models.TextField(_("Abstract"), blank=False)
    # time period (341)
    time_period_textual = models.CharField(_('Temporal range'), max_length=255, blank=True)
    # objective (361)
    objective = models.TextField(_('Objective'), max_length=255, blank=True)
    # responsible cooperative center
    cooperative_center_code = models.CharField(_('Cooperative center'), max_length=55, blank=True)

    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Resource._meta.fields]

    def __unicode__(self):
        return unicode(self.title)


# Relation resource -- thematic areas/ Field lis type (302)
class ResourceThematic(Generic):
    STATUS_CHOICES = (
        (0, _('Pending')),
        (1, _('Admitted')),
        (2, _('Refused')),
    )

    class Meta:
        verbose_name = _("Thematic area")
        verbose_name_plural = _("Thematic areas")

    resource = models.ForeignKey(Resource, related_name='thematics')
    thematic_area = models.ForeignKey(ThematicArea, related_name='+')
    status = models.SmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=PENDING, blank=True)

    def __unicode__(self):
        return unicode(self.thematic_area.name)


# DeCS descriptors table
class Descriptor(Generic):
    STATUS_CHOICES = (
        (0, _('Pending')),
        (1, _('Admitted')),
        (2, _('Refused')),
    )

    class Meta:
        order_with_respect_to = 'resource'

    resource = models.ForeignKey(Resource, related_name='descriptors')
    text = models.CharField(_('Text'), max_length=255, blank=True)
    code = models.CharField(_('Code'), max_length=50, blank=True)
    status = models.SmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=PENDING)

    def __unicode__(self):
        return self.text


# Keywords table
class Keyword(Generic):
    STATUS_CHOICES = (
        (0, _('Pending')),
        (1, _('Admitted')),
        (2, _('Refused')),
    )

    class Meta:
        order_with_respect_to = 'resource'

    resource = models.ForeignKey(Resource, related_name='keywords')
    text = models.CharField(_('Text'), max_length=255, blank=True)
    status = models.SmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=PENDING)
    user_recomendation = models.BooleanField(_('User recomendation?'))

    def __unicode__(self):
        return self.text
