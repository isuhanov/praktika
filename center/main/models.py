from django.db import models

#модель таблицы Klient 
class Klient(models.Model):
    id_kl = models.AutoField(blank=False, primary_key=True)
    fio = models.CharField(max_length=100, blank=False)
    bd = models.DateField(blank=False)
    phone = models.CharField(max_length=11, blank=False)
    mail = models.CharField(max_length=100, blank=False)
    pasp_seria = models.CharField(max_length=4,blank=False)
    pasp_nomer = models.CharField(max_length=6, blank=False)

#модель таблицы Seller
class Seller(models.Model):
    id_seller = models.AutoField(blank=False, primary_key=True)
    id_kl = models.ForeignKey(Klient, on_delete=models.CASCADE, blank=False)
    status = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return str(self.id_seller)

#модель таблицы Flat
class Flat(models.Model):
    id_fl = models.AutoField(blank=False, primary_key=True)
    coast = models.IntegerField(blank=False)
    descr = models.TextField(blank=False)
    rooms = models.IntegerField(blank=False)
    adress = models.CharField(max_length=150, blank=False)
    square_f = models.IntegerField(blank=False)
    id_seller = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=False, null=True)
    status = models.CharField(max_length=10, blank=False) 


    def __str__(self):
        return str(self.id_fl)

#модель таблицы Buyer
class Buyer(models.Model):
    id_buyer = models.AutoField(blank=False, primary_key=True)
    id_kl = models.ForeignKey(Klient, on_delete=models.CASCADE, blank=False)
    wish_room = models.IntegerField(blank=False)
    wish_adress = models.CharField(max_length=150, blank=False)
    wish_square = models.IntegerField(blank=False)
    budget = models.IntegerField(blank=False)
    status = models.CharField(max_length=10, blank=False)


    def __str__(self):
        return str(self.id_buyer)

#модель таблицы Contract
class Contract(models.Model):
    id_contract = models.AutoField(blank=False, primary_key=True)
    id_buyer = models.ForeignKey(Buyer, on_delete = models.CASCADE, blank=False)
    id_seller = models.ForeignKey(Seller, on_delete = models.CASCADE, blank=False)
    id_fl = models.ForeignKey(Flat, on_delete=models.CASCADE, blank=False)
    time_to_sale = models.DateField(blank=False)
    coast = models.IntegerField(blank=False)
    proc_for_comp = models.IntegerField(blank=False)
    time_create = models.DateField(auto_now_add=True, blank=False)

    def __str__(self):
        return str(self.id_contract)