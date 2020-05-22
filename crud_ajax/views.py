from .models import CrudUser
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import View #, ListView
from django.core import serializers


displayingItemsNumber = 3

# class CrudView(ListView):
#     model = CrudUser
#     template_name = 'crud_ajax/crud.html'
#     context_object_name = 'users'

class CrudView(View):
    def get(self, request):
        users = CrudUser.objects.all()[:displayingItemsNumber]
        # users = CrudUser.objects.all().order_by('id')[1:CrudUser.objects.all().count()-1]
        template = loader.get_template('crud_ajax/crud.html')
        context = {
            'users': users,
        }
        return HttpResponse(template.render(context, request))

class RetrieveCrudUser(View):
    def get(self, request):
        # Gets via ajax the requested indexes expressed in javascript
        fromIndex = int(request.GET.get('fromIndex', None))
        toIndex = int(request.GET.get('toIndex', None))

        # Checking pagination position
        first_page = False
        last_page = False
        if fromIndex > CrudUser.objects.all().count()-1: # Is it going to the First Page?
            first_page = True
            fromIndex = 0
            toIndex = displayingItemsNumber
        elif fromIndex < 0: # Is it going to the Last Page?
            last_page = True
            fromIndex = (CrudUser.objects.all().count() - displayingItemsNumber
                + CrudUser.objects.all().count()%displayingItemsNumber)
            toIndex = CrudUser.objects.all().count()

        if toIndex > CrudUser.objects.all().count(): # Is it the Last Page and not full?
            toIndex = CrudUser.objects.all().count()

        users = serializers.serialize("json",CrudUser.objects.all().order_by('id')[fromIndex:toIndex])
        data = {
            'users': users,
            'fromIndex': fromIndex,
            'toIndex': toIndex,
            'first_page' : first_page,
            'last_page' : last_page
        }
        return JsonResponse(data)

class CreateCrudUser(View):
    def  get(self, request):
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = CrudUser.objects.create(
            name = name1,
            address = address1,
            age = age1
        )

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)

class UpdateCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = CrudUser.objects.get(id=id1)
        obj.name = name1
        obj.address = address1
        obj.age = age1
        obj.save()

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)

class DeleteCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        CrudUser.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
