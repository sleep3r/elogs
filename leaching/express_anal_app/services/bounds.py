
def get_critical_values(model, values):
    wrong = []
    fields = [f.name for f in model._meta.get_fields(include_parents=False)]
    for name, bounds in values.items():
        print(name)
        val = getattr(model, name)
        if val and name in fields and not (bounds[0] <= float(val) <= bounds[1]):
            wrong.append(name)
    return wrong