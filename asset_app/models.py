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

    name = models.CharField(max_length=50, unique=True)
    type = models.IntegerField(choices=MAINTENANCE_CHOICES, default=ROUTINE)
    slug = models.SlugField(unique=True, null=False, editable=False)
    schedule = models.IntegerField(choices=MAINTENANCE_SCHEDULE, default=HOURS)
    frequency = models.IntegerField(default=0)
    time_allocated = models.FloatField(default=0)
    action = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def get_absolute_url(self):
        return reverse('maintenance_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenances"
        ordering = ("name",)
    
    def __str__(self):
        return self.name


class MaintenanceSchedule(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def get_absolute_url(self):
        return reverse('maintanance_schedule_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Maintenance Schedules"
    
    def __str__(self):
        return self.name


class Component(models.Model):
    component_no = models.IntegerField(_('System no'), unique=True)
    name = models.CharField(_('Component Name'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    manufacturer = models.CharField(_('Manufacturer'), max_length=100, blank=True)
    stock_code = models.CharField(_('Stock Code'), max_length=100, blank=True)
    maintenanceschedule= models.ForeignKey(MaintenanceSchedule, on_delete=models.CASCADE)
    image = models.ImageField(_('Image'), default="default.jpeg", upload_to = 'media')
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, default=timezone.now)
    date_modified = models.DateTimeField(editable=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return "{} - {}".format(self.component_no, self.name)

    def get_absolute_url(self):
        return reverse('component_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify("{} - {}".format(self.component_no, self.name))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"
        ordering = ("name",)


class Company(models.Model):

    name = models.CharField(_('Company Name'), 
    help_text=_('Name of the Company, Department, etc'), max_length=100, unique=True)
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'slug': self.slug})

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
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField(blank=True, max_length=255)
    contacts = models.CharField(blank=True, max_length=255)
    manager = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length = 254, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('division_detail', kwargs={'slug': self.slug})

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
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('branch_detail', kwargs={'slug': self.slug})

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
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('position_detail', kwargs={'slug': self.slug})

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class System(models.Model):
    name = models.CharField(_('System'), max_length=50, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def get_absolute_url(self):
        return reverse('system_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Type(models.Model):
    name = models.CharField(_('Type'), max_length=50, unique=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def get_absolute_url(self):
        return reverse('type_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class SubType(models.Model):
    name = models.CharField(_('Subtype'), max_length=50, unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=False, editable=False)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def get_absolute_url(self):
        return reverse('subtype_detail', kwargs={'slug': self.slug})

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vendor_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Vendors"


class Allocation(models.Model):
   
    GOOD = 1
    BROKEN = 0

    STATUS = ((GOOD, 'Good'), (BROKEN, 'Broken'),)

    allocation_no = models.IntegerField(_("Allocation No.")) # validators=[RegexValidator(r'^[0-9]{9}$')]
    component = models.ForeignKey(Component,on_delete=models.PROTECT, verbose_name= _('component Name'))
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, verbose_name= _('Vendor Name'))
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    serial_number = models.CharField(_('Component Serial No.'), max_length=50, unique=True)
    status = models.IntegerField(_('Component Status'), choices=STATUS, 
    default=GOOD)
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
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    subtype = models.ForeignKey(SubType, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")


    def __str__(self):
        return str('{} - {}'.format(self.allocation_no, self.name))

    def get_absolute_url(self):
        return reverse('allocation_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify('{}-{}'.format(self.allocation_no, self.name))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Allocations"
        ordering = ("-date_allocated",)


class Item(models.Model):
    
    name = models.CharField(_('Name'), max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    quantity = models.DecimalField(_('Quantity'), decimal_places=2, max_digits=9)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'slug': self.slug})

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


