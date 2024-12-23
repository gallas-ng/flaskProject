from flask import Flask, request
app = Flask(__name__)

Stores = [
    {
        "title" : "My Store",
        "items" : [
            { "name" : "Chair", "price" : 100 },
            { "name" : "Table", "price" : 600 },
        ]
    }
]
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/store')
def stores():
    return {'stores': Stores}

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = { "title" : request_data["title"], "items" : []}
    Stores.append(new_store)
    return new_store, 201

@app.post('/store/<string:title>/item')
def create_item(title):
    request_data = request.get_json()
    for store in Stores:
        if store["title"] == title:
            new_item = { "name" : request_data['name'], "price" : request_data["price"] }
            store["items"].append(new_item)
            return new_item, 201
    return {"message" : "Store not found"}, 404

@app.get('/store/<string:title>')
def get_store(title):
    for store in Stores:
        if store["title"] == title:
            return store, 200
    return {"message" : "Store not found"}, 404

@app.get('/store/<string:title>/item')
def get_item(title):
    for store in Stores:
        if store["title"] == title:
            return {"items" :store['items']}, 200
    return {"message" : "Store not found"}, 404




if __name__ == '__main__':
    app.run()
