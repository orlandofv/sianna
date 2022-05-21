import datetime

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


class Settings(models.Model):
    name = models.CharField(_('Company Name'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    address = models.CharField(_('Address'), blank=True, max_length=255)
    cell = models.CharField(_('Cell'), blank=True, max_length=255)
    cell_2 = models.CharField(_('Cell 2'), blank=True, max_length=255)
    telephone = models.CharField(_('Telephone'), blank=True, max_length=255)
    fax = models.CharField(_('Fax'), blank=True, max_length=255)
    email = models.EmailField(_('Email'))
    web = models.CharField(_('Web Site'), max_length=255, blank=True)
    logo = models.ImageField(_('Logo'), max_length=255, blank=True)
    logo_square = models.ImageField(_('Logo Square'), max_length=255, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, default=timezone.now)
    date_modified = models.DateTimeField(editable=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def get_absolute_url(self):
        return reverse('maintenance_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"
        ordering = ("name",)
    
    def __str__(self):
        return self.name


class Maintenance(models.Model):
    
    ROUTINE = 'Routine'
    PREVENTIVE = 'Preventive'
    CORRECTIVE = 'Corrective'
    PREDECTIVE = 'Predective'

    MAINTENANCE_CHOICES = (
        (ROUTINE, 'Routine'), 
        (PREVENTIVE, 'Preventive'), 
        (CORRECTIVE, 'Corrective'), 
        (PREDECTIVE, 'Predective'), 
    )

    HOURS = 'Hours'
    DAYS = 'Days'
    MONTHS = 'Months'
    KM = 'KM'

    MAINTENANCE_SCHEDULE = (
        (HOURS, 'Hours'), (DAYS, 'Days'), (MONTHS, 'Months'), 
        (KM, 'KM\'s'), 
    )

    name = models.CharField(max_length=50)
    type = models.CharField(choices=MAINTENANCE_CHOICES, default=ROUTINE, max_length=15)
    slug = models.SlugField(unique=True, null=False, editable=False)
    schedule = models.CharField(choices=MAINTENANCE_SCHEDULE, default=HOURS, max_length=10)
    frequency = models.PositiveIntegerField(default=0)
    time_allocated = models.FloatField(default=0)
    time_schedule = models.CharField(choices=MAINTENANCE_SCHEDULE, default=HOURS, max_length=10)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    
    def get_absolute_url(self):
        return reverse('maintenance_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify('{}-{}'.format(self.name, self.type))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenances"
        ordering = ("name",)
        unique_together = ('name', 'type',)

    def __str__(self):
        return '{} ({})'.format(self.name, self.type)


class Component(models.Model):
    component_no = models.PositiveIntegerField(_('System no'), unique=True)
    name = models.CharField(_('Component Name'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    manufacturer = models.CharField(_('Manufacturer'), max_length=100, blank=True)
    stock_code = models.CharField(_('Stock Code'), max_length=100, blank=True)
    maintenance = models.ForeignKey(Maintenance, on_delete=models.PROTECT)
    image = models.ImageField(_('Image'), default="default.jpeg", upload_to = 'media')
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, default=timezone.now)
    date_modified = models.DateTimeField(editable=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('component_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"
        ordering = ("name",)


class Company(models.Model):

    name = models.CharField(_('Company Name'), 
    help_text=_('Name of the Company, Department, etc'), max_length=100, unique=True)
    parent = models.IntegerField(_('Parent Company'), 
    help_text=_('Choose Parent Company'), default=0)
    slug = models.SlugField(unique=True, null=False, editable=False)
    address = models.CharField(blank=True, max_length=255)
    contacts = models.CharField(blank=True, max_length=255)
    manager = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length = 254, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Companies"


class Division(models.Model):

    name = models.CharField(_('Division Name'), 
    help_text=_('Name of the Division, Department, etc'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    address = models.CharField(blank=True, max_length=255)
    contacts = models.CharField(blank=True, max_length=255)
    manager = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length = 254, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('division_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)


class Branch(models.Model):

    name = models.CharField(_('Branch Name'), 
    help_text=_('Name of the Branch, Department, etc'),max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('branch_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Branches"


class Position(models.Model):

    name = models.CharField(_('Position Name'), 
    help_text=_('Name of the Position, Department, etc'),max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('position_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)


class Group(models.Model):
    name = models.CharField(_('Group'), max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def get_absolute_url(self):
        return reverse('group_details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class System(models.Model):
    name = models.CharField(_('System'), max_length=50, unique=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def get_absolute_url(self):
        return reverse('system_details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Type(models.Model):
    name = models.CharField(_('Type'), max_length=50, unique=True)
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def get_absolute_url(self):
        return reverse('type_details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class SubType(models.Model):
    name = models.CharField(_('Subtype'), max_length=50, unique=True)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    def get_absolute_url(self):
        return reverse('subtype_details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


    class Meta(object):
        verbose_name_plural = "Subtypes"


class Vendor(models.Model):

    name = models.CharField(_('Vendor Name'), 
    help_text=_('Name of the Vendor, Department, etc'),max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    address = models.CharField(blank=True, max_length=255)
    contacts = models.CharField(blank=True, max_length=255)
    manager = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length = 254, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vendor_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Vendors"


class Allocation(models.Model):
   
    GOOD = 'Good'
    BROKEN = 'Broken'
    
    STATUS = ((GOOD, 'Good'), (BROKEN, 'Broken'),)

    allocation_no = models.PositiveIntegerField(_("Allocation No."), unique=True) # validators=[RegexValidator(r'^[0-9]{9}$')]
    component = models.ForeignKey(Component,on_delete=models.PROTECT, verbose_name= _('component Name'))
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, verbose_name= _('Vendor Name'))
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    serial_number = models.CharField(_('Component Serial No.'), max_length=50, unique=True)
    status = models.CharField(_('Status'), max_length=15, choices=STATUS, default=GOOD)
    image = models.ImageField(_('Image'), default="default.jpeg", 
    upload_to = 'media', blank=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    purchase_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    date_purchased = models.DateTimeField(default=timezone.now)
    date_allocated = models.DateTimeField(default=timezone.now)
    depreciation = models.FloatField(_('Depreciation %'), default=0)
    start_value_hours = models.FloatField(_('Start Value (Hours)'), default=0)
    start_value_years = models.FloatField(_('Start Value (Years)'), default=0)
    start_value_milliege = models.FloatField(_('Start Value (KM)'), default=0)
    garrantee_value_hours = models.FloatField(_('Warrantee Value (Hours)'), default=0)
    garrantee_value_years = models.FloatField(_('Warrantee Value (Years)'), default=0)
    garrantee_milliege = models.FloatField(_('Warrantee Milliege (KM)'), default=0)
    end_of_life_hours = models.FloatField(_('End of Life (Hours)'), default=0)
    end_of_life_years = models.FloatField(_('End of Life (Years)'),default=0)
    end_of_life_milliege = models.FloatField(_('End of Life (KM)'),default=0)
    warn_before_hours = models.FloatField(_('Warn Before (Hours)'), default=0)
    warn_before_years = models.FloatField(_('Warn Before (Years)'), default=0)
    warn_before_milliege = models.FloatField(_('Warn Before (KM)'), default=0)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    subtype = models.ForeignKey(SubType, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    qrcode = models.ImageField(_('QrCode'), upload_to = 'media', blank=True)

    def __str__(self):
        return str('{} - {}'.format(self.allocation_no, self.component))

    def get_absolute_url(self):
        return reverse('allocation_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify('{}-{}'.format(self.allocation_no, self.component))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Allocations"
        ordering = ("-date_allocated",)


class WorkOrder(models.Model):
    
    PENDING = 'Pending'
    INPROGRESS = 'InProgress'
    ABANDONED = 'Abandoned'
    FINISHED = 'Finished'

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

    STATUSES = ((PENDING, _('Pending')), (INPROGRESS, _('InProgress')),
    (FINISHED, _('Finished')), (ABANDONED, _('Abandoned')))

    PRIORITY = ((LOW, _('Low')), (MEDIUM, _('Medium')), (HIGH, _('High')))

    order = models.PositiveIntegerField(_('Order Number'), unique=True)
    priority = models.CharField(_('Priority'), max_length=10, choices=PRIORITY, default=LOW)
    slug = models.SlugField(unique=True, null=False, editable=False)
    allocation = models.ForeignKey(Allocation, on_delete=models.PROTECT, verbose_name=_('Allocation'))
    responsible = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('Person in Charge'))
    start = models.DateTimeField(_("Start date"), default=timezone.now)
    end = models.DateTimeField(_("End date"), default=timezone.now)
    warn_after = models.DateTimeField(_('Warn After'), default=timezone.now) 
    status = models.CharField(max_length=15, choices=STATUSES, default=PENDING, blank=True)
    progress = models.DecimalField(_('Work Progress (%)'), max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    @property
    def is_overdue(self):
        if self.end < datetime.datetime.now() and self.status in (self.PENDING, self.INPROGRESS):
            return True
        return False
    
    @property
    def is_complete(self):
        if self.progress == 100 or self.status == self.FINISHED:
            return True
        return False
    
    @property
    def is_pending(self):
        if self.status == self.PENDING and not self.is_overdue:
            return True
        return False

    @property
    def is_progress(self):
        if self.status == self.INPROGRESS and not self.is_overdue:
            return True
        return False

    def __str__(self):
        return str('{}'.format(self.order))

    def get_absolute_url(self):
        return reverse('work_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = self.order
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Work Orders"
        verbose_name = "Work Order"
        ordering = ("-start",)


# Maintenance Action
class Action(models.Model):
   
    name = models.CharField(_('Name'), max_length=50, unique=True)
    maintenance = models.ForeignKey(Maintenance, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, null=False, editable=False)
    cost = models.DecimalField(_('Quantity'), decimal_places=2, max_digits=9)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('action_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)


class Item(models.Model):
    cm = 'Cm'
    kg = 'Kg'
    gb = 'Gb'
    mb = 'Mb'
    piece = 'Piece'
    m3 = 'M3'
    km = 'Km'
    lt = 'Lt'
    g = 'G'

    UNITY_CHOICES = ((cm, _('Cm')), (kg, _('Kg')), (lt, _('Lt')),(gb, _('Gb')), 
    (mb, _('Mb')), (piece, _('Piece')), (m3, _('M3')), (km, _('Km')), (g, _('G')))

    name = models.CharField(_('Name'), max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    quantity = models.DecimalField(_('Quantity'), decimal_places=2, max_digits=9)
    unity = models.CharField(_('Unity'), max_length=10, choices=UNITY_CHOICES, default=piece)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)


class MaintenanceItem(models.Model):
    
    maintenance = models.ForeignKey(Maintenance, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.DecimalField(_('Quantity'), decimal_places=2, max_digits=9)
    
    def __str__(self):
        return '{} - {}'.format(self.maintenance, self.item)    

    class Meta:
        verbose_name_plural = "Maintenance Items"
        unique_together = [['maintenance', 'item']]


