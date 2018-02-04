

with open('a_run.csv', as f):
    for b in Block.select():
        for day in precipitacion:
            b.next(precipitacion[day])
            f.write(b.to_dict)
