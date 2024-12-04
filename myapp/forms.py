from django import forms
from myapp.models import TblUser, TblCustomer, TblVendor, TblSalesOrder, TblPurchaseOrder, TblLedger

class UserForm(forms.ModelForm):
    class Meta:
        model = TblUser
        fields = ['username', 'password', 'name', 'email', 'role']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = TblCustomer
        fields = ['retail_name', 'address', 'email', 'phone_number']  # Specify the fields you want to update

class VendorForm(forms.ModelForm):  # New form for TblVendor
    class Meta:
        model = TblVendor
        fields = ['company_name', 'address', 'email', 'phone_number', 'contract_period']  # Specify the fields for vendor

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = TblSalesOrder
        fields = ['order_date', 'customer_name', 'address', 'product', 'quantity', 'price', 'total_price', 'information', 'buy_price', 'profit', 'nomor_so']  # Specify the fields for the sales order

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = TblPurchaseOrder
        fields = ['order_date', 'vendor_name', 'product', 'quantity', 'price', 'total_price', 'nomor_po']  # Specify the fields for the sales order

class LedgerForm(forms.ModelForm):
    class Meta:
        model = TblLedger
        fields = ['order_date', 'customer_name', 'income', 'outcome', 'sisa', 'nomor_so', 'totaltransaksi']  # Specify the fields for the sales order