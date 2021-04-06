from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .forms import *

def index(request):
    return render(request, 'main/index.html')


class SellerView(View):
    def get(self,request):
        seller = Seller.objects.values('id_kl')# SELECT id_kl FROM Seller
        klient = Klient.objects.all()#SELECT * FROM Klient
        sel_list_act = Seller.objects.filter(status='активен')
        sel_list_disact = Seller.objects.filter(status='неактивен')
        return render(request, 'main/seller_view.html', context={'seller': seller, 'klient': klient, 'sel_list_act': sel_list_act, 'sel_list_disact': sel_list_disact})


class BuyerView(View):
    def get(self,request):
        buyer = Buyer.objects.values('id_kl')# SELECT id_kl FROM Buyer
        klient = Klient.objects.all()#SELECT * FROM Klient
        b_list_act = Buyer.objects.filter(status='активен')
        b_list_dis_act = Buyer.objects.filter(status='неактивен')
        return render(request, 'main/buyer_view.html', context={'buyer': buyer, 'klient': klient, 'b_list_act': b_list_act, 'b_list_dis_act': b_list_dis_act})


class ContractView(View):
    def get(self,request):
        # id_b = Contract.objects.get(id_contract=1).id_buyer
        contract =Contract.objects.all()#SELECT * FROM Contract
        klient = Klient.objects.all()#SELECT * FROM Klient
        flat = Flat.objects.all()#SELECT * FROM Flat

        return render(request, 'main/contract_view.html', context={'contract': contract, 'klient': klient, 'flat': flat})


class FlatView(View):
    def get(sefl, request):
        flat = Flat.objects.all()#SELECT * FROM Flat
        return render(request, 'main/flat_view.html', context={'flat': flat})

class CreateSeller(View):
    def get(self,request):
        seller = SellerForm()
        return render(request, 'main/seller_create.html' ,context={'seller': seller})

    def post(self, request):
        bound_form = SellerForm(request.POST)

        if bound_form.is_valid():
            new_klient = bound_form.save_k()
            new_seller = bound_form.save_sel()
            new_flat = bound_form.save_fl()

            return render(request, 'main/succes.html')

        return render(request, 'main/seller_create.html' ,context={'seller': bound_form})

class CreateBuyer(View):
    def get(self, request):
        buyer = BuyerForm()
        return render(request, 'main/buyer_create.html', context={'buyer': buyer})

    def post(self, request):
        bound_form = BuyerForm(request.POST)

        if bound_form.is_valid():
            new_klient = bound_form.save_k()
            new_buyer = bound_form.save_b()

            return render(request, 'main/succes.html')

        return render(request, 'main/buyer_create.html' ,context={'buyer': bound_form}) 

class AddFlat(View):
    def get(self,request):
        flat = FlatForm()
        return render(request, 'main/flat_add.html', context={'flat': flat})

    def post(self,request):
        bound_form = FlatForm(request.POST)

        if bound_form.is_valid():
            new_flat = bound_form.save()

            return render(request, 'main/succes.html')

        return render(request, 'main/flat_add.html', context={'flat': bound_form})


class CreateContract(View):
    def get(self,request):
        contract = ContractForm()
        return render(request, 'main/contract_create.html', context={'contract': contract})


    def post(self, request):
        bound_form = ContractForm(request.POST)

        if bound_form.is_valid():
            new_contract = bound_form.save()
            new_doc = bound_form.create_contr()
            return render(request, 'main/succes.html')

        return render(request, 'main/contract_create.html', context={'contract': bound_form})
