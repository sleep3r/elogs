import json

from django.db.models import Q

from main_app.processors import *
from main_app.processors import get_docx_path, get_pdf_path
from room_app.models import Room
from utils.errors import SemanticError
from utils.webutils import processView


def conf_info_object(c):
    def permitted(conf, can_empty=False):
        return bool(c.state != 'future' and (can_empty or conf.track_set.filter(is_active=True)))

    res = {
        'name': c.name,
        'state': c.state,
        'language': c.languages,
        'type': c.type,
        'recognition': c.recognition,
        'room': c.room.id,
        'date': str(c.start_time),
        'conference': c.id,
        'canDownloadPdf': int(permitted(c)),
        'canDownloadDoc': int(permitted(c)),
        'canMailPdf': int(permitted(c)),
        'canMailDoc': int(permitted(c)),
        'canUploadDoc': int(permitted(c)),
        'canListen': int(permitted(c)),
        'canEditTracks': int(permitted(c, True)),
        'pdfSaved': int(os.path.isfile(get_pdf_path(c))),
        'docSaved': int(os.path.isfile(get_docx_path(c))),
        'recompile': 1 if c.talkers_changed.exists() else 0,
        'canForget': 0,
        'canRecognizeAll': 1,
        'canLink': 1,
        'hasLink': 0,
        'isExported': 0,
    }

    return res


def update_queues(conf_id, peacedun, res):
    for user_que in TrackQueue.objects.filter(conference_id=conf_id, is_active=True):
        if time.time() - user_que.last_refresh > QUEUE_LIFETIME:
            user_que.is_active = False
        res_dict = cast_to_deep(json.loads(user_que.queue))
        add_deep(res, res_dict)
        user_que.queue = json.dumps(res_dict)
        user_que.save()

    if peacedun != -1:
        my_que = TrackQueue.objects.get(pk=peacedun)
        res = my_que.queue
        my_que.queue = '{}'
        my_que.last_refresh = int(time.time())
        my_que.save()

        if my_que.is_active:
            return json.loads(res)
        else:
            return {'error': 'refresh'}


@processView(auth_required=True)
def get_conference(request):
    conf_id = request.GET['conference']
    c = Conference.objects.get(pk=conf_id)
    if not has_access(request.user, c):
        raise SemanticError(message='У вас нет прав на доступ к этой конференции.')
    res = deep_dict()
    tr_set = c.track_set.filter(is_active=True)
    res["files"] = deep_dict()
    res["talkers"] = deep_dict()
    for t in tr_set:
        res["files"][t.id] = create_file_struct(t.path, t.talker.id, t.offset, t.duration, t.text)
    for t in c.talker_set.all():
        res['talkers'][t.id] = {'name': t.name, 'title': t.title, 'email': t.email}

    q = TrackQueue()
    q.conference_id = conf_id
    q.save()
    q.queue = '{}'
    q.save()

    res['firstMoment'], res['lastMoment'] = get_tracks_boundaries(c.track_set.all())
    res['info'] = conf_info_object(c)
    res['peacedun'] = q.id

    return res


@processView(auth_required=True)
def edit_file(request):
    conf_id = request.POST['conference']
    file_id = request.POST['file']
    peacedun = request.POST['peacedun']
    text = request.POST['text']

    t = Track.objects.get(pk=file_id)
    t.text = text
    t.save()

    res = deep_dict()
    res['files'][str(file_id)] = id2file_struct(file_id)
    res['info']['conference'] = conf_id
    return update_queues(conf_id, peacedun, res)


@processView(auth_required=True)
def edit_talker(request):
    conf_id = request.POST['conference']
    talker_id = request.POST['talker']
    name = request.POST['name']
    title = request.POST['title']
    email = request.POST['email']
    peacedun = request.POST['peacedun']

    t = Talker.objects.get(pk=talker_id)
    t.name = name
    t.title = title
    t.email = email
    t.save()

    res = deep_dict()
    res['talkers'][talker_id]['name'] = name
    res['talkers'][talker_id]['title'] = title
    res['talkers'][talker_id]['email'] = email
    res['info']['conference'] = conf_id
    return update_queues(conf_id, peacedun, res)


@processView(auth_required=True)
def add_conference(request):
    args = request.POST
    u = request.user
    if args['type'] == 'closed' and args['recognition'] == 'out':
        raise SemanticError(message='В закрытых конференциях не разрешается использовать автоматическое распознавание.')

    if not check_fields(args):
        raise SemanticError(code='fatal')

    if args['state'] == 'active' and Conference.objects.filter(room_id=args['room'], state='active'):
        raise SemanticError(message='В этой комнате сейчас уже проходит конференция.')

    c = Conference()
    c.name = args['name']
    c.state = args['state']
    c.languages = args['language']
    c.type = args['type']
    c.recognition = args['recognition']
    c.room = Room.objects.get(pk=args['room'])
    c.start_time = str(args['date'])
    c.department = u.employee.department
    c.save()

    return conf_info_object(c)


@processView(auth_required=True)
def edit_conference(request):
    args = request.POST
    conf_id = args["conference"]
    u = request.user
    c = Conference.objects.get(pk=conf_id)

    if not has_access(u, c):
        raise SemanticError(message='У вас нет прав на изменение этой конференции.')
    if c.type == 'closed' and args["type"] == 'open' and not u.has_perm('main_app.can_open'):
        raise SemanticError(message='Вы не можете сделать закрытую конференцию открытой.')
    if args['type'] == 'closed' and args['recognition'] == 'out':
        raise SemanticError(message='В закрытых конференциях не разрешается использовать автоматическое распознавание.')
    if not check_fields(args):
        raise SemanticError(code='fatal')
    if args['state'] == 'active' and Conference.objects.filter(room_id=args['room'], state='active').filter(~Q(id=conf_id)):
        raise SemanticError(message='В этой комнате сейчас уже проходит конференция.')

    c.name = args["name"]
    c.state = args["state"]
    c.languages = args["language"]
    c.type = args["type"]
    c.recognition = args["recognition"]
    c.room = Room.objects.get(pk=args["room"])
    c.start_time = args["date"]

    c.save()

    return conf_info_object(c)


@processView(auth_required=True)
def conference_info(request):
    conf_id = request.GET["conference"]
    c = Conference.objects.get(pk=conf_id)
    u = request.user

    if not has_access(u, c):
        raise SemanticError(message='У вас нет прав на доступ к этой конференции.')

    res = conf_info_object(c)
    return res


@processView(auth_required=True)
def conference_list(request):
    res = deep_dict()
    if request.user.has_perm('main_app.can_admin'):
        confs = Conference.objects.all()
    else:
        confs = Conference.objects.all().filter(department_id=request.user.employee.department_id)
    for c in confs:
        res['conferences'][c.id]['conference'] = c.id
        res['conferences'][c.id]['name'] = c.name
        res['conferences'][c.id]['state'] = c.state
        res['conferences'][c.id]['language'] = c.languages
        res['conferences'][c.id]['type'] = c.type
        res['conferences'][c.id]['recognition'] = c.recognition
        res['conferences'][c.id]['room'] = c.room.id
        res['conferences'][c.id]['date'] = str(c.start_time)
    for r in Room.objects.all():
        res['rooms'][r.id] = r.name
    for l in Language.objects.all():
        res['languages'][l.shortcut] = l.name
    return res


@processView(auth_required=True)
def drop_file(request):
    conf_id = request.POST['conference']
    track_id = request.POST['file']
    peacedun = request.POST['peacedun']
    tr = Track.objects.get(pk=track_id)
    tr.is_active = False
    tr.save()

    c = Conference.objects.get(pk=conf_id)
    c.talkers_changed.add(tr.talker)
    c.save()

    res = deep_dict()
    res['files'][str(track_id)] = None
    res['info']['conference'] = conf_id

    return update_queues(conf_id, peacedun, res)


@processView(auth_required=True)
def cut_file(request):
    conf_id = request.POST['conference']
    track_id = request.POST['file']
    pos = request.POST['position']
    peacedun = request.POST['peacedun']
    tr = Track.objects.get(pk=track_id)
    tr.is_active = False
    tr.cut = True
    tr.save()
    c = Conference.objects.get(pk=conf_id)
    c.talkers_changed.add(tr.talker)
    c.save()

    an, bn, al, bl = cut_mp3(tr, pos)

    t1 = Track()
    t1.conference_id = conf_id
    t1.duration = int(al)
    t1.offset = int(tr.offset)
    t1.talker = tr.talker
    t1.path = an
    t1.text = tr.text
    t1.save()

    t2 = Track()
    t2.conference_id = conf_id
    t2.duration = int(bl)
    t2.offset = int(tr.offset + al)
    t2.talker = tr.talker
    t2.path = bn
    t2.text = ''
    t2.save()

    res = deep_dict()
    res['files'][str(track_id)] = None
    res['files'][str(t1.id)] = create_file_struct(t1.path, t1.talker_id, t1.offset, t1.duration, t1.text)
    res['files'][str(t2.id)] = create_file_struct(t2.path, t2.talker_id, t2.offset, t2.duration, t2.text)
    res['info']['conference'] = conf_id
    res['forceSelect'] = t1.id

    return update_queues(conf_id, peacedun, res)


@processView(auth_required=True)
def conf_updates(request):
    conf_id = request.GET['conference']
    peacedun = request.GET['peacedun']

    return update_queues(conf_id, peacedun, deep_dict())


@processView(auth_required=True)
def deleted_files(request):
    conf_id = request.GET['conference']
    peacedun = request.GET['peacedun']

    res = deep_dict()
    for t in Track.objects.filter(conference=conf_id, is_active=False, cut=False):
        res['deleted_files'][t.id] = create_file_struct(t.path, t.talker_id, t.offset, t.duration, t.text)

    return update_queues(conf_id, peacedun, res)


@processView(auth_required=True)
def restore_file(request):
    conf_id = request.POST['conference']
    tr_id = request.POST['file']
    peacedun = request.POST['peacedun']

    res = deep_dict()
    t = Track.objects.get(pk=tr_id, conference_id=conf_id)
    t.is_active = True
    t.save()

    res['files'][t.id] = create_file_struct(t.path, t.talker_id, t.offset, t.duration, t.text)
    res['info']['conference'] = conf_id

    c = Conference.objects.get(pk=conf_id)
    c.talkers_changed.add(t.talker)
    c.save()

    return update_queues(conf_id, peacedun, res)
