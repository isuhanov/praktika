from django import forms
from .models import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from docxtpl import DocxTemplate
import datetime

set_number = {'1','2','3','4','5','6','7','8','9','0'}
set_letters_cir = {' ', 'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я' }
set_letters_lat = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

class DateInput(forms.DateInput):
    input_type = 'date'

def check_fio(fio):
    fio.lower
    for i in fio.lower():
        if not(i in set_letters_cir or i in set_letters_lat):
            raise ValidationError('ФИО содержит недопустимые символы')
    if len(fio) > 100:
        raise ValidationError('Кол-во символов превышает предел')

def check_bd(bd):
    if bd > datetime.date.today():
        raise ValidationError('Дата рождения не должна превышать настоящую')

def check_phone(phone):
    for i in phone:
        if not(i in set_number):
            raise ValidationError('Номер содержит недопустимые символы')
    if len(phone) > 11:
        raise ValidationError('В номере слишком много символов')
    if len(phone) < 11:
        raise ValidationError('В номере недостаточно символов')

def check_mail(mail):
    if len(mail) > 100:
        raise ValidationError('В адресе почтового адреса слишком много сомволов')

def check_pseria(pasp_seria):
    for i in pasp_seria:
        if not(i in set_number):
            raise ValidationError('Серия паспорта содержит недопустимые символы')
    if len(pasp_seria) > 4:
        raise ValidationError('В серии паспорта слишком много символов')
    if len(pasp_seria) < 4:
        raise ValidationError('В серии паспорта недостаточно символов')

def check_pnomer(pasp_nomer):
    for i in pasp_nomer:
        if not(i in set_number):
            raise ValidationError('Номер паспорта содержит недопустимые символы')
    if len(pasp_nomer) > 6:
        raise ValidationError('В номере паспорта слишком много символов')
    if len(pasp_nomer) < 6:
        raise ValidationError('В номере паспорта недостаточно символов')

def check_adress(adress):
    if len(adress) > 150:
        raise ValidationError('В адресе слишком много символов')
    if len(adress) < 5:
        raise ValidationError('В адресе недостаточно символов')

def check_coast(coast):
    coast = str(coast)
    if coast[0] == '-':
        raise ValidationError('Цена не может быть отрицательной')
    for i in coast:
        if not(i in set_number):
            raise ValidationError('Некорректные символы в цене')
    if len(coast) > 20:
        raise ValidationError('Слишком большая цена')
    if float(coast) == 0:
        raise ValidationError('Не может быть равным 0')

def check_rooms(rooms):
    rooms = str(rooms)
    if rooms[0] == '-':
        raise ValidationError('Кол-во комнат не может быть отрицательным')
    for i in rooms:
        if not(i in set_number):
            raise ValidationError('Некорректные символы в кол-ве комнат')
    if len(rooms) > 10:
        raise ValidationError('Слишком большое кол-во комнат')

def chech_square(square):
    square = str(square)
    if square[0] == '-':
        raise ValidationError('Площадь не может быть отрицательной')
    for i in square:
        if not(i in set_number):
            raise ValidationError('Некорректные символы в площади')
    if len(square) > 5:
        raise ValidationError('Слишком большая площадь')


def check_exist_kl(pseria, pnomer, model):
    try:
        kl = Klient.objects.get(pasp_seria=pseria, pasp_nomer=pnomer)#SELECT * FORM Klient WHERE pasp_seria={pseria}, pasp_nomer={pnomer}
        obj = model.objects.get(id_kl = kl)#SELECT * FORM {model} WHERE id_kl = {kl}
        raise ValidationError('Такой клиент существует')
        return 'клиент существует'
    except ObjectDoesNotExist:
        return 'клиент не существует'

def check_doesnotexist_kl(pseria, pnomer, model):
    try:
        kl = Klient.objects.get(pasp_seria=pseria, pasp_nomer=pnomer)#SELECT * FORM Klient WHERE pasp_seria={pseria}, pasp_nomer={pnomer}
        sel_status = model.objects.get(id_kl=kl).status#SELECT status FORM {model} WHERE id_kl = {kl}
        if sel_status == 'неактивен':
            return 'клиент неактивен'
        elif sel_status == 'активен':
            return 'клиент активен'
    except ObjectDoesNotExist:
        raise ValidationError('Такой клиент не существует')
        return 'клиент не существует'

def check_exist_fl(new_adress):
    try:
        fl = Flat.objects.get(adress=new_adress)#SELECT * FORM Flat WHERE adress = {new_adress}
        if fl.status == 'активен':
            raise ValidationError('Такая квартира уже существует')
            return 'активен'
        elif fl.status == 'продана':
            return 'продана'
    except ObjectDoesNotExist:
        return 'не существует'

def checheck_doesnotexist_fl(new_adress):
    try:
        fl = Flat.objects.get(adress=new_adress)#SELECT * FORM Flat WHERE adress = {new_adress}
        if fl.status == 'активен':
            return 'активен'
        elif fl.status == 'продана':
            raise ValidationError('Такая квартира уже продана')
            return 'продана'
    except ObjectDoesNotExist:
        raise ValidationError('Такая квартира не существует')    
        return 'не существует'



def create_kl(text, n_fio,n_bd, n_phone, n_mail, n_pseria, n_pnomer):
    if text == 'клиент не существует':
        new_kl = Klient.objects.create( #INSERT INTO Klient (fio, bd, phone, mail, pasp_seria, pasp_nomer) VALUES (
            fio = n_fio,                #   {n_fio},
            bd = n_bd,                  #   {n_bd},
            phone = n_phone,            #   {n_phone},
            mail = n_mail,              #   {n_mail},
            pasp_seria = n_pseria,      #   {n_pseria},
            pasp_nomer = n_pnomer       #   {n_pnomer},
        )                               #    );
        return new_kl

def create_flat(n_coast, n_descr, n_rooms, n_adress, n_squae, n_id_seller):
    new_flat = Flat.objects.create(                        #INSERT INTO Seller (coast, descr, rooms, adress, square_f, id_seller, status) VALUES (
        coast = n_coast,                                   #    {self.cleaned_data['coast']},
        descr = n_descr,                                   #    {self.cleaned_data['descr']},
        rooms = n_rooms,                                   #    {self.cleaned_data['rooms']},
        adress = n_adress,                                 #    {self.cleaned_data['adress']},
        square_f = n_squae,                                #    {self.cleaned_data['square_f']},
        id_seller = n_id_seller,                           #    {id_sel},
        status = 'активен'                                 #    'активен'
    )                                                      #    );
    return new_flat

def change_status_flat(new_adress, n_coast, n_descr, n_rooms, n_squae, n_id_seller):
    fl = Flat.objects.get(adress = new_adress)          #UPDATE Flat SET coast = n_coast, descr = n_descr, rooms = n_rooms, square_f = n_squae, id_seller = (SELECT * FORM Seller WHERE id_kl = {n_id_seller}), status = 'активен'
    fl.coast = n_coast                                  #WHERE adress = {new_adress}
    fl.descr = n_descr
    fl.rooms = n_rooms
    fl.square_f = n_squae
    fl.id_seller = Seller.objects.get(id_kl=n_id_seller)
    fl.status = 'активен'
    fl.save()




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
        check_fio(new_fio)
        return new_fio

    def clean_bd(self):
        new_bd = self.cleaned_data['bd']
        check_bd(new_bd)
        return new_bd

    def clean_phone(self):
        new_phone = self.cleaned_data['phone']
        check_phone(new_phone)
        return new_phone

    def clean_mail(self):
        new_mail = self.cleaned_data['mail']
        check_mail(new_mail)
        return new_mail

    def clean_pasp_seria(self):
        new_pseria = self.cleaned_data['pasp_seria']
        check_pseria(new_pseria)
        return new_pseria

    def clean_pasp_nomer(self):
        new_pnomer = self.cleaned_data['pasp_nomer']
        check_pnomer(new_pnomer)
        self.exist_klient_text = check_exist_kl(self.cleaned_data['pasp_seria'], new_pnomer, Seller)#проверка на существование клиента
        return new_pnomer

    def clean_coast(self):
        new_coast = self.cleaned_data['coast']
        check_coast(new_coast)
        return new_coast

    def clean_rooms(self):
        new_rooms = self.cleaned_data['rooms']
        check_rooms(new_rooms)
        return new_rooms

    def clean_adress(self):
        new_adress = self.cleaned_data['adress']
        check_adress(new_adress)
        self.text_flat_exist = check_exist_fl(new_adress)
        return new_adress

    def clean_square_f(self):
        new_square_f = self.cleaned_data['square_f']
        chech_square(new_square_f)
        return new_square_f


    def save_k(self):#сохраняю клиента в бд
        create_kl(self.exist_klient_text, self.cleaned_data['fio'], self.cleaned_data['bd'], self.cleaned_data['phone'], self.cleaned_data['mail'], self.cleaned_data['pasp_seria'], self.cleaned_data['pasp_nomer'])

    def save_sel(self):#сохраняю продавца в бд
        self.id_kl_sel = Klient.objects.get(pasp_seria = self.cleaned_data['pasp_seria'], pasp_nomer = self.cleaned_data['pasp_nomer'])#SELECT * FROM Klient WHERE pasp_seria = {self.cleaned_data['pasp_seria']} AND pasp_nomer = {self.cleaned_data['pasp_nomer']}
        new_seller = Seller.objects.create(          #INSERT INTO Seller (id_kl, status) VALUES (
            id_kl = self.id_kl_sel,                  #    {self.id_kl_sel},
            status = 'активен'                       #    'активен'
        )                                            #    );
        return new_seller

    def save_fl(self):#сохраняю квартиру в бд
        id_sel = Seller.objects.get(id_kl=self.id_kl_sel)#SELECT * FROM Seller WHERE id_kl = {self.id_kl_sel}
        if self.text_flat_exist == 'не существует':
            create_flat(self.cleaned_data['coast'], self.cleaned_data['descr'], self.cleaned_data['rooms'], self.cleaned_data['adress'], self.cleaned_data['square_f'], id_sel)
        elif self.text_flat_exist == 'продана':
            change_status_flat(self.cleaned_data['adress'], self.cleaned_data['coast'], elf.cleaned_data['descr'], self.cleaned_data['rooms'], self.cleaned_data['square_f'], id_sel)



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
        check_fio(new_fio)
        return new_fio

    def clean_bd(self):
        new_bd = self.cleaned_data['bd']
        check_bd(new_bd)
        return new_bd

    def clean_phone(self):
        new_phone = self.cleaned_data['phone']
        check_phone(new_phone)
        return new_phone

    def clean_mail(self):
        new_mail = self.cleaned_data['mail']
        check_mail(new_mail)
        return new_mail

    def clean_pasp_seria(self):
        new_pseria = self.cleaned_data['pasp_seria']
        check_pseria(new_pseria)
        return new_pseria

    def clean_pasp_nomer(self):
        new_pnomer = self.cleaned_data['pasp_nomer']
        check_pnomer(new_pnomer)
        self.exist_klient_text = check_exist_kl(self.cleaned_data['pasp_seria'], new_pnomer, Buyer)#проверка на существование клиента
        try:
            kl = Klient.objects.get(pasp_seria= self.cleaned_data['pasp_seria'], pasp_nomer=new_pnomer)#SELECT * FROM Klient WHERE pasp_seria= {self.cleaned_data['pasp_seria']}, pasp_nomer={new_pnomer}
            try:
                self.buyer = Buyer.objects.get(id_kl=kl)#SELECT * FROM Buyer WHERE id_kl={kl}
                if self.buyer.status == 'неактивен':
                    self.text = 'существует неактивен'
                elif self.buyer.status == 'активен':
                    self.text = 'существует активен' 
                    raise ValidationError('Такой покупатель уже существует')  
            except ObjectDoesNotExist:
                self.text = 'нет такого покупателя'                 
        except ObjectDoesNotExist:
            self.text = 'клиент не существует'
        return new_pnomer       

    def clean_wish_room(self):
        new_wish_room = self.cleaned_data['wish_room']
        check_rooms(new_wish_room)
        return new_wish_room

    def clean_wish_adress(self):
        new_wish_adress = self.cleaned_data['wish_adress']
        check_adress(new_wish_adress)
        return new_wish_adress

    def clean_wish_square(self):
        new_wish_square = self.cleaned_data['wish_square']
        chech_square(new_wish_square)
        return new_wish_square

    def clean_budget(self):
        new_budget = self.cleaned_data['budget']
        check_coast(new_budget)
        return new_budget

    def save_k(self):#сохраняю клиента в бд
        if self.text == 'клиент не существует':
            create_kl(self.text, self.cleaned_data['fio'], self.cleaned_data['bd'], self.cleaned_data['phone'], self.cleaned_data['mail'], self.cleaned_data['pasp_seria'], self.cleaned_data['pasp_nomer'])

    def save_b(self):#сохраняю поупателя в бд
        kl = Klient.objects.get(pasp_seria=self.cleaned_data['pasp_seria'], pasp_nomer= self.cleaned_data['pasp_nomer'])#SELECT * FROM Klient WHERE pasp_seria={self.cleaned_data['pasp_seria']}, pasp_nomer= {self.cleaned_data['pasp_nomer']}
        if self.text == 'клиент не существует' or self.text == 'нет такого покупателя':
            new_buyer = Buyer.objects.create(                       #INSERT INTO Buyer (id_kl, wish_room, wish_adress, wish_square, budget, status) VALUES (
                id_kl = kl,                                         #   {id_kl_b},
                wish_room = self.cleaned_data['wish_room'],         #   {self.cleaned_data['wish_room']},
                wish_adress = self.cleaned_data['wish_adress'],     #   {self.cleaned_data['wish_adress']},
                wish_square = self.cleaned_data['wish_square'],     #   {self.cleaned_data['wish_square']},
                budget = self.cleaned_data['budget'],               #   {self.cleaned_data['budget']},
                status = 'активен'                                  #   'активен'
            )                                                       #    );
            return new_buyer
        elif self.text == 'существует неактивен':
            self.buyer.status = 'активен'                              #UPDATE Buyer SET wish_room = {self.cleaned_data['wish_room']}, wish_adress = {self.cleaned_data['wish_adress']}, wish_square = {self.cleaned_data['wish_square']}, budget = {self.cleaned_data['budget']}
            self.buyer.wish_room = self.cleaned_data['wish_room']      #WHERE id_kl={kl}
            self.buyer.wish_adress = self.cleaned_data['wish_adress']
            self.buyer.wish_square = self.cleaned_data['wish_square']
            self.buyer.budget = self.cleaned_data['budget']
            self.buyer.save()
            
            
        


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
        new_pasp_seria = self.cleaned_data['pasp_seria']
        check_pseria(new_pasp_seria)
        return new_pasp_seria

    def clean_pasp_nomer(self):
        new_pasp_nomer = self.cleaned_data['pasp_nomer']
        check_pnomer(new_pasp_nomer)
        self.text_klient_doesnotexist = check_doesnotexist_kl(self.cleaned_data['pasp_seria'], new_pasp_nomer, Seller)
        return new_pasp_nomer

    def clean_coast(self):
        new_coast = self.cleaned_data['coast']
        check_coast(new_coast)
        return new_coast

    def clean_rooms(self):
        new_rooms = self.cleaned_data['rooms']
        check_rooms(new_rooms)
        return new_rooms

    def clean_adress(self):
        new_adress = self.cleaned_data['adress']
        check_adress(new_adress)
        self.text_flat_doesnotexist = check_exist_fl(new_adress)
        return new_adress

    def clean_square_f(self):
        new_square_f = self.cleaned_data['square_f']
        chech_square(new_square_f)
        return new_square_f

    def save(self) :    #сохраняю квартиру бд
        id_sel_kl = Klient.objects.get(pasp_seria=self.cleaned_data['pasp_seria'], pasp_nomer=self.cleaned_data['pasp_nomer'])#SELECT * FROM Klient WHERE pasp_seria={self.cleaned_data['pasp_seria']}, pasp_nomer= {self.cleaned_data['pasp_nomer']}
        sel = Seller.objects.get(id_kl=id_sel_kl)#SELECT * FROM Seller WHERE id_kl={id_sel_kl}
        if self.text_klient_doesnotexist == 'клиент неактивен':
            sel.status = 'активен'   #UPDATE Seller SET status = 'активен'
            sel.save()               #WHERE id_kl={id_sel_kl}
        if self.text_flat_doesnotexist == 'продана':
            change_status_flat(self.cleaned_data['adress'], self.cleaned_data['coast'], elf.cleaned_data['descr'], self.cleaned_data['rooms'], self.cleaned_data['square_f'], sel)
        elif self.text_flat_doesnotexist == 'не существует':
            create_flat(self.cleaned_data['coast'], self.cleaned_data['descr'], self.cleaned_data['rooms'], self.cleaned_data['adress'], self.cleaned_data['square_f'], sel)



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

    def clean_b_pseria(self):#проверка серии паспорта
        new_pseria_b = self.cleaned_data['b_pseria']
        check_pseria(new_pseria_b)
        return new_pseria_b

    def clean_b_pnomer(self):#проверка номера паспорта
        print(self.cleaned_data)
        new_pnomer_b = self.cleaned_data['b_pnomer']
        check_pnomer(new_pnomer_b)
        text_exist_buyer = check_doesnotexist_kl(self.cleaned_data['b_pseria'], new_pnomer_b, Buyer)
        if text_exist_buyer == 'клиент неактивен':
            raise ValidationError('Клиент имеет статус неактивен')
        return new_pnomer_b

    def clean_s_pseria(self):
        new_pseria_s = self.cleaned_data['s_pseria']
        check_pseria(new_pseria_s)
        return new_pseria_s

    def clean_s_pnomer(self):
        new_pnomer_s = self.cleaned_data['s_pnomer']
        check_pnomer(new_pnomer_s)
        if self.cleaned_data['b_pseria'] == self.cleaned_data['s_pseria'] and self.cleaned_data['b_pnomer'] == new_pnomer_s:
            raise ValidationError('Паспорта клиентов совпадают')
        text_exist_sel = check_doesnotexist_kl(self.cleaned_data['s_pseria'], new_pnomer_s, Seller)
        if text_exist_sel == 'клиент неактивен':
            raise ValidationError('Клиент имеет статус неактивен')
        return new_pnomer_s

    def clean_time_to_sale(self):
        new_time = self.cleaned_data['time_to_sale']
        if new_time < datetime.date.today():
            raise ValidationError('Срок сдачи не может быть меньше сегодняшнего числа')
        return new_time

    def clean_adress(self):
        new_adress = self.cleaned_data['adress']
        check_adress(new_adress)
        text_exist_flat = checheck_doesnotexist_fl(new_adress)
        return new_adress

    def clean_coast(self):
        new_coast = self.cleaned_data['coast']
        check_coast(new_coast)
        return new_coast

    def clean_proc_for_comp(self):
        new_proc_for_comp = self.cleaned_data['proc_for_comp']
        if len(str(new_proc_for_comp)) > 2:
            raise ValidationError('Вы ввели слишком большой процент')
        if str(new_proc_for_comp)[0] == '-':
            raise ValidationError('Процент не может быть отрицательным') 
        for i in str(new_proc_for_comp):
            if not(i in set_number):
                raise ValidationError('В поле с процентом недопустимые символы')
        return new_proc_for_comp

    def save(self):#сохраняю договор в бд
        self.id_kl_b = Klient.objects.get(pasp_seria = self.cleaned_data['b_pseria'], pasp_nomer = self.cleaned_data['b_pnomer'])#SELECT * FROM Klient WHERE pasp_seria = {self.cleaned_data['b_pseria']} AND pasp_nomer = {self.cleaned_data['b_pnomer']}
        self.id_kl_sel = Klient.objects.get(pasp_seria = self.cleaned_data['s_pseria'], pasp_nomer = self.cleaned_data['s_pnomer'])#SELECT * FROM Klient WHERE pasp_seria = {self.cleaned_data['s_pseria']} AND pasp_nomer = {self.cleaned_data['s_pnomer']}
        self.id_b = Buyer.objects.get(id_kl=self.id_kl_b)#SELECT * FROM Buyer WHERE id_kl = {self.id_kl_b}
        self.id_sel = Seller.objects.get(id_kl=self.id_kl_sel)#SELECT * FROM Seller WHERE id_kl = {self.id_kl_sel}
        self.id_f = Flat.objects.get(adress=self.cleaned_data['adress'])#SELECT * FROM Flat WHERE adress = {self.cleaned_data['adress']}


        new_contract = Contract.objects.create(                  #INSERT INTO Contract (id_buyer, id_seller, id_fl, time_to_sale, coast, proc_for_comp) VALUES (
            id_buyer = self.id_b,                                #    {self.id_b},
            id_seller = self.id_sel,                             #    {self.id_sel},
            id_fl = self.id_f,                                   #    {self.id_f},
            time_to_sale = self.cleaned_data['time_to_sale'],    #    {self.cleaned_data['time_to_sale']},
            coast = self.cleaned_data['coast'],                  #    {self.cleaned_data['coast']},
            proc_for_comp = self.cleaned_data['proc_for_comp']   #    {self.cleaned_data['proc_for_comp'}
        )                                                        #    );
        am_flat = Flat.objects.filter(id_seller= self.id_sel).count() #SELECT COUNT(id_fl) FROM Flat WHERE id_seller = {seller}
        if am_flat == 1:
            self.id_sel.status = 'неактивен'    #UPDATE Seller SET status = 'неактивен'
            self.id_sel.save()                  #WHERE id_kl = {self.id_kl_sel}

        self.id_b.status = 'неактивен'          #UPDATE Buyer SET status = 'неактивен'
        self.id_b.save()                        #WHERE id_kl = {self.id_kl_b}

        self.id_f.status = 'продана'            #UPDATE Flat SET status = 'продана'
        self.id_f.save()                        #WHERE adress = {self.cleaned_data['adress']}
        return new_contract

    def create_contr(self):
        doc = DocxTemplate('main/doc_contract/contract_templeate.docx')

        id_c = Contract.objects.get(id_buyer=self.id_b, id_seller=self.id_sel, id_fl=self.id_f).id_contract#SELECT id_contract FROM Contract WHERE id_buyer={self.id_b} AND id_seller={self.id_sel} AND id_fl={self.id_f}

        date = Contract.objects.get(id_contract=id_c).time_create#SELECT time_create FROM Contract WHERE id_contract={id_c}
    
        buyer = Klient.objects.get(pasp_seria = self.cleaned_data['b_pseria'], pasp_nomer = self.cleaned_data['b_pnomer'])#SELECT * FROM Klient WHERE pasp_seria = {self.cleaned_data['b_pseria']} AND pasp_nomer = {self.cleaned_data['b_pnomer']}
        seller = Klient.objects.get(pasp_seria = self.cleaned_data['s_pseria'], pasp_nomer = self.cleaned_data['s_pnomer'])#SELECT * FROM Klient WHERE pasp_seria = {self.cleaned_data['s_pseria']} AND pasp_nomer = {self.cleaned_data['s_pnomer']}
    
        buyer_fio = buyer.fio
        seller_fio = seller.fio
        bd_buyer = buyer.bd
        bd_seller = seller.bd
    
        b_pseria = self.cleaned_data['b_pseria']
        b_pnomer = self.cleaned_data['b_pnomer']
    
        s_pseria = self.cleaned_data['s_pseria']
        s_pnomer = self.cleaned_data['s_pnomer']
    
        adress = self.cleaned_data['adress']
        rooms = Flat.objects.get(adress=self.cleaned_data['adress']).rooms#SELECT rooms FROM Flat WHERE adress = {self.cleaned_data['adress']}
        square = Flat.objects.get(adress=self.cleaned_data['adress']).square_f#SELECT square_f FROM Flat WHERE adress = {self.cleaned_data['adress']}
    
        coast = self.cleaned_data['coast']
    
        time_to_sale = self.cleaned_data['time_to_sale']
    
        context = {'id_c': id_c, 'date': date, 'buyer': buyer_fio, 'seller': seller_fio,
                   'bd_buyer': bd_buyer, 'bd_seller': bd_seller,
                   'b_pseria': b_pseria, 'b_pnomer': b_pnomer, 's_pseria': s_pseria, 's_pnomer': s_pnomer,
                   'adress': adress, 'rooms': rooms, 'square': square, 'coast': coast, 'time_to_sale': time_to_sale}
    
        doc.render(context)
        doc.save('main/doc_contract/contract_{}.docx'.format(str(id_c)))
