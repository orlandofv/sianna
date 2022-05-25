from turtle import position
from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify # new
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.utils.functional import lazy
from django.conf import settings


class Tax(models.Model):
    ACTIVE = 1
    DEACTIVATED  = 0
    
    STATUSES = ((ACTIVE, _('Active')), (DEACTIVATED , _('Deactivated')))

    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    rate = models.DecimalField(max_digits=4, decimal_places=2, default=0, unique=True)
    active_status = models.IntegerField(_('Status'), choices=STATUSES, default=ACTIVE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, default=timezone.now)
    date_modified = models.DateTimeField(editable=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tax_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)


class Warehouse(models.Model):
    ACTIVE = 1
    DEACTIVATED  = 0
    
    STATUSES = ((ACTIVE, _('Active')), (DEACTIVATED , _('Deactivated')))

    OPEN = 'OPEN'
    CLOSE = 'CLOSE'

    OPEN_STATUS = ((OPEN, 'Open'), (CLOSE, 'Close'))

    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    parent = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    address = models.CharField(blank=True, max_length=255)
    contacts = models.CharField(max_length=255, blank=True)
    active_status = models.IntegerField(choices=STATUSES, default=ACTIVE)
    open_status = models.CharField(max_length=25, choices=OPEN_STATUS, default=OPEN)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, default=timezone.now)
    date_modified = models.DateTimeField(editable=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('warehouse_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)


class Gallery(models.Model):
    image = models.ImageField(_('Image'), default="default.jpeg", upload_to = 'media')
    date_created = models.DateTimeField(editable=False, default=timezone.now)
    date_modified = models.DateTimeField(editable=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    class Meta:
        verbose_name_plural = 'Gallery'
        ordering = ("-date_created",)


class Product(models.Model):
    ACTIVE = 1
    DEACTIVATED  = 0
    
    STATUSES = ((ACTIVE, _('Active')), (DEACTIVATED , _('Deactivated')))

    FOR_SALE = FOR_PURCHASE = 1
    NOT_FOR_SALE = NOT_FOR_PURCHASE = 0

    TON ='ton'
    KG ='kg'
    G ='g'
    MG ='mg'
    PD ='pound'
    OUNCE ='ounce'

    M = 'm'
    DM = 'dm'
    CM = 'cm'
    MM = 'mm'
    FOOT ='ft'
    INCH ='in'
    
    M2 = 'm2'
    DM2 = 'dm2'
    CM2 = 'cm2'
    MM2 = 'mm2'
    FOOT2 ='ft2'
    INCH2 ='in2'
    
    M3 = 'm3'
    DM3 = 'dm3'
    CM3 = 'cm3'
    MM3 = 'mm3'
    FOOT3 ='ft3'
    INCH3 ='in3'
    LITRE ='litre'
    GALLON = 'gallon'


    WEIGHT_MEASUREMENT_CHOICES = ((KG, _('Kg')), (G, _('G')), (MG, _('MG')), (OUNCE, _('ounce')), 
    (PD, _('pound')), (TON, _('ton')))

    LENGTH_CHOICES = ((M, _('m')), (DM, _('dm')), (CM, _('cm')), (MM, _('mm')), (FOOT, _('ft')), 
    (INCH, _('in')))
    
    AREA_CHOICES = ((M2, _('m²')), (DM2, _('dm²')), (CM2, _('cm²')), (MM2, _('mm²')), (FOOT2, _('ft²')), 
    (INCH2, _('in²')))
    
    VOLUME_CHOICES = ((M3, _('m³')), (DM3, _('dm³')), (CM3, _('cm³')), (MM3, _('mm³')), (FOOT3, _('ft³')), 
    (INCH3, _('in³')), (LITRE, _('litre')), (GALLON, _('gallon')))

    RAW_PRODUCT = 'raw_product'
    MANUFACTURED_PRODUCT = 'manufactured_product'
    
    SELL_STATUSES = ((FOR_SALE, _('For Sale')), (NOT_FOR_SALE, _('Not for Sale')))
    PURCHASE_STATUSES = ((FOR_PURCHASE, _('For Purchase')), (NOT_FOR_PURCHASE, _('Not for Purchase')))

    PRODUCT_NATURE = ((RAW_PRODUCT, _('Raw Product')), (MANUFACTURED_PRODUCT, _('Manufactured Product')))
    
    code = models.CharField(_('Product Code'), max_length=50, unique=True)
    name = models.CharField(_('Name of Product'), max_length=255, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    parent = models.IntegerField(_('Parent Product'), default=0)
    tax = models.ForeignKey(Tax, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('Default Warehouse'), on_delete=models.PROTECT)
    description = models.TextField(_("Detailed Description"), blank=True)
    barcode = models.CharField(_("Barcode"), max_length=255, blank=True)
    sell_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    min_sell_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    sell_price2 = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    sell_price3 = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    sell_price4 = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    sell_price5 = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    purchase_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    max_purchase_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    physical_stock = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    stock_limit = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    desired_stock = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    image = models.ImageField(_('Primary Image'), default="default.jpeg", upload_to = 'media', blank=True)
    product_nature = models.CharField(max_length=50, choices=PRODUCT_NATURE, default=RAW_PRODUCT)
    product_url = models.URLField(max_length=255, blank=True)
    weight = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    length = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    width = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    height = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    length_units = models.CharField(max_length=10, choices=LENGTH_CHOICES, default=M)
    area = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    area_units = models.CharField(max_length=10, choices=AREA_CHOICES, default=M2)
    volume = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    volume_units = models.CharField(max_length=10, choices=VOLUME_CHOICES, default=0)
    weight_units = models.CharField(max_length=50, choices=WEIGHT_MEASUREMENT_CHOICES, default=KG)
    active_status = models.IntegerField(choices=STATUSES, default=ACTIVE)
    sell_status = models.IntegerField(choices=SELL_STATUSES, default=FOR_SALE)
    purchase_status = models.IntegerField(choices=PURCHASE_STATUSES, default=FOR_PURCHASE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, default=timezone.now)
    date_modified = models.DateTimeField(editable=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)

