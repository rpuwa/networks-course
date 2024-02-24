def id_generate():
    id = 0
    while True:
        yield id
        id += 1

id_generator = id_generate()