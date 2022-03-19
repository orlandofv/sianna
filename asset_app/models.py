from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify # new
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.utils.functional import lazy

BROKEN = 0
GOOD = 1
STOLEN = 2

ASSET_STATUSES = ((GOOD, 'Good'), (BROKEN, 'Broken'), (BROKEN, 'Broken'),)
LOCATION_CHOICES = [(0, 'No Parent'),]


class Maintenance(models.Model):
    ROUTINE = 1
    PREVENTIVE = 2
    CORRECTIVE = 3
    PREDECTIVE = 4

    MAINTENANCE_CHOICES = (
        (ROUTINE, 'Routine'), 
        (PREVENTIVE, 'Preventive'), 
        (CORRECTIVE, 'Corrective'), 
        (PREDECTIVE, 'Predective'), 
    )

    HOURS = 1
    DAYS = 2
    MONTHS = 3
    KM = 4

    MAINTENANCE_SCHEDULE = (
        (HOURS, 'Hours'), (DAYS, 'Days'), (MONTHS, 'Months'), 
        (KM, 'KM\'s'), 
    )

    maintenance_name = models.CharField(max_length=50)
    maintenance_type = models.IntegerField(choices=MAINTENANCE_CHOICES, default=ROUTINE)
    slug = models.SlugField(unique=True, null=False, editable=False)
    maintenance_schedule = models.IntegerField(choices=MAINTENANCE_SCHEDULE, default=HOURS)
    maintenance_frequency = models.IntegerField(default=0)
    time_allocated = models.FloatField(default=0)
    maintenance_action = models.CharField(max_length=255)
    item_used = models.CharField(max_length=20)
    quantity = models.FloatField(default=0)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def get_absolute_url(self):
        return reverse('maintenance_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.maintenance_name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenances"
        ordering = ("maintenance_name",)
    
    def __str__(self):
        return self.maintenance_name


class MaintenanceSchedule(models.Model):
    schedule_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=False, editable=False)
    maintenance_name = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def get_absolute_url(self):
        return reverse('maintanance_schedule_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.schedule_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("schedule_name",)
        verbose_name_plural = "Maintenance Schedules"
    
    def __str__(self):
        return self.schedule_name


class Component(models.Model):
    component_system_no = models.IntegerField(_('System no'),)
    component_name = models.CharField(_('Component Name'), max_length=100)
    slug = models.SlugField(unique=True, null=False, editable=False)
    component_manufacturer = models.CharField(_('Manufacturer'), max_length=100, blank=True)
    component_stock_code = models.CharField(_('Stock Code'), max_length=100, blank=True)
    maintenance_schedule= models.ForeignKey(MaintenanceSchedule, on_delete=models.CASCADE)
    component_image = models.ImageField(_('Image'), default="default.jpeg", upload_to = 'images/% Y/% m/% d/')
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, default=timezone.now)
    date_modified = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return self.component_name

    def get_absolute_url(self):
        return reverse('component_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.component_name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"
        ordering = ("component_name",)


class Company(models.Model):

    company_name = models.CharField(_('Company Name'), 
    help_text=_('Name of the Company, Department, etc'), max_length=100)
    slug = models.SlugField(unique=True, null=False, editable=False)
    company_address = models.CharField(blank=True, max_length=255)
    company_contacts = models.CharField(blank=True, max_length=255)
    company_manager = models.CharField(max_length=100, blank=True)
    company_email = models.EmailField(max_length = 254, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.company_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("company_name",)
        verbose_name_plural = "Companies"


class Division(models.Model):

    division_name = models.CharField(_('Division Name'), 
    help_text=_('Name of the Division, Department, etc'), max_length=100)
    slug = models.SlugField(unique=True, null=False, editable=False)
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    division_address = models.CharField(blank=True, max_length=255)
    division_contacts = models.CharField(blank=True, max_length=255)
    division_manager = models.CharField(max_length=100, blank=True)
    division_email = models.EmailField(max_length = 254, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.division_name

    def get_absolute_url(self):
        return reverse('division_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.division_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("division_name",)


class Branch(models.Model):

    branch_name = models.CharField(_('Branch Name'), 
    help_text=_('Name of the Branch, Department, etc'), max_length=100)
    slug = models.SlugField(unique=True, null=False, editable=False)
    division_name = models.ForeignKey(Division, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.branch_name

    def get_absolute_url(self):
        return reverse('branch_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.branch_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("branch_name",)
        verbose_name_plural = "Branches"


class Position(models.Model):

    position_name = models.CharField(_('Position Name'), 
    help_text=_('Name of the Position, Department, etc'), max_length=100)
    slug = models.SlugField(unique=True, null=False, editable=False)
    branch_name = models.ForeignKey(Branch, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.position_name

    def get_absolute_url(self):
        return reverse('position_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.position_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("position_name",)


class Group(models.Model):
    group_name = models.CharField(_('Group'), max_length=50)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.group_name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.group_name)
        return super().save(*args, **kwargs)


class System(models.Model):
    system_name = models.CharField(_('System'), max_length=50)
    group_name = models.ForeignKey(Group, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.system_name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.system_name)
        return super().save(*args, **kwargs)


class Type(models.Model):
    type_name = models.CharField(_('Type'), max_length=50)
    system_name = models.ForeignKey(System, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.type_name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.type_name)
        return super().save(*args, **kwargs)


class SubType(models.Model):
    subtype_name = models.CharField(_('Subtype'), max_length=50)
    type_name = models.ForeignKey(Type, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.subtype_name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.subtype_name)
        return super().save(*args, **kwargs)


    class Meta(object):
        verbose_name_plural = "Subtypes"


class Vendor(models.Model):

    vendor_name = models.CharField(_('Vendor Name'), 
    help_text=_('Name of the Vendor, Department, etc'), max_length=100)
    slug = models.SlugField(unique=True, null=False, editable=False)
    vendor_address = models.CharField(blank=True, max_length=255)
    vendor_contacts = models.CharField(blank=True, max_length=255)
    vendor_manager = models.CharField(max_length=100, blank=True)
    vendor_email = models.EmailField(max_length = 254, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.vendor_name

    def get_absolute_url(self):
        return reverse('vendor_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.vendor_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("vendor_name",)
        verbose_name_plural = "Vendors"


class ComponentAllocation(models.Model):
   
    GOOD = 1
    BROKEN = 0

    STATUS = ((GOOD, 'Good'), (BROKEN, 'Broken'),)

    component_name = models.ForeignKey(Component,on_delete=models.PROTECT, verbose_name= _('component Name'))
    vendor_name = models.ForeignKey(Vendor, on_delete=models.PROTECT, verbose_name= _('Vendor Name'))
    company_name = models.ForeignKey(Company, on_delete=models.PROTECT)
    division_name = models.ForeignKey(Division, on_delete=models.PROTECT)
    branch_name = models.ForeignKey(Branch, on_delete=models.PROTECT)
    position_name = models.ForeignKey(Position, on_delete=models.PROTECT)
    component_serial_number = models.CharField(_('Component Serial No.'), max_length=50)
    component_status = models.IntegerField(_('Component Status'), choices=STATUS, 
    default=GOOD)
    component_image = models.ImageField(_('Image'), default="default.jpeg", upload_to = 'images/% Y/% m/% d/')
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
    group_name = models.ForeignKey(Group, on_delete=models.CASCADE)
    system_name = models.ForeignKey(System, on_delete=models.CASCADE)
    type_name = models.ForeignKey(Type, on_delete=models.CASCADE)
    subtype_name = models.ForeignKey(SubType, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return str('{} - {}'.format(self.component_name))

    def get_absolute_url(self):
        return reverse('allocation_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify('{}{}{}'.format(self.component_name, self.company_name, self.timezone.now))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Components Allocation"
        ordering = ("-date_allocated",)


    

