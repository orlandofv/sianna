from decimal import Decimal

from turtle import position
from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify # new
from django.utils.translation import ugettext_lazy as _

from asset_app.models import Costumer
from isis.models import PaymentMethod, PaymentTerm, Product, Warehouse


class SupplierInvoice(models.Model):
    DELIVERED = 1
    NOT_DELIVERED = 0

    DELIVERED_STATUS = ((DELIVERED, _('Delivered')), (NOT_DELIVERED, _('Not delivered')))

    invoice = models.CharField('Invoice Number', help_text='Supplier Invoice Number(Ex: Invoice: 12345)', 
    max_length=100)
    name =  models.CharField(max_length=50, unique=True)
    number = models.IntegerField(unique=True)
    slug = models.SlugField(unique=True, null=False, editable=False)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, default=1)
    payment_term = models.ForeignKey(PaymentTerm, on_delete=models.PROTECT, default=1)
    supplier = models.ForeignKey(verbose_name=_('Supplier'), to=Costumer, on_delete=models.PROTECT, default=1)
    date = models.DateTimeField(_('Invoice Date'), default=timezone.now)
    due_date = models.DateTimeField(_('Due Date'), default=timezone.now)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, default=1)
    paid_status = models.IntegerField(default=0)
    delivered_status = models.IntegerField(default=0)
    finished_status = models.IntegerField(default=0)
    active_status = models.IntegerField(default=1)
    notes = models.TextField(_('Invoice Notes'), blank=True)
    public_notes = models.TextField(_('Public Notes'), blank=True)
    date_created = models.DateTimeField(editable=False, default=timezone.now)
    date_modified = models.DateTimeField(editable=False, default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('costumer_invoice_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        invoice = '{} {}'.format(_('Invoice'), self.number)
        self.name = invoice

        if not self.slug:
            self.slug = slugify(invoice)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('-name',)
        unique_together = ('invoice', 'supplier')


class SupplierInvoiceItem(models.Model):
    invoice = models.ForeignKey(SupplierInvoice, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    tax = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    quantity = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    tax_total = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    discount_total = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    sub_total = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=18, decimal_places=6, default=0)
        
    def __str__(self):
        return self.invoice
    
    def save(self, *args, **kwargs): # new
        print("Nao sei que corre antes {}".format(self.invoice.number))
        # Discount is saved on db as whole number so we must divide by 100
        total = round(self.quantity * self.price, 6)
        print('Total: ', total)

        discount = round(self.discount * Decimal(0.01) * total, 6)
        print('Discount ', discount)

        sub_total = round(total - discount, 6)
        print('Subtotal ', sub_total)

        tax = round(sub_total * self.tax * Decimal(0.01), 6)
        print('Tax ', tax)

        grand_total = sub_total + tax
        print('Grand Total ', grand_total)

        self.tax_total = tax
        self.discount_total = discount
        self.sub_total = sub_total
        self.total = grand_total

        return super().save(*args, **kwargs)

