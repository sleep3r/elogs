import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.template import loader


# Create your views here.
from leaching.express_anal_app.tables import add_model_to_dict
from leaching.repair_app.models import Repairs, Equipment
from utils.deep_dict import deep_dict
from utils.webutils import parse, process_json_view



@login_required
def index(request):

    context = {
        'repair': ''
    }

    template = loader.get_template('repair/index.html')
    return HttpResponse(template.render(context, request))

@process_json_view(auth_required=False)
def get_equipment(request):

    items = Equipment.objects.all().order_by('name')

    records = []
    for num, item in enumerate(items):
        row = {'num': num, 'name': item.name, 'id': item.id}
        records.append(row)

    return {
        'component': 'equipment',
        'items': records,
        'count': len(records)
    }


@process_json_view(auth_required=False)
def get_items(request):
    equipment_id = int(request.GET['equipment'])

    if equipment_id > 0:
        items = Repairs.objects.filter(equipment__id=equipment_id).order_by('date')
    else:
        items = []

    records = []
    for num, item in enumerate(items):
        row = {'num': num, 'name': item.name, 'id': item.id, 'comment': item.comment, 'date': item.date.strftime("%Y-%m-%dT%H:%M")}
        records.append(row)

    return {
        'result': 'ok',
        'equipment_id': equipment_id,
        'items': records,
        'count': len(records)
    }


@process_json_view(auth_required=False)
def add_record(request):

    data = json.loads(request.POST['items'])
    fields = ['date', 'name', 'comment']

    equipment_id = request.POST['equipment_id']
    equipment = Equipment.objects.get(id=equipment_id)

    model = Repairs()
    for field in fields:
        if field in data:
            if field == 'date':
                model.date = parse(data['date'])
            else:
                setattr(model, field, data[field])

    model.equipment = equipment
    result = model.save()

    return {
        'result': result,
        'equipment_id': equipment_id
    }


@process_json_view(auth_required=False)
def save_record(request):
    items = json.loads(request.POST['items'])
    data = items[0]
    print(data)
    fields = ['date', 'name', 'comment']

    if 'id' in data:
        record_id = data['id']
        model = Repairs.objects.get(id=record_id)
    else:
        model = Repairs()

    for field in fields:
        if field in data:
            if field == 'date':
                date = parse(data['date'])
                if date is None:
                    date = datetime.datetime.now()
                model.date = date

                print(model.date)
            else:
                setattr(model, field, data[field])

    result = model.save()

    return {
        'result': result,
    }

@process_json_view(auth_required=False)
def remove_record(request):
    print(request.GET['id'])
    result = 'none'
    if 'id' in request.GET:
        record_id = request.GET['id']
        model = Repairs.objects.get(id=record_id)
        model.delete()
        result = 'ok'
    else:
        result = 'none'

    return {
        'result': result,
    }


@login_required
def edit(request):
    context = {}


    template = loader.get_template('repair/edit.html')
    return HttpResponse(template.render(context, request))
