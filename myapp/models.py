from django.db import models

class TblUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'tbl_user'  # Map to the existing tbl_user table
        managed = False  # Prevent Django from creating the table

    def __str__(self):
        return self.username

class TblCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    retail_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'tbl_customer'  # Map to the existing tbl_customer table
        managed = False  # Prevent Django from creating the table

    def __str__(self):
        return self.retail_name

class TblVendor(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    contract_period = models.CharField(max_length=50, null=True, blank=True)  # New field for contract period

    class Meta:
        db_table = 'tbl_vendor'  # Map to the existing tbl_vendor table
        managed = False  # Prevent Django from creating the table

    def __str__(self):
        return self.company_name


class TblSalesOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_date = models.DateField(null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    product = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.CharField(max_length=255, null=True, blank=True)
    information = models.CharField(max_length=255, null=True, blank=True)
    nomor_so = models.CharField(max_length=255, null=True, blank=True)
    buy_price = models.CharField(max_length=255, null=True, blank=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'tbl_sales_order'  # Map to the existing tbl_sales_order table
        managed = False  # Prevent Django from creating the table

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class TblPurchaseOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_date = models.DateField(max_length=255, null=True, blank=True)
    vendor_name = models.CharField(max_length=255, null=True, blank=True)
    product = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.CharField(max_length=255, null=True, blank=True)
    nomor_po = models.CharField(max_length=255,unique=True, null=True, blank=True)

    class Meta:
        db_table = 'tbl_purchase_order'  # Map to the existing tbl_sales_order table
        managed = False  # Prevent Django from creating the table

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class TblLedger(models.Model):
    id = models.AutoField(primary_key=True)
    order_date = models.CharField(max_length=255, null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    outcome = models.IntegerField(null=True, blank=True)
    income = models.CharField(max_length=255, null=True, blank=True)
    sisa = models.CharField(max_length=255, null=True, blank=True)
    nomor_so = models.CharField(max_length=255, null=True, blank=True)
    totaltransaksi = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'tbl_ledger'  # Map to the existing tbl_sales_order table
        managed = False  # Prevent Django from creating the table

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
