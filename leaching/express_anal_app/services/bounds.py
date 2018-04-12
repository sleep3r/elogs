
def get_critical_values(model, values):
    wrong = []
    fields = [f.name for f in model._meta.get_fields(include_parents=False)]
    for name, bounds in values.items():
        if name in fields and not (bounds[0] <= getattr(model, name) <= bounds[0]):
            wrong.append(name)
    return wrong