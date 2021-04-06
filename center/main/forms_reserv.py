from django import forms
from .models import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist

# from docxtpl import DocxTemplate
import datetime

set_number = {'1','2','3','4','5','6','7','8','9','0'}
set_letters_cir = {'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я', '-' }
set_letters_lat = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

def check_lettr(obj, rais_str):#проверяет строку на наличие букв
        for i in obj:
            if i in set_letters_cir or i in set_letters_lat:
                 raise ValidationError('{} не может состоять из букв'.format(rais_str))

def check_number(obj, rais_str):#проверяет строку на наличие цифр
    for i in obj:
            if i in set_number:
                raise ValidationError('{} не могут состоять из цифр'.format(rais_str))

def check_kl(pseria, pnomer, mod_obj, mod_id, mod_str):
    try:
        id_kl = Klient.objects.filter(pasp_seria = pseria).get(pasp_nomer = pnomer).id_kl#SELECT id_kl FROM Klient WHERE pasp_seria = {pseria} AND pasp_nomer = {pnomer}
        seller = mod_obj.objects.values(mod_id, 'id_kl')#SELECT {mod_id}, id_kl FROM {mod_obj}
        for sel in seller:
            if sel['id_kl'] == id_kl:
                raise ValidationError('Такой {} уже существует'.format(mod_str))
        return 'клиент есть в базе'
    except ObjectDoesNotExist:
        print('клиента нет')
        return 'новый клиент'  #хотел возвращать значения для того, чтобы понять есть клиент в бд или нет(для сохранения)

def check_exist_kl(pseria, pnomer, mod_obj, mod_id, mod_str):  #проверяет клиента на несуществование
    try:
        id_kl = Klient.objects.filter(pasp_seria = pseria).get(pasp_nomer = pnomer).id_kl#SELECT id_kl FROM Klient WHERE pasp_seria = {pseria} AND pasp_nomer = {pnomer}
        print(id_kl)
        objects = mod_obj.objects.values(mod_id, 'id_kl')#SELECT {mod_id}, id_kl FROM {mod_obj}
        for obj in objects:
            if obj['id_kl'] == id_kl:
                print('клиента есть')
                return 'клиент есть'
    except ObjectDoesNotExist:
        raise ValidationError('Такого {} не существует'.format(mod_str))
        return 'клиента нет'


class DateInput(forms.DateInput):
    input_type = 'date'



class SellerForm(forms.Form):
    fio = forms.CharField(max_length=100)
    bd = forms.DateField(widget=DateInput)
    phone = forms.CharField(max_length=11)
    mail = forms.EmailField()
    pasp_seria = forms.CharField(max_length=4)
    pasp_nomer = forms.CharField(max_length=6)

    coast = forms.IntegerField()
    descr = forms.CharField(widget=forms.Textarea)
    rooms = forms.IntegerField()
    adress = forms.CharField(max_length=150)
    square_f = forms.IntegerField()

    fio.widget.attrs.update({'class': 'from_input'})
    bd.widget.attrs.update({'class': 'from_input'})
    phone.widget.attrs.update({'class': 'from_input'})
    mail.widget.attrs.update({'class': 'from_input'})
    pasp_seria.widget.attrs.update({'class': 'from_input'})
    pasp_nomer.widget.attrs.update({'class': 'from_input'})

    coast.widget.attrs.update({'class': 'from_input'})
    descr.widget.attrs.update({'class': 'from_input form_textarea'})
    rooms.widget.attrs.update({'class': 'from_input'})
    adress.widget.attrs.update({'class': 'from_input'})
    square_f.widget.attrs.update({'class': 'from_input'})

    def clean_fio(self):
        new_fio = self.cleaned_data['fio']
        check_number(new_fio, 'Имена')
        return new_fio

    def clean_bd(self):
        new_bd = self.cleaned_data['bd']
        if datetime.date.today() <= new_bd:
            raise ValidationError('Дата рождения не может быть больше или равна настоящей')
        return new_bd

    def clean_phone(self):
        new_phone = self.cleaned_data['phone']
        phone_check = new_phone.lower()
        check_lettr(phone_check, 'Телефон')
        if len(new_phone) < 11:
            raise ValidationError('В номере слишком мало цифр')
        return new_phone

    def clean_mail(self):
        new_main = self.cleaned_data['mail']
        for i in set_letters_cir:
            if i in new_main:
                raise ValidationError('Почта должна состоять из латинскх символов')
        return new_main

    def clean_pasp_seria(self):
        self.new_pasp_seria = self.cleaned_data['pasp_seria']
        pseria_check = self.new_pasp_seria.lower()
        check_lettr(pseria_check, 'Серия паспорта')
        if len(self.new_pasp_seria) < 4:
            raise ValidationError('В серии пспорта слишком мало цифр')
        return self.new_pasp_seria

    def clean_pasp_nomer(self):
        new_pasp_nomer = self.cleaned_data['pasp_nomer']
        pnomer_check = new_pasp_nomer.lower()
        check_lettr(pnomer_check, 'Номер паспорта')
        if len(new_pasp_nomer) < 6:
            raise ValidationError('В номере паспорта слишком мало цифр')
        text = check_kl(self.new_pasp_seria, new_pasp_nomer, Seller, 'id_seller', 'продавец')#проверяю клиента на существование в бд
        return new_pasp_nomer


    def clean_adress(self):
        new_adress = self.cleaned_data['adress']
        try:
            fl = Flat.objects.filter(adress= new_adress)
        except ObjectDoesNotExist:
            return new_adress
        try:
            if fl.exclude(status='продана').get(adress=new_adress).status == 'активен':
                raise ValidationError('Квартира с таким адресом уже существует')
            else:
                return new_adress
        except:
            return new_adress



    # def clean_coast(self):
    #     new_coast = self.cleaned_data['coast']
    #     coast_check = new_coast
    #     check_lettr(coast_check, 'Цена')
    #     return new_coast

    # def clean_rooms(self):
    #     new_rooms= self.cleaned_data['rooms']
    #     rooms_check = new_rooms
    #     check_lettr(rooms_check, 'Кол-во комнат')
    #     return new_rooms

    # def clean_square_f(self):
    #     new_square_f= self.cleaned_data['square_f']
    #     square_f_check = new_square_f
    #     check_lettr(square_f_check, 'Площадь')
    #     return new_square_f


    def save_k(self):#сохраняю клиента в бд
        text_check = check_kl(self.cleaned_data['pasp_seria'],  self.cleaned_data['pasp_nomer'], Seller, 'id_seller', 'продавец')
        if text_check == 'новый клиент':
            new_klient = Klient.objects.create(                   #INSERT INTO Klient (fio, bd, phone, mail, pasp_seria, pasp_nomer) VALUES (
                fio = self.cleaned_data['fio'],                   #    {self.cleaned_data['fio']},
                bd = self.cleaned_data['bd'],                     #    {self.cleaned_data['bd']},
                phone = self.cleaned_data['phone'],               #    {self.cleaned_data['phone']},
                mail = self.cleaned_data['mail'],                 #    {self.cleaned_data['mail']},
                pasp_seria = self.cleaned_data['pasp_seria'],     #    {self.cleaned_data['pasp_seria']},
                pasp_nomer = self.cleaned_data['pasp_nomer']      #    {self.cleaned_data['pasp_nomer']}
            )                                                     #    );
            return new_klient
        elif text_check == 'клиент есть в базе':
            return False

    def save_sel(self):#сохраняю продавца в бд
        self.id_kl_sel = Klient.objects.filter(pasp_seria = self.cleaned_data['pasp_seria']).get(pasp_nomer = self.cleaned_data['pasp_nomer'])#SELECT id_kl FROM Klient WHERE pasp_seria = {self.cleaned_data['pasp_seria']} AND pasp_nomer = {self.cleaned_data['pasp_nomer']}

        new_seller = Seller.objects.create(          #INSERT INTO Seller (id_kl) VALUES (
            id_kl = self.id_kl_sel,                  #    {self.id_kl_sel},
            status = 'активен'                       #    'активен'
        )                                            #    );

        return new_seller

    def save_fl(self):#сохраняю квартиру в бд
        id_sel = Seller.objects.get(id_kl=self.id_kl_sel)#SELECT id_seller FROM Seller WHERE id_kl = {self.id_kl_sel}

        new_flat = Flat.objects.create(                        #INSERT INTO Seller (coast, descr, rooms, adress, square_f, id_seller) VALUES (
            coast = self.cleaned_data['coast'],                #    {self.cleaned_data['coast']},
            descr = self.cleaned_data['descr'],                #    {self.cleaned_data['descr']},
            rooms = self.cleaned_data['rooms'],                #    {self.cleaned_data['rooms']},
            adress = self.cleaned_data['adress'],              #    {self.cleaned_data['adress']},
            square_f = self.cleaned_data['square_f'],          #    {self.cleaned_data['square_f']},
            id_seller = id_sel,                                #    {id_sel},
            status = 'активен'                                 #    'активен'
        )                                                      #    );

        return new_flat








class BuyerForm(forms.Form):
    fio = forms.CharField(max_length=100)
    bd = forms.DateField(widget=DateInput)
    phone = forms.CharField(max_length=11)
    mail = forms.EmailField()
    pasp_seria = forms.CharField(max_length=4)
    pasp_nomer = forms.CharField(max_length=6)

    wish_room = forms.IntegerField()
    wish_adress = forms.CharField(max_length=150)
    wish_square = forms.IntegerField()
    budget = forms.IntegerField()

    fio.widget.attrs.update({'class': 'from_input'})
    bd.widget.attrs.update({'class': 'from_input'})
    phone.widget.attrs.update({'class': 'from_input'})
    mail.widget.attrs.update({'class': 'from_input'})
    pasp_seria.widget.attrs.update({'class': 'from_input'})
    pasp_nomer.widget.attrs.update({'class': 'from_input'})

    wish_room.widget.attrs.update({'class': 'from_input'})
    wish_adress.widget.attrs.update({'class': 'from_input'})
    wish_square.widget.attrs.update({'class': 'from_input'})
    budget.widget.attrs.update({'class': 'from_input'})

    def clean_fio(self):
        new_fio = self.cleaned_data['fio']
        check_number(new_fio, 'Имена')
        return new_fio

    def clean_bd(self):
        new_bd = self.cleaned_data['bd']
        if datetime.date.today() <= new_bd:
            raise ValidationError('Дата рождения не может быть больше или равна настоящей')
        return new_bd

    def clean_phone(self):
        new_phone = self.cleaned_data['phone']
        phone_check = new_phone.lower()
        check_lettr(phone_check, 'Телефон')
        if len(new_phone) < 11:
            raise ValidationError('В номере слишком мало цифр')
        return new_phone

    def clean_mail(self):
        new_main = self.cleaned_data['mail']
        for i in set_letters_cir:
            if i in new_main:
                raise ValidationError('Почта должна состоять из латинскх символов')
        return new_main

    def clean_pasp_seria(self):
        self.new_pasp_seria = self.cleaned_data['pasp_seria']
        pseria_check = self.new_pasp_seria.lower()
        check_lettr(pseria_check, 'Серия паспорта')
        if len(self.new_pasp_seria) < 4:
            raise ValidationError('В серии паспорта слишком мало цифр')
        return self.new_pasp_seria

    def clean_pasp_nomer(self):
        new_pasp_nomer = self.cleaned_data['pasp_nomer']
        pnomer_check = new_pasp_nomer.lower()
        check_lettr(pnomer_check, 'Номер паспорта')
        if len(new_pasp_nomer) < 6:
            raise ValidationError('В номере паспорта слишком мало цифр')

        try:
            # kl = Klient.objects.filter(pasp_seria = self.new_pasp_seria).get(pasp_nomer = new_pasp_nomer)
        # text_exist = check_kl(self.new_pasp_seria, new_pasp_nomer, Buyer, 'id_buyer', 'покупатель') #проверяю клиента на существование в бд
        # if  text_exist != 'новый клиент':
            kl = Klient.objects.filter(pasp_seria = self.new_pasp_seria).get(pasp_nomer = new_pasp_nomer)
            buyer = Buyer.objects.get(id_kl=kl)
            if buyer.status == 'неактивен':
                self.text = 'существует неактивен'
                return new_pasp_nomer
            else:
                self.text = 'существует активен'
                check_kl(self.new_pasp_seria, new_pasp_nomer, Buyer, 'id_buyer', 'покупатель')
        except ObjectDoesNotExist:
            self.text = 'несуществует'
            return new_pasp_nomer
        return new_pasp_nomer

    # def clean_budget(self):
    #     new_budget = self.cleaned_data['budget']
    #     budget_check = new_budget
    #     check_lettr(budget_check, 'Цена')
    #     return new_budget

    # def clean_wish_room(self):
    #     new_wish_room= self.cleaned_data['wish_room']
    #     wish_room_check = new_wish_room
    #     check_lettr(wish_room_check, 'Кол-во комнат')
    #     return new_wish_room

    # def clean_wish_square(self):
    #     new_wish_square= self.cleaned_data['wish_square']
    #     square_f_check = new_wish_square
    #     check_lettr(square_f_check, 'Площадь')
    #     return new_wish_square


    def save_k(self):#сохраняю клиента в бд
        if self.text == 'несуществует':
            text_check = check_kl(self.cleaned_data['pasp_seria'],  self.cleaned_data['pasp_nomer'], Buyer, 'id_buyer', 'покупатель')
            if text_check == 'новый клиент':
                new_klient = Klient.objects.create(                      #INSERT INTO Klient (fio, bd, phone, mail, pasp_seria, pasp_nomer) VALUES (
                    fio = self.cleaned_data['fio'],                      #    {self.cleaned_data['fio']},
                    bd = self.cleaned_data['bd'],                        #    {self.cleaned_data['bd']},
                    phone = self.cleaned_data['phone'],                  #    {self.cleaned_data['phone']},
                    mail = self.cleaned_data['mail'],                    #    {self.cleaned_data['mail']},
                    pasp_seria = self.cleaned_data['pasp_seria'],        #    {self.cleaned_data['pasp_seria']},
                    pasp_nomer = self.cleaned_data['pasp_nomer']         #    {self.cleaned_data['pasp_nomer']}
                )                                                        #    );
                self.check_exist_buyer = 'новый клиент'
                return new_klient
        elif self.text == 'существует неактивен':
            self.check_exist_buyer = 'клиент создан'
            return False

    def save_b(self):#сохраняю поупателя в бд
        id_kl_b = Klient.objects.filter(pasp_seria = self.cleaned_data['pasp_seria']).get(pasp_nomer = self.cleaned_data['pasp_nomer'])#SELECT id_kl FROM Klient WHERE pasp_seria = {self.cleaned_data['pasp_seria']} AND pasp_nomer = {self.cleaned_data['pasp_nomer']}

        if self.text == 'несуществует':
            print('в функции несузествующий')
            # text_exist = check_kl(self.cleaned_data['pasp_seria'], self.cleaned_data['pasp_nomer'], Buyer, 'id_buyer', 'покупатель')
            if self.check_exist_buyer == 'новый клиент':
                new_buyer = Buyer.objects.create(                       #INSERT INTO Buyer (id_kl, wish_room, wish_adress, wish_square, budget) VALUES (
                    id_kl = id_kl_b,                                    #   {id_kl_b},
                    wish_room = self.cleaned_data['wish_room'],         #   {self.cleaned_data['wish_room']},
                    wish_adress = self.cleaned_data['wish_adress'],     #   {self.cleaned_data['wish_adress']},
                    wish_square = self.cleaned_data['wish_square'],     #   {self.cleaned_data['wish_square']},
                    budget = self.cleaned_data['budget'],              #   {self.cleaned_data['budget']},
                    status = 'активен'                                  #   'активен'
                )                                                       #    );
                return new_buyer
        else:
            buyer = Buyer.objects.get(id_kl=id_kl_b)
            if buyer.status == 'неактивен':
                buyer.status = 'активен'
                buyer.wish_room = self.cleaned_data['wish_room']
                buyer.wish_adress = self.cleaned_data['wish_adress']
                buyer.wish_square = self.cleaned_data['wish_square']
                buyer.budget = self.cleaned_data['budget']
                buyer.save()









class FlatForm(forms.Form):
    pasp_seria = forms.CharField(max_length=4)
    pasp_nomer = forms.CharField(max_length=6)

    coast = forms.IntegerField()
    descr = forms.CharField(widget=forms.Textarea)
    rooms = forms.IntegerField()
    adress = forms.CharField(max_length=150)
    square_f = forms.IntegerField()

    pasp_seria.widget.attrs.update({'class': 'from_input'})
    pasp_nomer.widget.attrs.update({'class': 'from_input'})

    coast.widget.attrs.update({'class': 'from_input'})
    descr.widget.attrs.update({'class': 'from_input form_textarea'})
    rooms.widget.attrs.update({'class': 'from_input'})
    adress.widget.attrs.update({'class': 'from_input'})
    square_f.widget.attrs.update({'class': 'from_input'})

    def clean_pasp_seria(self):
        self.new_pasp_seria = self.cleaned_data['pasp_seria']
        pseria_check = self.new_pasp_seria.lower()
        check_lettr(pseria_check, 'Серия паспорта')
        if len(self.new_pasp_seria) < 4:
            raise ValidationError('В серии паспорта слишком мало цифр')


        return self.new_pasp_seria

    def clean_pasp_nomer(self):
        print(self.new_pasp_seria)
        self.new_pasp_nomer = self.cleaned_data['pasp_nomer']
        # print(new_pasp_nomer)
        pnomer_check = self.new_pasp_nomer.lower()
        check_lettr(pnomer_check, 'Номер паспорта')
        if len(self.new_pasp_nomer) < 6:
            raise ValidationError('В номере паспорта слишком мало цифр')
        check_exist_kl(self.new_pasp_seria, self.new_pasp_nomer, Seller, 'id_seller', 'продавец')#проверяю клиента на несуществование в бд
        return self.new_pasp_nomer

    def clean_adress(self):
        new_adress = self.cleaned_data['adress']
        fl_list = Flat.objects.values('adress', 'id_seller')
        for fl in fl_list:
            if fl['adress'] == new_adress:
                id_sel_fl = fl['id_seller']
                if check_exist_kl(self.new_pasp_seria, self.new_pasp_nomer, Seller, 'id_seller', 'продавец') == 'клиент есть':
                    id_kl_sel = Klient.objects.filter(pasp_seria= self.new_pasp_seria).get(pasp_nomer= self.new_pasp_nomer).id_kl
                    sel_list = Seller.objects.values('id_seller', 'id_kl')
                    for sel in sel_list:
                        if sel['id_kl'] == id_kl_sel:
                            id_sel = sel['id_seller']

                    if fl['id_seller'] == id_sel:
                        # flat = Flat.objects.get(adress= new_adress)
                        # if flat.status == 'активен':
                        raise ValidationError('Эта квартира уже числится за этим человекам или числилась за ним')
                        # elif flat.status == 'продана':
                            # return new_adress

                    else:
                        return new_adress
        return new_adress




    def save(self) :    #сохраняю квартиру бд
        id_kl_sel = Klient.objects.filter(pasp_seria = self.cleaned_data['pasp_seria']).get(pasp_nomer = self.cleaned_data['pasp_nomer'])#SELECT id_kl FROM Klient WHERE pasp_seria = {self.cleaned_data['pasp_seria']} AND pasp_nomer = {self.cleaned_data['pasp_nomer']}
        id_sel = Seller.objects.get(id_kl=id_kl_sel)#SELECT id_seller FROM Seller WHERE id_kl = {id_kl_sel}

        seller = Seller.objects.get(id_kl=id_kl_sel)
        seller.status = 'активен'
        seller.save()

        new_flat = Flat.objects.create(                        #INSERT INTO Buyer (coast, descr, rooms, adress, square_f, id_seller) VALUES (
            coast = self.cleaned_data['coast'],                #    {self.cleaned_data['coast']},
            descr = self.cleaned_data['descr'],                #    {self.cleaned_data['descr']},
            rooms = self.cleaned_data['rooms'],                #    {self.cleaned_data['rooms']},
            adress = self.cleaned_data['adress'],              #    {self.cleaned_data['adress']},
            square_f = self.cleaned_data['square_f'],          #    {self.cleaned_data['square_f']},
            id_seller = id_sel,                                #    {id_sel},
            status = 'активен'                                 #    'активен'
        )                                                      #    );

        return new_flat








class ContractForm(forms.Form):
    b_pseria = forms.CharField(max_length=4)
    b_pnomer = forms.CharField(max_length=6)
    s_pseria = forms.CharField(max_length=4)
    s_pnomer = forms.CharField(max_length=6)
    adress = forms.CharField(max_length=150)
    time_to_sale = forms.DateField(widget=DateInput)
    coast = forms.IntegerField()
    proc_for_comp = forms.IntegerField()

    b_pseria.widget.attrs.update({'class': 'from_input'})
    b_pnomer.widget.attrs.update({'class': 'from_input'})
    s_pseria.widget.attrs.update({'class': 'from_input'})
    s_pnomer.widget.attrs.update({'class': 'from_input'})
    adress.widget.attrs.update({'class': 'from_input'})
    time_to_sale.widget.attrs.update({'class': 'from_input'})
    coast.widget.attrs.update({'class': 'from_input'})
    proc_for_comp.widget.attrs.update({'class': 'from_input'})



    def check_seria(self, obj):#проверка серии паспорта
        pseria_check = obj.lower()
        check_lettr(pseria_check, 'Серия паспорта')
        if len(obj) < 4:
            raise ValidationError('В серии паспорта слишком мало цифр')
        return obj

    def chech_pnomer(self, obj):#проверка номера паспорта
        pnomer_check = obj.lower()
        check_lettr(pnomer_check, 'Номер паспорта')
        if len(obj) < 6:
            raise ValidationError('В номере паспорта слишком мало цифр')
        return obj



    def clean_b_pseria(self):
        self.new_b_seria = self.cleaned_data['b_pseria']
        self.check_seria(self.new_b_seria)
        return self.new_b_seria

    def clean_b_pnomer(self):
        self.new_b_nomer = self.cleaned_data['b_pnomer']
        self.chech_pnomer(self.new_b_nomer)
        text_exist = check_exist_kl(self.new_b_seria, self.new_b_nomer, Buyer, 'id_buyer', 'покупатель')
        if text_exist == 'клиент есть':
            id_k = Klient.objects.filter(pasp_seria = self.new_b_seria).get(pasp_nomer = self.new_b_nomer)
            buyer = Buyer.objects.get(id_kl=id_k)
            if buyer.status == 'неактивен':
                raise ValidationError('Данный пользователь имеет статус "неактивен"')

        return self.new_b_nomer

    def clean_s_pseria(self):
        self.new_sel_seria = self.cleaned_data['s_pseria']
        self.check_seria(self.new_sel_seria)
        return self.new_sel_seria

    def clean_s_pnomer(self):
        self.new_sel_nomer = self.cleaned_data['s_pnomer']
        self.chech_pnomer(self.new_sel_nomer)
        text_exist = check_exist_kl(self.new_sel_seria, self.new_sel_nomer, Seller, 'id_seller', 'продавец')
        if self.new_b_nomer == self.new_sel_nomer and self.new_b_seria == self.new_sel_seria:
            raise ValidationError('Паспортные данные покупателя и продавца совпадают')

        if text_exist == 'клиент есть':
            id_k = Klient.objects.filter(pasp_seria = self.new_sel_seria).get(pasp_nomer = self.new_sel_nomer)
            seller = Seller.objects.get(id_kl=id_k)
            if seller.status == 'неактивен':
                raise ValidationError('Данный пользователь имеет статус "неактивен"')

        return self.new_sel_nomer

    def clean_time_to_sale(self):
        new_time = self.cleaned_data['time_to_sale']
        if datetime.date.today() > new_time:
            raise ValidationError('Срок сдачи не может быть меньше настоящей даты')
        return new_time

    def clean_adress(self):
        new_adress = self.cleaned_data['adress']

        new_adress = self.cleaned_data['adress']
        try:
            id_f = Flat.objects.filter(adress=new_adress).get(status='активен').id_fl#SELECT id_fl FROM Flat WHERE adress = {new_adress}
        except ObjectDoesNotExist:
            raise ValidationError('Квартиры с указанным адресом нет в базе данных')#проверка квартиры на отсутствие в бд

        fl_objs = Flat.objects.values('id_fl','id_seller')#получение значений полей для корректного сравнения (SELECT id_fl, id_seller FROM Flat)
        for obj in fl_objs:
            if obj['id_fl'] == id_f:
                id_sel_fl = obj['id_seller']#получение данных id_seller из таблица Flat

        if check_exist_kl(self.new_sel_seria, self.new_sel_nomer, Seller, 'id_seller', 'продавец') == 'клиент есть':

            id_kl = Klient.objects.filter(pasp_seria=self.new_sel_seria).get(pasp_nomer=self.new_sel_nomer).id_kl#SELECT id_kl FROM Klient WHERE pasp_seria = {self.new_sel_seria} AND pasp_nomer = {self.new_sel_nomer}
            seller = Seller.objects.values('id_seller', 'id_kl')#SELECT id_seller, id_kl FROM Seller
            for sel in seller:
                if sel['id_kl'] == id_kl:
                    id_sel_contr = sel['id_seller']#получение данных id_seller из таблица Klient для договора

            if id_sel_contr != id_sel_fl:
                raise ValidationError('Данная квартира не значится за продавцом')

        return new_adress



    def save(self):#сохраняю договор в бд
        print(self.cleaned_data['b_pseria'])
        print(self.cleaned_data['b_pnomer'])
        self.id_kl_b = Klient.objects.filter(pasp_seria = self.cleaned_data['b_pseria']).get(pasp_nomer = self.cleaned_data['b_pnomer'])#SELECT id_kl FROM Klient WHERE pasp_seria = {self.cleaned_data['b_pseria']} AND pasp_nomer = {self.cleaned_data['b_pnomer']}
        self.id_kl_sel = Klient.objects.filter(pasp_seria = self.cleaned_data['s_pseria']).get(pasp_nomer = self.cleaned_data['s_pnomer'])#SELECT id_kl FROM Klient WHERE pasp_seria = {self.cleaned_data['S_pseria']} AND pasp_nomer = {self.cleaned_data['s_pnomer']}
        self.id_b = Buyer.objects.get(id_kl=self.id_kl_b)#SELECT id_buyer FROM Buyer WHERE id_kl = {self.id_kl_b}
        self.id_sel = Seller.objects.get(id_kl=self.id_kl_sel)#SELECT id_seller FROM Seller WHERE id_kl = {self.id_kl_sel}

        self.id_f = Flat.objects.filter(adress=self.cleaned_data['adress']).get(status='активен')#SELECT id_fl FROM Flat WHERE adress = {self.cleaned_data['adress']}



        seller = Seller.objects.get(id_kl= self.id_kl_sel)
        am_flat = Flat.objects.filter(id_seller=seller).count()
        if am_flat == 1:
            seller.status = 'неактивен'
            seller.save()

        buyer = Buyer.objects.get(id_kl= self.id_kl_b)
        buyer.status = 'неактивен'
        buyer.save()

        flat_list = Flat.objects.values('adress', 'id_fl')
        for fl in flat_list:
            if fl['adress'] == self.cleaned_data['adress']:
                id_flat = fl['id_fl']

        flat = Flat.objects.get(id_fl= id_flat)
        flat.status = 'продана'
        flat.save()

        new_contract = Contract.objects.create(                  #INSERT INTO Buyer (id_buyer, id_seller, id_fl, time_to_sale, coast, proc_for_comp) VALUES (
            id_buyer = self.id_b,                                #    {self.id_b},
            id_seller = self.id_sel,                             #    {self.id_sel},
            id_fl = self.id_f,                                   #    {self.id_f},
            time_to_sale = self.cleaned_data['time_to_sale'],    #    {self.cleaned_data['time_to_sale']},
            coast = self.cleaned_data['coast'],                  #    {self.cleaned_data['coast']},
            proc_for_comp = self.cleaned_data['proc_for_comp'],  #    {self.cleaned_data['proc_for_comp'}
        )                                                        #    );
        return new_contract


    def create_contr(self):
        doc = DocxTemplate('main/doc_contract/contract_templeate.docx')
    
        contr_list = Contract.objects.all()#SELECT * FROM Contract
    
        for contr in contr_list:
            if contr.id_buyer == self.id_b and contr.id_seller == self.id_sel and contr.id_fl == self.id_f:
                id_c = contr.id_contract
                print(id_c)
                print(str(id_c))
    
        date = Contract.objects.get(id_contract=id_c).time_create
    
        buyer = Klient.objects.filter(pasp_seria = self.cleaned_data['b_pseria']).get(pasp_nomer = self.cleaned_data['b_pnomer']).fio#SELECT fio FROM Klient WHERE pasp_seria = {self.cleaned_data['b_pseria']} AND pasp_nomer = {self.cleaned_data['b_pnomer']}
        seller = Klient.objects.filter(pasp_seria = self.cleaned_data['s_pseria']).get(pasp_nomer = self.cleaned_data['s_pnomer']).fio#SELECT fio FROM Klient WHERE pasp_seria = {self.cleaned_data['S_pseria']} AND pasp_nomer = {self.cleaned_data['s_pnomer']}
    
        bd_buyer = Klient.objects.filter(pasp_seria = self.cleaned_data['b_pseria']).get(pasp_nomer = self.cleaned_data['b_pnomer']).bd#SELECT bd FROM Klient WHERE pasp_seria = {self.cleaned_data['b_pseria']} AND pasp_nomer = {self.cleaned_data['b_pnomer']}
        bd_seller = Klient.objects.filter(pasp_seria = self.cleaned_data['s_pseria']).get(pasp_nomer = self.cleaned_data['s_pnomer']).bd#SELECT bd FROM Klient WHERE pasp_seria = {self.cleaned_data['S_pseria']} AND pasp_nomer = {self.cleaned_data['s_pnomer']}
    
        b_pseria = self.cleaned_data['b_pseria']
        b_pnomer = self.cleaned_data['b_pnomer']
    
        s_pseria = self.cleaned_data['s_pseria']
        s_pnomer = self.cleaned_data['s_pnomer']
    
        adress = self.cleaned_data['adress']
        rooms = Flat.objects.filter(adress=self.cleaned_data['adress']).get(status='активен').rooms#SELECT rooms FROM Flat WHERE adress = {self.cleaned_data['adress']}
        square = Flat.objects.filter(adress=self.cleaned_data['adress']).get(status='активен').square_f#SELECT square_f FROM Flat WHERE adress = {self.cleaned_data['adress']}
    
        coast = self.cleaned_data['coast']
    
        time_to_sale = self.cleaned_data['time_to_sale']
    
        context = {'id_c': id_c, 'date': date, 'buyer': buyer, 'seller': seller,
                   'bd_buyer': bd_buyer, 'bd_seller': bd_seller,
                   'b_pseria': b_pseria, 'b_pnomer': b_pnomer, 's_pseria': s_pseria, 's_pnomer': s_pnomer,
                   'adress': adress, 'rooms': rooms, 'square': square, 'coast': coast, 'time_to_sale': time_to_sale}
    
        doc.render(context)
        doc.save('main/doc_contract/contract_{}.docx'.format(str(id_c)))
    
    
    
    
