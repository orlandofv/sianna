from django.db import models
from django.utils import timezone
from asset_manager.settings import DATABASES
from users.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify # new
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.utils.functional import lazy


database = DATABASES
db = database['default']['NAME']
usr = database['default']['USER']
psw = database['default']['PASSWORD']
prt = database['default']['PORT']


BROKEN = 0
GOOD = 1
STOLEN = 2

ASSET_STATUSES = ((GOOD, 'Good'), (BROKEN, 'Broken'), (BROKEN, 'Broken'),)
LOCATION_CHOICES = [(0, 'No Parent'),]


def load_locations(cls):
    data = cls.objects.all()
    for d in data:
        LOCATION_CHOICES.append((d.id, d.location_name))

    print(LOCATION_CHOICES)
    return data


class Category(models.Model):
    category_name = models.CharField(_('Category Name'), max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    category_image = models.ImageField(default="default.jpeg", upload_to = 'images/')
    notes = models.TextField(_('Notes'), blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.category_name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("category_name",)
    

class System(models.Model):
    system_name = models.CharField(_('System Name'), max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, 
    verbose_name = _('Category'))
    system_image = models.ImageField(default="default.jpeg", upload_to = 'images/')
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.system_name
        
    def get_absolute_url(self):
        return reverse('system_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.system_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("system_name",)


class Assets(models.Model):
    asset_name = models.CharField(_('Asset Name'), max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name = _('Category'))
    system_id = models.ForeignKey(System, on_delete=models.PROTECT, verbose_name = _('System'))
    slug = models.SlugField(unique=True, null=False, editable=False)
    asset_serial_no = models.CharField(max_length=100, blank=True)
    asset_manufacturer = models.CharField(max_length=100, blank=True)
    date_purchased = models.DateTimeField(default=timezone.now)
    asset_issued = models.BooleanField(default=False, editable=False)
    asset_image = models.ImageField(default="default.jpeg", upload_to = 'images/')
    asset_status = models.IntegerField(_('Asset Status'), default=GOOD, choices=ASSET_STATUSES)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.asset_name

    def get_absolute_url(self):
        return reverse('asset_detail', kwargs={'slug': self.slug})

    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.asset_name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Assets"
        ordering = ("asset_name",)

    
class Location(models.Model):

    location_name = models.CharField(_('Location Name'), 
    help_text=_('Name of the Company, Department, etc'), max_length=100)
    slug = models.SlugField(unique=True, null=False, editable=False)
    parent_location = models.IntegerField(choices=LOCATION_CHOICES, 
    default=0, verbose_name= _('Parent Location (if Any)'))
    location_address = models.CharField(blank=True, max_length=255)
    location_contacts = models.CharField(blank=True, max_length=255)
    location_manager = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.location_name

    def get_absolute_url(self):
        return reverse('location_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.location_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("location_name",)

    
class AssetsIssuance(models.Model):
    asset_id=models.ForeignKey(Assets,on_delete=models.PROTECT, verbose_name= _('Asset Name'))
    asset_location = models.ForeignKey(Location, on_delete=models.PROTECT, 
    verbose_name= _('Location of Asset'))
    date_issued = models.DateTimeField(default=timezone.now)
    asset_assignee = models.ForeignKey(User, on_delete=models.CASCADE, 
    verbose_name= _('Assignee'))
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return str(self.asset_id)

    def get_absolute_url(self):
        return reverse('issuance_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = "Assets Issuance"
        ordering = ("-date_issued",)


@receiver(post_save, sender=Location)
def get_locations(sender, **kwargs):
    data = sender.objects.all()
    for d in data:
        LOCATION_CHOICES.append((d.id, d.location_name))

    print(LOCATION_CHOICES)
    return data
