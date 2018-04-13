import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.template import loader


# Create your views here.
from leaching.express_anal_app.tables import add_model_to_dict
from leaching.repair_app.models import Repairs
from utils.deep_dict import deep_dict
from utils.webutils import parse, process_json_view


def get_repair_table():

    res = deep_dict()
    for d in Repairs.objects.all:
        add_model_to_dict(d, res[str(d.time)])

    return res.clear_empty().get_dict()


@login_required
def index(request):
    # items = get_repair_table()

    context = {
        'repair': ''
    }

    template = loader.get_template('repair/index.html')
    return HttpResponse(template.render(context, request))


@process_json_view(auth_required=False)
def get_items(request):

    items = Repairs.objects.all().order_by('date')

    records = []
    for num, item in enumerate(items):
        row = {'num': num, 'name': item.name, 'id': item.id, 'comment': item.comment, 'date': item.date.strftime("%Y-%m-%dT%H:%M")}
        records.append(row)

    return {
        'result': 'ok',
        'items': records,
        'count': len(records)
    }


@process_json_view(auth_required=False)
def add_record(request):

    print(request.POST)
    data = json.loads(request.POST['items'])
    fields = ['date', 'name', 'comment']


    model = Repairs()
    for field in fields:
        if field in data:
            if field == 'date':
                model.date = parse(data['date'])
            else:
                setattr(model, field, data[field])

    result = model.save()

    return {
        'result': result,
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



@login_required
def edit(request):
    context = {}


    template = loader.get_template('repair/edit.html')
    return HttpResponse(template.render(context, request))
