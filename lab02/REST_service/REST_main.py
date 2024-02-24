import flask, json, os
from product_json import Product

app = flask.Flask(__name__)
RELATIVE_UPLOAD_FOLDER = 'lab02\REST_service\images'
app.config['UPLOAD_FOLDER'] = 'images'

products = {}

@app.route('/product', methods=['POST'])
def product_add():
    data = json.loads(flask.request.data if flask.request.data else '{}')
    product = Product(data)
    products[str(product.id())] = product
    return product.json()

@app.route('/product/<id>', methods=['GET'])
def product_get(id):
    if id not in products.keys():
        return flask.Response('Product not found', status=404)
    else:
        return products[id].json()
    
@app.route('/product/<id>', methods=['PUT'])
def product_upd(id):
    data = json.loads(flask.request.data if flask.request.data else '{}')
    if id not in products.keys():
        return flask.Response('Product not found', status=404)
    elif 'id' in data and str(data['id']) != id and str(data['id']) in products.keys():
        return flask.Response('Incorrect update request', status=409)
    else:
        new_id = id if 'id' not in data else str(data['id'])
        products[id].update(data)
        if new_id != id:
            products[new_id] = products.pop(id)
        return products[new_id].json()

@app.route('/product/<id>', methods=['DELETE'])
def product_del(id):
    if id not in products.keys():
        return flask.Response('Product not found', status=404)
    else:
        return products.pop(id).json()

@app.route('/products', methods=['GET'])
def products_get():
    return [prod.json() for prod in products.values()]

@app.route('/product/<id>/image', methods=['POST'])
def product_set_image(id):
    if id not in products.keys():
        return flask.Response('Product not found', status=404)
    else:
        icon = flask.request.files.get('icon', '')
        products[id].set_icon(icon)
        icon.save(os.path.join(RELATIVE_UPLOAD_FOLDER, icon.filename))
        return flask.Response('', status=204)

@app.route('/product/<id>/image', methods=['GET'])
def product_get_image(id):
    if id not in products.keys():
        return flask.Response('Product not found', status=404)
    elif products[id].icon():
        return flask.send_file(os.path.join(app.config['UPLOAD_FOLDER'], products[id].icon()), mimetype='image/png')
    else:
        return flask.Response('Image not found', status=404)

if __name__ == '__main__':
    app.run(debug=True)