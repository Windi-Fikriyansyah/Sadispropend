# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from myapp.models import TblUser, TblCustomer, TblVendor, TblSalesOrder, TblPurchaseOrder, TblLedger
from .forms import UserForm, CustomerForm, VendorForm, SalesOrderForm, PurchaseOrderForm, LedgerForm
from django.contrib.auth import logout
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.db.models.functions import TruncYear
from django.utils import timezone
from pytz import timezone as pytz_timezone
from .models import TblPurchaseOrder, TblSalesOrder

# Logout function
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Manually authenticate the user from the TblUser model
            user = TblUser.objects.get(username=username, password=password)  # No hash comparison
            # Set session data manually
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['user_role'] = user.role
            return redirect('success_page')  # Redirect to the success page
        except TblUser.DoesNotExist:
            messages.error(request, 'Gagal Login')

    return render(request, 'login.html')

# Read - Display all users
def user_list(request):
    # Pastikan pengguna sudah login
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Jika belum login, redirect ke halaman login

    try:
        # Ambil data pengguna berdasarkan session
        user = TblUser.objects.get(id=user_id)
        if user.role != 'admin':  # Hanya admin yang diizinkan
            return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")
    except TblUser.DoesNotExist:
        return redirect('login')  # Redirect jika pengguna tidak valid

    # Tampilkan daftar pengguna jika peran sesuai
    users = TblUser.objects.all()
    return render(request, 'user_list.html', {'users': users})

# Create - Add a new user
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User berhasil ditambahkan')
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

# Update - Edit an existing user
def user_update(request, id):
    user = get_object_or_404(TblUser, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User berhasil diubah')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

def user_detail(request, id):
    user = get_object_or_404(TblUser, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_detail.html', {'form': form})

# Delete - Remove a user
def user_delete(request, id):
    user = get_object_or_404(TblUser, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User berhasil dihapus')
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

def accounting(request):
    return render(request, 'accounting.html')

def report_view(request):
    return render(request, 'report.html')

def vendor_view(request):
    return render(request, 'vendor.html')

def customer_view(request):
    return render(request, 'customer.html')

def vendor_view(request):
    return render(request, 'vendor.html')

def ledger_view(request):
    return render(request, 'ledger.html')

def customer_list(request):
    customers = TblCustomer.objects.all()  # Assuming you have a TblCustomer model
    return render(request, 'customer.html', {'customers': customers})

def customer_create(request):
    if request.method == 'POST':
        retail_name = request.POST['retail_name']
        address = request.POST['address']
        email = request.POST['email']
        phone_number = request.POST['phone_number']

        # Create a new customer instance and save it to the database
        customer = TblCustomer(
            retail_name=retail_name,
            address=address,
            email=email,
            phone_number=phone_number
        )
        customer.save()
        messages.success(request, 'Customer berhasil ditambahkan')
        return redirect('customer_list')  # Corrected redirect to the customer list page

    return render(request, 'customer_form.html')  # Show the form

def customer_detail(request, id):
    customer = get_object_or_404(TblCustomer, id=id)
    return render(request, 'customer_detail.html', {'customer': customer})

def customer_update(request, id):
    customer = get_object_or_404(TblCustomer, id=id)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer berhasil diubah')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customer_update.html', {'form': form, 'customer': customer})


def customer_delete(request, id):
    customer = get_object_or_404(TblCustomer, id=id)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer berhasil dihapus')
        return redirect('customer_list')  # Redirect to the customer list or appropriate page
    return render(request, 'customer_confirm_delete.html', {'customer': customer})

def vendor_list(request):
    vendors = TblVendor.objects.all()  # Assuming you have a TblVendor model
    return render(request, 'vendor.html', {'vendors': vendors})

def vendor_create(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        address = request.POST['address']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        contract_period = request.POST['contract_period']

        # Create a new vendor instance and save it to the database
        vendor = TblVendor(
            company_name=company_name,
            address=address,
            email=email,
            phone_number=phone_number,
            contract_period=contract_period  # Include contract_period
        )
        vendor.save()
        messages.success(request, 'Vendor berhasil ditambahkan')
        return redirect('vendor_list')  # Corrected redirect to the vendor list page

    return render(request, 'vendor_form.html')  # Show the form

def vendor_detail(request, id):
    vendor = get_object_or_404(TblVendor, id=id)
    return render(request, 'vendor_detail.html', {'vendor': vendor})

def vendor_update(request, id):
    vendor = get_object_or_404(TblVendor, id=id)
    if request.method == "POST":
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor berhasil diubah')
            return redirect('vendor_list')
    else:
        form = VendorForm(instance=vendor)

    return render(request, 'vendor_update.html', {'form': form, 'vendor': vendor})

def vendor_delete(request, id):
    vendor = get_object_or_404(TblVendor, id=id)
    if request.method == 'POST':
        vendor.delete()
        messages.success(request, 'Vendor berhasil dihapus')
        return redirect('vendor_list')  # Redirect to the vendor list or appropriate page
    return render(request, 'vendor_confirm_delete.html', {'vendor': vendor})

# Read - Display all sales orders
def sales_order_list(request):
    selected_year = request.GET.get('year', None)

    # Filter sales orders based on the selected year
    if selected_year:
        sales_orders = TblSalesOrder.objects.filter(order_date__year=selected_year)
    else:
        sales_orders = TblSalesOrder.objects.all()

    return render(request, 'sales_order_list.html', {'sales_orders': sales_orders})

# Create - Add a new sales order
def sales_order_create(request):
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        if form.is_valid():
            # Automatically generate the Sales Order Number (SO Number)
            last_order = TblSalesOrder.objects.order_by('id').last()
            if last_order:
                # Assuming SO numbers are incremented, otherwise customize the logic
                new_so_number = f"SO-{last_order.id + 1}"
            else:
                new_so_number = "SO-1"  # First Sales Order number

            # Add the generated SO number to the form data
            form.instance.nomor_so = new_so_number
            jakarta_tz = pytz_timezone('Asia/Jakarta')
            if not form.instance.order_date:
                form.instance.order_date = timezone.now().astimezone(jakarta_tz).date()

            form.save()
            messages.success(request, 'Sales Order berhasil ditambahkan')
            return redirect('sales_order_list')
    else:
        form = SalesOrderForm()
        # Automatically generate the SO number on page load
        last_order = TblSalesOrder.objects.order_by('id').last()
        if last_order:
            new_so_number = f"SO-{last_order.id + 1}"
        else:
            new_so_number = "SO-1"  # First Sales Order number
        form.fields['nomor_so'].initial = new_so_number  # Set initial value for the field
        jakarta_tz = pytz_timezone('Asia/Jakarta')
        form.fields['order_date'].initial = timezone.now().astimezone(jakarta_tz).date()
        context = {
            'form': form,
            'title': 'Add Sales Order',
            'today': timezone.now().astimezone(jakarta_tz).date(),
        }
    return render(request, 'sales_order_form.html', context)

# Update - Edit an existing sales order
def sales_order_update(request, id):
    sales_order = get_object_or_404(TblSalesOrder, id=id)
    if request.method == 'POST':
        form = SalesOrderForm(request.POST, instance=sales_order)
        if form.is_valid():

            jakarta_tz = pytz_timezone('Asia/Jakarta')
            if not form.instance.order_date:
                form.instance.order_date = timezone.now().astimezone(jakarta_tz).date()

            form.save()
            messages.success(request, 'Sales Order berhasil diubah')
            return redirect('sales_order_list')
    else:
        form = SalesOrderForm(instance=sales_order)

    jakarta_tz = pytz_timezone('Asia/Jakarta')
    return render(request, 'sales_order_form.html',{
        'form': form,
        'title': 'Update Sales Order',
        'today': timezone.now().astimezone(jakarta_tz).date(),   # Add the 'today' variable
    })

def sales_order_detail(request, id):
    sales_order = get_object_or_404(TblSalesOrder, id=id)
    if request.method == 'POST':
        form = SalesOrderForm(request.POST, instance=sales_order)
        if form.is_valid():
            form.save()
            return redirect('sales_order_list')
    else:
        form = SalesOrderForm(instance=sales_order)
    return render(request, 'sales_order_detail.html', {'form': form})

# Delete - Remove a sales order
def sales_order_delete(request, id):
    sales_order = get_object_or_404(TblSalesOrder, id=id)
    if request.method == 'POST':
        sales_order.delete()
        messages.success(request, 'Sales Order berhasil dihapus')
        return redirect('sales_order_list')
    return render(request, 'sales_order_confirm_delete.html', {'sales_order': sales_order})

# Read - Display all sales orders
def purchase_order_list(request):
    selected_year1 = request.GET.get('year', None)
    search_term = request.GET.get('search', '').strip()

    # Filter purchase orders based on the selected year
    if selected_year1:
        purchase_orders = TblPurchaseOrder.objects.filter(order_date__year=selected_year1)
    else:
        purchase_orders = TblPurchaseOrder.objects.all()

    # Further filter by search term
    if search_term:
        purchase_orders = purchase_orders.filter(
            Q(vendor_name__icontains=search_term) |
            Q(product__icontains=search_term) |
            Q(nomor_po__icontains=search_term)
        )

    return render(request, 'purchase_order_list.html', {'purchase_orders': purchase_orders})
# Create - Add a new sales order
def purchase_order_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            # Automatically generate the PO number
            last_order = TblPurchaseOrder.objects.order_by('id').last()
            if last_order:
                # Assuming PO numbers are incremented, otherwise customize the logic
                new_po_number = f"PO-{last_order.id + 1}"
            else:
                new_po_number = "PO-1"  # First PO number

            # Add the generated PO number to the form data
            form.instance.nomor_po = new_po_number
            jakarta_tz = pytz_timezone('Asia/Jakarta')
            if not form.instance.order_date:
                form.instance.order_date = timezone.now().astimezone(jakarta_tz).date()

            form.save()
            messages.success(request, 'Purchase Order berhasil ditambahkan')
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm()
        # Automatically generate the PO number on page load
        last_order = TblPurchaseOrder.objects.order_by('id').last()
        if last_order:
            new_po_number = f"PO-{last_order.id + 1}"
        else:
            new_po_number = "PO-1"  # First PO number
        form.fields['nomor_po'].initial = new_po_number  # Set initial value for the field
        jakarta_tz = pytz_timezone('Asia/Jakarta')
        form.fields['order_date'].initial = timezone.now().astimezone(jakarta_tz).date()

        context = {
            'form': form,
            'title': 'Add Purchase Order',
            'today': timezone.now().astimezone(jakarta_tz).date(),
        }
        return render(request, 'purchase_order_form.html', context)

# Update - Edit an existing sales order
def purchase_order_update(request, id):
    purchase_order = get_object_or_404(TblPurchaseOrder, id=id)

    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=purchase_order)
        if form.is_valid():
            # Ensure 'order_date' is set to today's date if it is missing
            jakarta_tz = pytz_timezone('Asia/Jakarta')
            if not form.instance.order_date:
                form.instance.order_date = timezone.now().astimezone(jakarta_tz).date()


            form.save()
            messages.success(request, 'Purchase Order berhasil diubah')
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm(instance=purchase_order)

    # Pass 'today' to the template
    jakarta_tz = pytz_timezone('Asia/Jakarta')
    return render(request, 'purchase_order_form.html', {
        'form': form,
        'title': 'Update Purchase Order',
        'today': timezone.now().astimezone(jakarta_tz).date(),  # Add the 'today' variable
    })


def purchase_order_detail(request, id):
    purchase_order = get_object_or_404(TblPurchaseOrder, id=id)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=purchase_order)
        if form.is_valid():
            form.save()
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm(instance=purchase_order)
    return render(request, 'purchase_order_detail.html', {'form': form})

# Delete - Remove a sales order
def purchase_order_delete(request, id):
    purchase_order = get_object_or_404(TblPurchaseOrder, id=id)
    if request.method == 'POST':
        purchase_order.delete()
        messages.success(request, 'Purchasae Order berhasil dihapus')
        return redirect('purchase_order_list')
    return render(request, 'purchase_order_confirm_delete.html', {'purchase_order': purchase_order})

# Read - Display all sales orders
def ledger_list(request):
    selected_year = request.GET.get('year')

    # Filter sales orders berdasarkan tahun yang dipilih (jika ada)
    try:
        if selected_year and selected_year.isdigit():
            ledger = TblLedger.objects.filter(order_date__year=int(selected_year))
        else:
            ledger = TblLedger.objects.all()
    except ValueError:
        # Jika input tidak valid, kembalikan semua data
        ledger = TblLedger.objects.all()

    # Render template dengan data ledger
    return render(request, 'ledger_list.html', {'ledger': ledger})

# Create - Add a new sales order
def ledger_create(request):
    if request.method == "POST":
        # Extract the form data from POST request
        order_date = request.POST.get('order_date')
        nomor_so = request.POST.get('nomor_so')
        customer_name = request.POST.get('customer_name')

        try:
            income = int(request.POST.get('income', 0))  # Default to 0 if empty
        except ValueError:
            income = 0  # If the conversion fails, set it to 0

        try:
            outcome = int(request.POST.get('outcome', 0))  # Default to 0 if empty
        except ValueError:
            outcome = 0

        try:
            hutang_piutang = int(request.POST.get('hutang_piutang', 0))  # Default to 0 if empty
        except ValueError:
            hutang_piutang = 0

        try:
            totaltransaksi = int(request.POST.get('totaltransaksi', 0))  # Default to 0 if empty
        except ValueError:
            totaltransaksi = 0

        # Save the data to the Ledger model
        if not order_date:
            # Get the current time in Indonesia timezone (Asia/Jakarta)
            jakarta_tz = pytz_timezone('Asia/Jakarta')
            order_date = timezone.now().astimezone(jakarta_tz).date()

        new_ledger = TblLedger(
            order_date=order_date,
            nomor_so=nomor_so,
            customer_name=customer_name,
            income=income,
            outcome=outcome,
            hutang_piutang=hutang_piutang,
            totaltransaksi=totaltransaksi,
        )

        new_ledger.save()  # Save the object to the database

        # Redirect to a different page (for example, a list page)
        return redirect('ledger_list')

    po_list = TblPurchaseOrder.objects.all()
    so_list = TblSalesOrder.objects.all()
    return render(request, "ledger_form.html", {
        "po_list": po_list,
        "so_list": so_list,
        "today": timezone.now().astimezone(pytz_timezone('Asia/Jakarta')).date(),
        "title" : "ADD LEDGER"
    })

def fetch_details(request):
    nomor = request.GET.get("nomor")  # Get the selected PO/SO number
    response = {}

    if nomor:
        try:
            po = TblPurchaseOrder.objects.get(nomor_po=nomor)
            response = {
                "nama": po.vendor_name,
                "type": "PO",  # Indicate this is a PO
            }
        except TblPurchaseOrder.DoesNotExist:
            try:
                so = TblSalesOrder.objects.get(nomor_so=nomor)
                response = {
                    "nama": so.customer_name,
                    "type": "SO",  # Indicate this is an SO
                }
            except TblSalesOrder.DoesNotExist:
                response = {"error": "PO/SO not found."}

    return JsonResponse(response)



def ledger_update(request, id):
    ledger = get_object_or_404(TblLedger, id=id)

    po_list = TblPurchaseOrder.objects.all()
    so_list = TblSalesOrder.objects.all()

    if request.method == "POST":
        form = LedgerForm(request.POST, instance=ledger, po_list=po_list, so_list=so_list)
        if form.is_valid():
            jakarta_tz = pytz_timezone('Asia/Jakarta')
            if not form.instance.order_date:
                form.instance.order_date = timezone.now().astimezone(jakarta_tz).date()
            form.save()
            return redirect('ledger_list')
    else:
        form = LedgerForm(instance=ledger, po_list=po_list, so_list=so_list)

    # Get the initial value for 'nomor_po_so' (if exists)
    initial_nomor = ledger.nomor_so if ledger.nomor_so else ''

    jakarta_tz = pytz_timezone('Asia/Jakarta')
    return render(request, 'ledger_form.html', {
        'form': form,
        'ledger': ledger,
        'po_list': po_list,
        'so_list': so_list,
        'initial_nomor': initial_nomor,
        'today': timezone.now().astimezone(jakarta_tz).date(),
        "title" : "UPDATE LEDGER" # Add initial value here
    })

def ledger_detail(request, id):
    purchase_order = get_object_or_404(TblLedger, id=id)
    if request.method == 'POST':
        form = LedgerForm(request.POST, instance=purchase_order)
        if form.is_valid():
            form.save()
            return redirect('ledger_list')
    else:
        form = LedgerForm(instance=purchase_order)
    return render(request, 'ledger_detail.html', {'form': form})

# Delete - Remove a sales order
def ledger_delete(request, id):
    purchase_order = get_object_or_404(TblLedger, id=id)
    if request.method == 'POST':
        purchase_order.delete()
        messages.success(request, 'Ledger berhasil dihapus')
        return redirect('ledger_list')
    return render(request, 'ledger_confirm_delete.html', {'purchase_order': purchase_order})


def get_profit_chart(request):
    data = TblSalesOrder.objects.all()
    customer_names=[entry.customer_name for entry in data]
    profits=[entry.profit for entry in data]  # Properly indented

    # Return the data as a JSON response
    return JsonResponse({
        'customer_names': customer_names,
        'profits': profits
    })

def get_incomeoutcome_chart(request):
    year = request.GET.get('year', None)

    # If a year is provided, filter by year, otherwise, get data for all years
    if year:
        try:
            year = int(year)
            queryset_outcome = TblPurchaseOrder.objects.filter(order_date__year=year).aggregate(outcome=Sum('total_price'))['outcome'] or 0
            queryset_income = TblSalesOrder.objects.filter(order_date__year=year).aggregate(income=Sum('total_price'))['income'] or 0
        except ValueError:
            return JsonResponse({'error': 'Invalid year'}, status=400)
    else:
        # If no year is selected, fetch total data without filtering by year
        queryset_outcome = TblPurchaseOrder.objects.aggregate(outcome=Sum('total_price'))['outcome'] or 0
        queryset_income = TblSalesOrder.objects.aggregate(income=Sum('total_price'))['income'] or 0

    data = {
        'outcome': queryset_outcome,
        'income': queryset_income
    }
    return JsonResponse(data)

def get_profit_per_year_chart(request):
    # Aggregate total profit per year
    queryset = TblSalesOrder.objects.annotate(year=TruncYear('order_date')) \
        .values('year') \
        .annotate(total_profit=Sum('profit')) \
        .order_by('year')

    # Prepare data for the chart
    data = {
        'labels': [str(entry['year'].year) for entry in queryset],  # Extract years
        'profits': [entry['total_profit'] for entry in queryset],    # Extract total profits
    }

    return JsonResponse(data)
