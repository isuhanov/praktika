from django import template
from django.template.defaulttags import register
from main.models import *

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_status(sel_list, id_k):
    print(sel_list)
    print('test')
    seller_status = sel_list.get(id_kl = id_k).status
    print(seller_status)

    return seller_status


def get_p_data(id_obj_field, obj_id, p_data):
    main_list = Contract.objects.values('id_contract', id_obj_field)
    for obj in main_list:                    #узнаю id неоходимого клиента
        if obj_id == obj['id_contract']:
            id_kl_contr = obj[id_obj_field]

    if id_obj_field == 'id_buyer':              #узнаю id необходимого клиента в нужной таблице
        some_kl_list = Buyer.objects.filter(id_buyer=id_kl_contr).values('id_kl')
    else:
        some_kl_list = Seller.objects.filter(id_seller=id_kl_contr).values('id_kl')

    klient_list = Klient.objects.all()

    for some_kl in some_kl_list:               #получаю нужные паспортные даты
        for kl in klient_list:
            if some_kl['id_kl'] == kl.id_kl:
                if p_data == 'номер':
                    p_data_kl = Klient.objects.get(id_kl=kl.id_kl).pasp_nomer
                elif p_data == 'серия':
                    p_data_kl = Klient.objects.get(id_kl=kl.id_kl).pasp_seria
    return p_data_kl


@register.filter
def get_buyer_pseria(model_info, obj_id):
    p_seria_b = get_p_data('id_buyer', obj_id, 'серия')
    return p_seria_b

@register.filter
def get_buyer_pnomer(model_info, obj_id):
    p_nomer_b = get_p_data('id_buyer', obj_id, 'номер')
    return p_nomer_b

@register.filter
def get_seller_pseria(model_info, obj_id):
    p_seria_s = get_p_data('id_seller', obj_id, 'серия')
    return p_seria_s

@register.filter
def get_seller_pnomer(model_info, obj_id):
    p_nomer_s = get_p_data('id_seller', obj_id, 'номер')
    return p_nomer_s

@register.filter
def get_adress(flat, obj_id):
    contr_list = Contract.objects.values('id_contract', 'id_fl')
    for contr in contr_list:
        if obj_id == contr['id_contract']:
            id_f = contr['id_fl']

    adress = Flat.objects.get(id_fl=id_f).adress
    return adress


@register.filter
def get_pseria_sel(klient, obj_id):
    flat_list = Flat.objects.values('id_fl', 'id_seller')
    for flat in flat_list:
        if obj_id == flat['id_fl']:
            id_s = flat['id_seller']
    
    seller_list = Seller.objects.filter(id_seller=id_s).values('id_kl')
    klient_list = Klient.objects.all()

    for seller in seller_list:
        for kl in klient_list:
            if seller['id_kl'] == kl.id_kl:
                p_seria_s = Klient.objects.get(id_kl=kl.id_kl).pasp_seria
    print(p_seria_s)
    return p_seria_s

@register.filter
def get_pnomer_sel(flat, obj_id):
    flat_list = Flat.objects.values('id_fl', 'id_seller')
    for flat in flat_list:
        if obj_id == flat['id_fl']:
            id_s = flat['id_seller']
    
    seller_list = Seller.objects.filter(id_seller=id_s).values('id_kl')
    klient_list = Klient.objects.all()

    for seller in seller_list:
        for kl in klient_list:
            if seller['id_kl'] == kl.id_kl:
                p_nomer_s = Klient.objects.get(id_kl=kl.id_kl).pasp_nomer
    print(p_nomer_s)
    return p_nomer_s
