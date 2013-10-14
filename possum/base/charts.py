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

from django.db.models import Max, Avg
from decimal import Decimal
import datetime
from possum.base.category import Categorie
from possum.base.product import Produit
from possum.base.payment import PaiementType
from possum.base.utils import nb_sorted
from possum.base.vat import VAT
from possum.base.payment import PaiementType
from possum.base.monthly_stat import MonthlyStat
import logging
from chartit import PivotDataPool, PivotChart
from possum.base.utils import month_name, month_sort

logger = logging.getLogger(__name__)

def get_datapool_year(year, keys):
    logger.debug(" ")
    series = []
    objects = MonthlyStat.objects.filter(year=year)
    for key in keys.keys():
        series.append({'options': {
            'source': objects.filter(key=key),
            'categories': 'month'},
            'terms': {keys[key]: Avg('value')}
            })
    return PivotDataPool(
            series = series,
            sortf_mapf_mts=(month_sort, month_name, True))

def get_chart(datasource, graph, keys, title, xaxis):
    """
    graph: line / pie
    """
    terms = [keys[x] for x in keys.keys()]
    return PivotChart(
                datasource = datasource,
                series_options = [{
                    'options': {
                        'type': graph,
                        'stacking': False
                        },
                    'terms': terms
                    }],
                chart_options = {
                    'title': {
                        'text': title},
                    'credits': {
                        'enabled': False
                        },
                    'xAxis': {
                        'title': {
                            'text': xaxis}},
                    'yAxis': {
                        'title': {
                            'text': ''}},
                    })

def get_chart_year_ttc(year):
    keys = {"total_ttc": 'total ttc',
            "guests_total_ttc": 'restauration',
            "bar_total_ttc": 'bar'}
    try:
        datasource = get_datapool_year(year, keys)
    except:
        return False
    return get_chart(datasource, 'line', keys, "Total TTC pour l'année %s" % year, "Mois")

def get_chart_year_bar(year):
    keys = {"bar_average": 'TM/facture',
            "bar_nb": 'nb factures',
            "bar_total_ttc": 'total ttc bar'}
    try:
        datasource = get_datapool_year(year, keys)
    except:
        return False
    return get_chart(datasource, 'line', keys, "Activité bar pour l'année %s" % year, "Mois")

def get_chart_year_guests(year):
    keys = {"guests_average": 'TM/couvert',
            "guests_nb": 'nb couverts',
            "guests_total_ttc": 'total ttc restaurant'}
    try:
        datasource = get_datapool_year(year, keys)
    except:
        return False
    return get_chart(datasource, 'line', keys, "Activité restaurant pour l'année %s" % year, "Mois")

def get_chart_year_vats(year):
    keys = {}
    for vat in VAT.objects.iterator():
        key = "%s_vat" % vat.id
        keys[key] = vat.name
    try:
        datasource = get_datapool_year(year, keys)
    except:
        return False
    return get_chart(datasource, 'line', keys, "TVA pour l'année %s" % year, "Mois")

def get_chart_year_payments(year):
    charts = []
    keys_nb = {}
    keys_value = {}
    for payment in PaiementType.objects.iterator():
        key = "%s_payment_nb" % payment.id
        keys_nb[key] = payment.nom
        key = "%s_payment_value" % payment.id
        keys_value[key] = payment.nom
    try:
        datasource = get_datapool_year(year, keys_nb)
    except:
        return False
    charts.append(get_chart(datasource, 'line', keys_nb, "Nombre de paiements par type pour l'année %s" % year, "Mois"))
    try:
        datasource = get_datapool_year(year, keys_value)
    except:
        return False
    charts.append(get_chart(datasource, 'line', keys_value, "Valeur des paiements par type pour l'année %s" % year, "Mois"))
    return charts

def get_chart_year_categories(year):
    charts = []
    keys_nb = {}
    keys_value = {}
    for cat in Categorie.objects.iterator():
        key = "%s_category_nb" % cat.id
        keys_nb[key] = cat.nom
        key = "%s_category_value" % cat.id
        keys_value[key] = cat.nom
    try:
        datasource = get_datapool_year(year, keys_nb)
    except:
        return False
    title = "Nombre de vente par catégorie pour l'année %s" % year
    charts.append(get_chart(datasource, 'line', keys_nb, title, "Mois"))
    try:
        datasource = get_datapool_year(year, keys_value)
    except:
        return False
    title = "Valeur des ventes par catégorie pour l'année %s" % year
    charts.append(get_chart(datasource, 'line', keys_value, title, "Mois"))
    return charts

def get_chart_year_products(year, category):
    charts = []
    keys_nb = {}
    keys_value = {}
    for product in Produit.objects.filter(categorie=category).iterator():
        key = "%s_product_nb" % product.id
        keys_nb[key] = product.nom
        key = "%s_product_value" % product.id
        keys_value[key] = product.nom
    try:
        datasource = get_datapool_year(year, keys_nb)
    except:
        return False
    title = u"Nombre de vente pour la catégorie [%s] en %s" % (category.nom, year)
    charts.append(get_chart(datasource, 'line', keys_nb, title, "Mois"))
    try:
        datasource = get_datapool_year(year, keys_value)
    except:
        return False
    title = u"Valeur des ventes pour la catégorie [%s] en %s" % (category.nom, year)
    charts.append(get_chart(datasource, 'line', keys_value, title, "Mois"))
    return charts

