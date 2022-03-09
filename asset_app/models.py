from django.db import models
from django.utils import timezone
from asset_manager.settings import DATABASES
from users.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify # new


database = DATABASES
db = database['default']['NAME']
usr = database['default']['USER']
psw = database['default']['PASSWORD']
prt = database['default']['PORT']


def get_locations():
    import mysql.connector as mc

    conn = mc.connect(host='127.0.0.1',
                            user=usr,
                            passwd=psw,
                            db=db,
                            port=prt)

    cur = conn.cursor()
    sql = 'SELECT id, location_name from asset_app_location'
    default = (0, ('---'))

    try:
        cur.execute(sql)
        data = cur.fetchall()
        data.insert(0, default)
    except Exception as e:
        data = (default, )
        
        print(e)
    
    print(data)
    return data

get_locations()

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=False)
    category_image = models.ImageField(default="default.jpeg", upload_to = 'images/')
    notes = models.TextField(blank=True)
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

class System(models.Model):
    system_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=False)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
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


class Assets(models.Model):
    asset_name = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    system_id = models.ForeignKey(System, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, null=False)
    asset_serial_no = models.CharField(max_length=100)
    asset_manufacturer = models.CharField(max_length=100)
    date_purchased = models.DateTimeField(default=timezone.now)
    asset_issued = models.BooleanField(default=False)
    asset_image = models.ImageField(default="default.jpeg", upload_to = 'images/')
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

    
class Location(models.Model):
    location_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=False)
    parent_location = models.IntegerField(choices=get_locations(), default=0)
    location_address = models.CharField(blank=True)
    location_contacts = models.CharField(blank=True)
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


class AssetsIssuance(models.Model):
    asset_id=models.ForeignKey(Assets,on_delete=models.PROTECT)
    asset_status = models.BooleanField(default=True)
    asset_location = models.ForeignKey(Location, on_delete=models.PROTECT)
    date_issued = models.DateTimeField(default=timezone.now)
    asset_assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(editable=False, 
    default=timezone.now)
    date_modified = models.DateTimeField(editable=False, 
    default=timezone.now)

    def __str__(self):
        return self.asset_id

    def get_absolute_url(self):
        return reverse('issuance_detail', kwargs={'pk': self.pk})

