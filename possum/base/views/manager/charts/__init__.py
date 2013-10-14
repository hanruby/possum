# -*- coding: utf-8 -*-
#
#    Copyright 2009-2013 Sébastien Bonnegent
#
#    This file is part of POSSUM.
#
#    POSSUM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    POSSUM is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with POSSUM.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
logger = logging.getLogger(__name__)

from possum.base.daily_stat import DailyStat
from possum.base.bill import Facture
from possum.base.models import Printer
from possum.base.product import Produit, ProduitVendu
from possum.base.payment import PaiementType, Paiement
from possum.base.category import Categorie
from possum.base.options import Cuisson, Sauce, Accompagnement
from possum.base.location import Zone, Table
from possum.base.vat import VAT
from possum.base.forms import DateForm, WeekForm, MonthForm, YearForm

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.context_processors import PermWrapper
from django.contrib.auth.models import User, UserManager, Permission
from django.conf import settings
from django.contrib import messages
from django.utils.functional import wraps
from django.core.mail import send_mail
import os
import datetime
from possum.base.views import get_user
from possum.base.charts import *

def charts_year(request, choice='ttc'):
    """
    chart1: pour un seul graphique
    chart2: pour 2 graphiques
    """
    data = get_user(request)
#    data['charts'] = True
    data['cat_list'] = Categorie.objects.order_by('priorite', 'nom')
    data['menu_manager'] = True
    DailyStat().update()
    year = datetime.datetime.now().year
    if request.method == 'POST':
        try:
            year = int(request.POST.get('year'))
        except:
            messages.add_message(request, messages.ERROR, "La date saisie n'est pas valide.")
    if choice == 'ttc':
        data['chart1'] = get_chart_year_ttc(year)
    elif choice == 'bar':
        data['chart1'] = get_chart_year_bar(year)
    elif choice == 'guests':
        data['chart1'] = get_chart_year_guests(year)
    elif choice == 'vats':
        data['chart1'] = get_chart_year_vats(year)
    elif choice == 'payments':
        data['chart2'] = get_chart_year_payments(year)
    elif choice == 'categories':
        data['chart2'] = get_chart_year_categories(year)
    else:
        try:
            cat = Categorie.objects.get(pk=choice)
        except Categorie.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Ce type de graphique n'existe pas.")
            return HttpResponseRedirect('/manager/')
        else:
            data['chart2'] = get_chart_year_products(year, cat)
    data[choice] = True
    data['choice'] = choice
    data['year_form'] = YearForm({'year': year})
    data['year'] = year
    return render_to_response('base/manager/charts/home.html',
                    data,
                    context_instance=RequestContext(request))
