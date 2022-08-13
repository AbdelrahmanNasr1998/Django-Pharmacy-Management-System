import json
from django.core.exceptions import PermissionDenied, BadRequest

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from accounts.models import Accounts, Payments
from django.template.loader import render_to_string
from django.http import Http404
from .models import Category, Medicine, Items, Payment, Settings
from .forms import AddMedicineForm, UpdateMedicineForm, AddCategoryForm, UpdateCategoryForm, NewPaymentForm, ItemsForm, \
    AddPaymentForm, UpdatePaymentForm, SettingsForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

import datetime

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month
current_day = datetime.datetime.now().day


# Create your views here.


def account(request, username):
    profile_user = Accounts.objects.get(username=username)

    if request.user == profile_user:

        if profile_user.type == 'pharmacy':

            payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

            notifi = 0

            year = 2000
            month = 1
            day = 1

            for payment in payment_user_one:
                day = payment.end_billing.day
                month = payment.end_billing.month
                year = payment.end_billing.year

            a = datetime.datetime.now()
            b = datetime.datetime(year, month, day)
            end = b - a
            if end.days <= 30:
                end_days = end.days
                notifi += 1
            else:
                end_days = ''

            payment_user = Payments.objects.filter(username=profile_user.id)

            payment_all = Payment.objects.filter(username=request.user).count()
            payment_year = Payment.objects.filter(username=request.user, date__year=current_year).count()
            payment_month = Payment.objects.filter(username=request.user, date__month=current_month,
                                                   date__year=current_year).count()
            payment_day = Payment.objects.filter(username=request.user, date__day=current_day,
                                                 date__month=current_month, date__year=current_year).count()

            payment = Payment.objects.filter(username=request.user)

            day_pay = 0.00
            month_pay = 0.00
            year_pay = 0.00
            total_pay = 0.00

            mon_1 = 0
            mon_2 = 0
            mon_3 = 0
            mon_4 = 0
            mon_5 = 0
            mon_6 = 0
            mon_7 = 0
            mon_8 = 0
            mon_9 = 0
            mon_10 = 0
            mon_11 = 0
            mon_12 = 0

            for pay in payment:
                if pay.date.month == 1 and pay.date.year == current_year:
                    tot = pay.total
                    mon_1 += float(tot)

                if pay.date.month == 2 and pay.date.year == current_year:
                    tot = pay.total
                    mon_2 += float(tot)

                if pay.date.month == 3 and pay.date.year == current_year:
                    tot = pay.total
                    mon_3 += float(tot)

                if pay.date.month == 4 and pay.date.year == current_year:
                    tot = pay.total
                    mon_4 += float(tot)

                if pay.date.month == 5 and pay.date.year == current_year:
                    tot = pay.total
                    mon_5 += float(tot)

                if pay.date.month == 6 and pay.date.year == current_year:
                    tot = pay.total
                    mon_6 += float(tot)

                if pay.date.month == 7 and pay.date.year == current_year:
                    tot = pay.total
                    mon_7 += float(tot)

                if pay.date.month == 8 and pay.date.year == current_year:
                    tot = pay.total
                    mon_8 += float(tot)

                if pay.date.month == 9 and pay.date.year == current_year:
                    tot = pay.total
                    mon_9 += float(tot)

                if pay.date.month == 10 and pay.date.year == current_year:
                    tot = pay.total
                    mon_10 += float(tot)

                if pay.date.month == 11 and pay.date.year == current_year:
                    tot = pay.total
                    mon_11 += float(tot)

                if pay.date.month == 12 and pay.date.year == current_year:
                    tot = pay.total
                    mon_12 += float(tot)

            for pay in payment:
                total_pay += float(pay.total)
                if pay.date.day == current_day and pay.date.month == current_month and pay.date.year == current_year:
                    tot = pay.total
                    day_pay += float(tot)
                if pay.date.month == current_month and pay.date.year == current_year:
                    tot = pay.total
                    month_pay += float(tot)
                if pay.date.year == current_year:
                    tot = pay.total
                    year_pay += float(tot)

            cset = Settings.objects.update_or_create(username=request.user)
            sett = Settings.objects.get(username=request.user)
            StartDate = datetime.date.today()
            EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_s = True
                noti_s_count = medicine_all.count()
                notifi += 1
            else:
                noti_s = False
                noti_s_count = 0

            StartDate = "2000-01-01"
            EndDate = datetime.date.today()
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_e = True
                noti_e_count = medicine_all.count()
                notifi += 1
            else:
                noti_e = False
                noti_e_count = 0

            medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

            if medicine_all:
                noti_l = True
                noti_l_count = medicine_all.count()
                notifi += 1
            else:
                noti_l = False
                noti_l_count = 0

            context = {
                'profile_user': profile_user,
                'payment_all': payment_all,
                'payment_year': payment_year,
                'payment_month': payment_month,
                'payment_day': payment_day,
                'total_pay': total_pay,
                'year_pay': year_pay,
                'month_pay': month_pay,
                'day_pay': day_pay,
                'mon_1': mon_1,
                'mon_2': mon_2,
                'mon_3': mon_3,
                'mon_4': mon_4,
                'mon_5': mon_5,
                'mon_6': mon_6,
                'mon_7': mon_7,
                'mon_8': mon_8,
                'mon_9': mon_9,
                'mon_10': mon_10,
                'mon_11': mon_11,
                'mon_12': mon_12,
                'current_year': current_year,
                'payment_user_one': payment_user_one,
                'payment_user': payment_user,
                'end_days': end_days,
                'noti_s': noti_s,
                'noti_s_count': noti_s_count,
                'sett': sett,
                'noti_e': noti_e,
                'noti_e_count': noti_e_count,
                'noti_l': noti_l,
                'noti_l_count': noti_l_count,
                'notifi': notifi,
            }
            return render(request, 'pharmacy/home.html', context)

        # elif profile_user.type == 'hospital':
        #     return render(request, 'accounts/test.html')
        #
        # elif profile_user.type == 'school':
        #     return render(request, 'accounts/test.html')
        #
        # elif profile_user.type == 'sales':
        #     return render(request, 'accounts/test.html')

        else:
            raise PermissionDenied

    else:
        raise PermissionDenied


def category(request, username):
    profile_user = Accounts.objects.get(username=username)
    category_all = Category.objects.filter(username=profile_user.id)
    category = Category.objects.filter(username=profile_user.id)

    payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

    notifi = 0

    year = 2000
    month = 1
    day = 1

    for payment in payment_user_one:
        day = payment.end_billing.day
        month = payment.end_billing.month
        year = payment.end_billing.year

    a = datetime.datetime.now()
    b = datetime.datetime(year, month, day)
    end = b - a
    if end.days <= 30:
        end_days = end.days
        notifi += 1
    else:
        end_days = ''

    sett = Settings.objects.get(username=request.user)
    StartDate = datetime.date.today()
    EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
    medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

    if medicine_all:
        noti_s = True
        noti_s_count = medicine_all.count()
        notifi += 1
    else:
        noti_s = False
        noti_s_count = 0

    StartDate = "2000-01-01"
    EndDate = datetime.date.today()
    medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

    if medicine_all:
        noti_e = True
        noti_e_count = medicine_all.count()
        notifi += 1
    else:
        noti_e = False
        noti_e_count = 0

    medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

    if medicine_all:
        noti_l = True
        noti_l_count = medicine_all.count()
        notifi += 1
    else:
        noti_l = False
        noti_l_count = 0

    paginator = Paginator(category, 20)
    page = request.GET.get('page')
    try:
        category = paginator.page(page)
    except PageNotAnInteger:
        category = paginator.page(1)
    except EmptyPage:
        category = paginator.page(paginator.num_pages)

    # Search
    item_name = request.GET.get('item_name')
    categories = Category.objects.filter(name=item_name)

    # for cat in category:
    #     med_num = Medicine.objects.filter(username=profile_user, category=cat)
    #     print(len(med_num))

    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            context = {
                'profile_user': profile_user,
                'category': category,
                'category_all': category_all,
                'categories': categories,
                'end_days': end_days,
                'noti_s': noti_s,
                'noti_s_count': noti_s_count,
                'sett': sett,
                'noti_e': noti_e,
                'noti_e_count': noti_e_count,
                'noti_l': noti_l,
                'noti_l_count': noti_l_count,
                'notifi': notifi,
            }
            return render(request, 'pharmacy/category.html', context)
        else:
            raise PermissionDenied


def new_category(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

            notifi = 0

            year = 2000
            month = 1
            day = 1

            for payment in payment_user_one:
                day = payment.end_billing.day
                month = payment.end_billing.month
                year = payment.end_billing.year

            a = datetime.datetime.now()
            b = datetime.datetime(year, month, day)
            end = b - a
            if end.days <= 30:
                end_days = end.days
                notifi += 1
            else:
                end_days = ''

            sett = Settings.objects.get(username=request.user)
            StartDate = datetime.date.today()
            EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_s = True
                noti_s_count = medicine_all.count()
                notifi += 1
            else:
                noti_s = False
                noti_s_count = 0

            StartDate = "2000-01-01"
            EndDate = datetime.date.today()
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_e = True
                noti_e_count = medicine_all.count()
                notifi += 1
            else:
                noti_e = False
                noti_e_count = 0

            medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

            if medicine_all:
                noti_l = True
                noti_l_count = medicine_all.count()
                notifi += 1
            else:
                noti_l = False
                noti_l_count = 0

            if request.method == 'POST':
                category_form = AddCategoryForm(data=request.POST)
                if category_form.is_valid():
                    new_med = category_form.save(commit=False)
                    new_med.username = request.user
                    new_med.save()
                    messages.success(request, "تم اضافة " + request.POST['name'] + " الي الفئات بنجاح ...")
            else:
                category_form = AddCategoryForm()
            context = {
                'profile_user': profile_user,
                'category_form': category_form,
                'end_days': end_days,
                'noti_s': noti_s,
                'noti_s_count': noti_s_count,
                'sett': sett,
                'noti_e': noti_e,
                'noti_e_count': noti_e_count,
                'noti_l': noti_l,
                'noti_l_count': noti_l_count,
                'notifi': notifi,

            }
            return render(request, 'pharmacy/new_category.html', context)
        else:
            raise BadRequest


def update_category(request, username, id):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            category = Category.objects.get(id=id)
            if category.username == request.user:
                payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

                notifi = 0

                year = 2000
                month = 1
                day = 1

                for payment in payment_user_one:
                    day = payment.end_billing.day
                    month = payment.end_billing.month
                    year = payment.end_billing.year

                a = datetime.datetime.now()
                b = datetime.datetime(year, month, day)
                end = b - a
                if end.days <= 30:
                    end_days = end.days
                    notifi += 1
                else:
                    end_days = ''

                sett = Settings.objects.get(username=request.user)
                StartDate = datetime.date.today()
                EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
                medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

                if medicine_all:
                    noti_s = True
                    noti_s_count = medicine_all.count()
                    notifi += 1
                else:
                    noti_s = False
                    noti_s_count = 0

                StartDate = "2000-01-01"
                EndDate = datetime.date.today()
                medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

                if medicine_all:
                    noti_e = True
                    noti_e_count = medicine_all.count()
                    notifi += 1
                else:
                    noti_e = False
                    noti_e_count = 0

                medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

                if medicine_all:
                    noti_l = True
                    noti_l_count = medicine_all.count()
                    notifi += 1
                else:
                    noti_l = False
                    noti_l_count = 0
                if request.method == 'POST':
                    category_form = UpdateCategoryForm(data=request.POST)
                    if category_form.is_valid():
                        update_cat = category_form.save(commit=False)
                        update_cat.id = category.id
                        update_cat.username = category.username
                        update_cat.save()
                        return HttpResponseRedirect(f"/pharmacy/{profile_user.username}/category/")
                else:
                    category_form = UpdateCategoryForm(instance=category)
                context = {
                    'profile_user': profile_user,
                    'category_form': category_form,
                    'category': category,
                    'end_days': end_days,
                    'noti_s': noti_s,
                    'noti_s_count': noti_s_count,
                    'sett': sett,
                    'noti_e': noti_e,
                    'noti_e_count': noti_e_count,
                    'noti_l': noti_l,
                    'noti_l_count': noti_l_count,
                    'notifi': notifi,
                }
                return render(request, 'pharmacy/update_category.html', context)
            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404


def delete_category(request, username, id):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            category = Category.objects.get(id=id)
            if category.username == request.user:
                category.delete()
                return HttpResponseRedirect(f"/pharmacy/{profile_user.username}/category/")
            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404


def medicine(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

            notifi = 0

            year = 2000
            month = 1
            day = 1

            for payment in payment_user_one:
                day = payment.end_billing.day
                month = payment.end_billing.month
                year = payment.end_billing.year

            a = datetime.datetime.now()
            b = datetime.datetime(year, month, day)
            end = b - a
            if end.days <= 30:
                end_days = end.days
                notifi += 1
            else:
                end_days = ''

            sett = Settings.objects.get(username=request.user)
            StartDate = datetime.date.today()
            EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_s = True
                noti_s_count = medicine_all.count()
                notifi += 1
            else:
                noti_s = False
                noti_s_count = 0

            StartDate = "2000-01-01"
            EndDate = datetime.date.today()
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_e = True
                noti_e_count = medicine_all.count()
                notifi += 1
            else:
                noti_e = False
                noti_e_count = 0

            medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

            if medicine_all:
                noti_l = True
                noti_l_count = medicine_all.count()
                notifi += 1
            else:
                noti_l = False
                noti_l_count = 0

            medicine_all = Medicine.objects.filter(username=profile_user.id)
            medicine = Medicine.objects.filter(username=profile_user.id)
            paginator = Paginator(medicine, 20)
            page = request.GET.get('page')
            try:
                medicine = paginator.page(page)
            except PageNotAnInteger:
                medicine = paginator.page(1)
            except EmptyPage:
                medicine = paginator.page(paginator.num_pages)

            # Search
            item_name = request.GET.get('item_name')
            medicines = Medicine.objects.filter(name=item_name, username=profile_user.id)

            context = {
                'profile_user': profile_user,
                'category': category,
                'medicine_all': medicine_all,
                'medicine': medicine,
                'medicines': medicines,
                'end_days': end_days,
                'noti_s': noti_s,
                'noti_s_count': noti_s_count,
                'sett': sett,
                'noti_e': noti_e,
                'noti_e_count': noti_e_count,
                'noti_l': noti_l,
                'noti_l_count': noti_l_count,
                'notifi': notifi,
            }
            return render(request, 'pharmacy/medicine.html', context)
        else:
            raise PermissionDenied


def new_medicine(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

            notifi = 0

            year = 2000
            month = 1
            day = 1

            for payment in payment_user_one:
                day = payment.end_billing.day
                month = payment.end_billing.month
                year = payment.end_billing.year

            a = datetime.datetime.now()
            b = datetime.datetime(year, month, day)
            end = b - a
            if end.days <= 30:
                end_days = end.days
                notifi += 1
            else:
                end_days = ''

            sett = Settings.objects.get(username=request.user)
            StartDate = datetime.date.today()
            EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_s = True
                noti_s_count = medicine_all.count()
                notifi += 1
            else:
                noti_s = False
                noti_s_count = 0

                StartDate = "2000-01-01"
                EndDate = datetime.date.today()
                medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_e = True
                noti_e_count = medicine_all.count()
                notifi += 1
            else:
                noti_e = False
                noti_e_count = 0

            medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

            if medicine_all:
                noti_l = True
                noti_l_count = medicine_all.count()
                notifi += 1
            else:
                noti_l = False
                noti_l_count = 0

            if request.method == 'POST':
                medicine_form = AddMedicineForm(data=request.POST, user=profile_user)
                if medicine_form.is_valid():
                    new_med = medicine_form.save(commit=False)
                    new_med.username = request.user
                    new_med.save()
                    messages.success(request, "تم اضافة " + request.POST['name'] + " الي الأدوية بنجاح ...")
            else:
                medicine_form = AddMedicineForm(user=profile_user)
            context = {
                'profile_user': profile_user,
                'medicine_form': medicine_form,
                'end_days': end_days,
                'noti_s': noti_s,
                'noti_s_count': noti_s_count,
                'sett': sett,
                'noti_e': noti_e,
                'noti_e_count': noti_e_count,
                'noti_l': noti_l,
                'noti_l_count': noti_l_count,
                'notifi': notifi,
            }
            return render(request, 'pharmacy/new_medicine.html', context)
        else:
            raise BadRequest


def update_medicine(request, username, id):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            medicine = Medicine.objects.get(id=id)
            if medicine.username == request.user:
                payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

                notifi = 0

                year = 2000
                month = 1
                day = 1

                for payment in payment_user_one:
                    day = payment.end_billing.day
                    month = payment.end_billing.month
                    year = payment.end_billing.year

                a = datetime.datetime.now()
                b = datetime.datetime(year, month, day)
                end = b - a
                if end.days <= 30:
                    end_days = end.days
                    notifi += 1
                else:
                    end_days = ''

                sett = Settings.objects.get(username=request.user)
                StartDate = datetime.date.today()
                EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
                medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

                if medicine_all:
                    noti_s = True
                    noti_s_count = medicine_all.count()
                    notifi += 1
                else:
                    noti_s = False
                    noti_s_count = 0

                StartDate = "2000-01-01"
                EndDate = datetime.date.today()
                medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

                if medicine_all:
                    noti_e = True
                    noti_e_count = medicine_all.count()
                    notifi += 1
                else:
                    noti_e = False
                    noti_e_count = 0

                medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

                if medicine_all:
                    noti_l = True
                    noti_l_count = medicine_all.count()
                    notifi += 1
                else:
                    noti_l = False
                    noti_l_count = 0
                if request.method == 'POST':
                    medicine_form = UpdateMedicineForm(data=request.POST, user=profile_user)
                    if medicine_form.is_valid():
                        update_med = medicine_form.save(commit=False)
                        update_med.id = medicine.id
                        update_med.username = medicine.username
                        update_med.save()
                        return HttpResponseRedirect(f"/pharmacy/{profile_user.username}/medicine/")
                else:
                    medicine_form = UpdateMedicineForm(user=profile_user, instance=medicine)
                context = {
                    'profile_user': profile_user,
                    'medicine_form': medicine_form,
                    'end_days': end_days,
                    'noti_s': noti_s,
                    'noti_s_count': noti_s_count,
                    'sett': sett,
                    'noti_e': noti_e,
                    'noti_e_count': noti_e_count,
                    'noti_l': noti_l,
                    'noti_l_count': noti_l_count,
                    'notifi': notifi,
                }
                return render(request, 'pharmacy/update_medicine.html', context)
            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404


def delete_medicine(request, username, id):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            medicine = Medicine.objects.get(id=id)
            if medicine.username == request.user:
                medicine.delete()
                return HttpResponseRedirect(f"/pharmacy/{profile_user.username}/medicine/")
            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404


def payment(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

            notifi = 0

            year = 2000
            month = 1
            day = 1

            for payment in payment_user_one:
                day = payment.end_billing.day
                month = payment.end_billing.month
                year = payment.end_billing.year

            a = datetime.datetime.now()
            b = datetime.datetime(year, month, day)
            end = b - a
            if end.days <= 30:
                end_days = end.days
                notifi += 1
            else:
                end_days = ''

            sett = Settings.objects.get(username=request.user)
            StartDate = datetime.date.today()
            EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_s = True
                noti_s_count = medicine_all.count()
                notifi += 1
            else:
                noti_s = False
                noti_s_count = 0

            StartDate = "2000-01-01"
            EndDate = datetime.date.today()
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_e = True
                noti_e_count = medicine_all.count()
                notifi += 1
            else:
                noti_e = False
                noti_e_count = 0

            medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

            if medicine_all:
                noti_l = True
                noti_l_count = medicine_all.count()
                notifi += 1
            else:
                noti_l = False
                noti_l_count = 0

            payments = Payment.objects.filter(username=request.user)
            context = {
                'profile_user': profile_user,
                'category': category,
                'medicine': medicine,
                'payments': payments,
                'end_days': end_days,
                'noti_s': noti_s,
                'noti_s_count': noti_s_count,
                'sett': sett,
                'noti_e': noti_e,
                'noti_e_count': noti_e_count,
                'noti_l': noti_l,
                'noti_l_count': noti_l_count,
                'notifi': notifi,
            }
            return render(request, 'pharmacy/payment.html', context)
        else:
            raise PermissionDenied


def new_payment(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

            notifi = 0

            year = 2000
            month = 1
            day = 1

            for payment in payment_user_one:
                day = payment.end_billing.day
                month = payment.end_billing.month
                year = payment.end_billing.year

            a = datetime.datetime.now()
            b = datetime.datetime(year, month, day)
            end = b - a
            if end.days <= 30:
                end_days = end.days
                notifi += 1
            else:
                end_days = ''

            sett = Settings.objects.get(username=request.user)
            StartDate = datetime.date.today()
            EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_s = True
                noti_s_count = medicine_all.count()
                notifi += 1
            else:
                noti_s = False
                noti_s_count = 0

            StartDate = "2000-01-01"
            EndDate = datetime.date.today()
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_e = True
                noti_e_count = medicine_all.count()
                notifi += 1
            else:
                noti_e = False
                noti_e_count = 0

            medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

            if medicine_all:
                noti_l = True
                noti_l_count = medicine_all.count()
                notifi += 1
            else:
                noti_l = False
                noti_l_count = 0
            fdata = ''
            medicine = Medicine.objects.filter(username=profile_user.id)
            if request.is_ajax():
                if request.method == 'POST':
                    data = json.loads(request.body)
                    product = []
                    qty = []
                    for x in data.keys():
                        if x == 'key1':
                            list = data.get(x)
                            for y in list:
                                product.append(y)
                        elif x == 'key2':
                            list = data.get(x)
                            for y in list:
                                qty.append(y)

                    counter = 0
                    for x in product:
                        pro = Medicine.objects.get(id=product[counter])
                        final_qty = pro.quantity - qty[counter]
                        dname = pro.name
                        dqty = qty[counter]

                        fdata += str(dname) + '\n' + 'qty: ' + str(dqty) + '\n'
                        if final_qty == -1:
                            pass
                        else:
                            pro.quantity = final_qty
                            pro.save()
                        counter += 1

                    items_form = ItemsForm(data=request.POST)
                    if items_form.is_valid():
                        new_item = items_form.save(commit=False)
                        new_item.username = request.user
                        new_item.data = str(fdata)
                        new_item.total = data['key3']
                        new_item.save()
                    pass
                else:
                    pass
            else:
                pass
            try:
                if request.method == 'POST':
                    items = Items.objects.filter(username=request.user)
                    adata = (items[len(items) - 1].data)
                    atotal = (items[len(items) - 1].total)
                    payment_form = NewPaymentForm(data=request.POST)
                    if payment_form.is_valid():
                        new_pay = payment_form.save(commit=False)
                        new_pay.username = request.user
                        new_pay.data = str(adata)
                        new_pay.total = atotal
                        new_pay.save()
                        items.delete()
                    return HttpResponseRedirect(f"/pharmacy/{profile_user.username}/medicine/")
                else:
                    payment_form = NewPaymentForm()
            except:
                payment_form = NewPaymentForm()
            context = {
                'profile_user': profile_user,
                'category': category,
                'medicine': medicine,
                'payment_form': payment_form,
                'end_days': end_days,
                'noti_s': noti_s,
                'noti_s_count': noti_s_count,
                'sett': sett,
                'noti_e': noti_e,
                'noti_e_count': noti_e_count,
                'noti_l': noti_l,
                'noti_l_count': noti_l_count,
                'notifi': notifi,
            }
            return render(request, 'pharmacy/new_payment.html', context)


def add_payment(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

            notifi = 0

            year = 2000
            month = 1
            day = 1

            for payment in payment_user_one:
                day = payment.end_billing.day
                month = payment.end_billing.month
                year = payment.end_billing.year

            a = datetime.datetime.now()
            b = datetime.datetime(year, month, day)
            end = b - a
            if end.days <= 30:
                end_days = end.days
                notifi += 1
            else:
                end_days = ''

            sett = Settings.objects.get(username=request.user)
            StartDate = datetime.date.today()
            EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_s = True
                noti_s_count = medicine_all.count()
                notifi += 1
            else:
                noti_s = False
                noti_s_count = 0

            StartDate = "2000-01-01"
            EndDate = datetime.date.today()
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_e = True
                noti_e_count = medicine_all.count()
                notifi += 1
            else:
                noti_e = False
                noti_e_count = 0

            medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

            if medicine_all:
                noti_l = True
                noti_l_count = medicine_all.count()
                notifi += 1
            else:
                noti_l = False
                noti_l_count = 0
            if request.method == 'POST':
                payment_form = AddPaymentForm(data=request.POST)
                if payment_form.is_valid():
                    add_pay = payment_form.save(commit=False)
                    add_pay.username = request.user
                    add_pay.save()
                    messages.success(request, "تم اضافة الفاتورة بنجاح")
            else:
                payment_form = AddPaymentForm()
            context = {
                'profile_user': profile_user,
                'payment_form': payment_form,
                'end_days': end_days,
                'noti_s': noti_s,
                'noti_s_count': noti_s_count,
                'sett': sett,
                'noti_e': noti_e,
                'noti_e_count': noti_e_count,
                'noti_l': noti_l,
                'noti_l_count': noti_l_count,
                'notifi': notifi,
            }
            return render(request, 'pharmacy/add_payment.html', context)
        else:
            raise BadRequest


def update_payment(request, username, id):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            payment_user_one = Payments.objects.filter(username=profile_user.id)[0:1]

            notifi = 0

            year = 2000
            month = 1
            day = 1

            for payment in payment_user_one:
                day = payment.end_billing.day
                month = payment.end_billing.month
                year = payment.end_billing.year

            a = datetime.datetime.now()
            b = datetime.datetime(year, month, day)
            end = b - a
            if end.days <= 30:
                end_days = end.days
                notifi += 1
            else:
                end_days = ''

            sett = Settings.objects.get(username=request.user)
            StartDate = datetime.date.today()
            EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_s = True
                noti_s_count = medicine_all.count()
                notifi += 1
            else:
                noti_s = False
                noti_s_count = 0

            StartDate = "2000-01-01"
            EndDate = datetime.date.today()
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            if medicine_all:
                noti_e = True
                noti_e_count = medicine_all.count()
                notifi += 1
            else:
                noti_e = False
                noti_e_count = 0

            medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)

            if medicine_all:
                noti_l = True
                noti_l_count = medicine_all.count()
                notifi += 1
            else:
                noti_l = False
                noti_l_count = 0
            payment = Payment.objects.get(id=id)
            if payment.username == request.user:
                if request.method == 'POST':
                    payment_form = UpdatePaymentForm(data=request.POST)
                    if payment_form.is_valid():
                        update_pay = payment_form.save(commit=False)
                        update_pay.id = payment.id
                        update_pay.username = payment.username
                        update_pay.data = payment.data
                        update_pay.save()
                        return HttpResponseRedirect(f"/pharmacy/{profile_user.username}/payment/")
                else:
                    payment_form = UpdatePaymentForm(instance=payment)
                context = {
                    'profile_user': profile_user,
                    'payment_form': payment_form,
                    'payment_id': payment.id,
                    'end_days': end_days,
                    'noti_s': noti_s,
                    'noti_s_count': noti_s_count,
                    'sett': sett,
                    'noti_e': noti_e,
                    'noti_e_count': noti_e_count,
                    'noti_l': noti_l,
                    'noti_l_count': noti_l_count,
                    'notifi': notifi,

                }
                return render(request, 'pharmacy/UPDATE_PAYMENT.html', context)
            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404


def delete_payment(request, username, id):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            payment = Payment.objects.get(id=id)
            if payment.username == request.user:
                payment.delete()
                return HttpResponseRedirect(f"/pharmacy/{profile_user.username}/payment/")
            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404


def expiration(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            cset = Settings.objects.update_or_create(username=request.user)
            sett = Settings.objects.get(username=request.user)
            StartDate = datetime.date.today()
            EndDate = datetime.date.today() + datetime.timedelta(days=sett.days)
            shorts = Medicine.objects.filter(username=request.user, end_date__range=[StartDate, EndDate])
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])
            # Search
            item_name = request.GET.get('item_name')
            medicines = Medicine.objects.filter(name=item_name, username=profile_user.id,
                                                end_date__range=[StartDate, EndDate])

            context = {
                'profile_user': profile_user,
                'shorts': shorts,
                'medicine_all': medicine_all,
                'medicines': medicines,
                'sett': sett,
            }

            return render(request, 'pharmacy/expiration.html', context)

        else:

            raise BadRequest
    else:
        raise Http404


def end_expiration(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            cset = Settings.objects.update_or_create(username=request.user)
            StartDate = "2000-01-01"
            EndDate = datetime.date.today()
            shorts = Medicine.objects.filter(username=request.user, end_date__range=[StartDate, EndDate])
            medicine_all = Medicine.objects.filter(username=profile_user.id, end_date__range=[StartDate, EndDate])

            # Search
            item_name = request.GET.get('item_name')
            medicines = Medicine.objects.filter(name=item_name, username=profile_user.id,
                                                end_date__range=[StartDate, EndDate])

            context = {
                'profile_user': profile_user,
                'shorts': shorts,
                'medicine_all': medicine_all,
                'medicines': medicines,
            }

            return render(request, 'pharmacy/end_expiration.html', context)

        else:

            raise BadRequest
    else:
        raise Http404


def settings(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            cset = Settings.objects.update_or_create(username=request.user)
            sett = Settings.objects.get(username=request.user)
            if request.method == 'POST':
                settings_form = SettingsForm(data=request.POST)
                if settings_form.is_valid():
                    sett.username = request.user
                    sett.days = request.POST['days']
                    sett.qty = request.POST['qty']
                    sett.save()
                    return HttpResponseRedirect(f"/pharmacy/{profile_user.username}/settings/")
            else:
                settings_form = SettingsForm(instance=sett)

            context = {
                'profile_user': profile_user,
                'settings_form': settings_form
            }
            return render(request, 'pharmacy/settings.html', context)

        else:

            raise BadRequest
    else:
        raise Http404


def shortcomings(request, username):
    profile_user = Accounts.objects.get(username=username)
    if request.user == profile_user:
        if profile_user.type == 'pharmacy':
            cset = Settings.objects.update_or_create(username=request.user)
            sett = Settings.objects.get(username=request.user)
            shorts = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)
            medicine_all = Medicine.objects.filter(username=request.user, quantity__lte=sett.qty)
            # Search
            item_name = request.GET.get('item_name')
            medicines = Medicine.objects.filter(name=item_name, username=profile_user.id, quantity__lte=sett.qty)

            context = {
                'profile_user': profile_user,
                'shorts': shorts,
                'medicine_all': medicine_all,
                'medicines': medicines,
                'sett': sett
            }

            return render(request, 'pharmacy/shortcomings.html', context)

        else:

            raise BadRequest
    else:
        raise Http404
