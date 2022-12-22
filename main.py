from flask import Flask, request

from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Ogrenciler(Resource):
    def get(self):
        data = pd.read_csv('veriler.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        ad = request.args['ad']
        yas = request.args['yas']
        sehir = request.args['sehir']
        notu = request.args['notu']

        data = pd.read_csv('veriler.csv')

        new_data = pd.DataFrame({
            'ad': [ad],
            'yas': [yas],
            'sehir': [sehir],
            'notu': [notu]
        })

        data = data.append(new_data, ignore_index=True)
        data.to_csv('veriler.csv', index=False)
        return {'data': new_data.to_dict('records')}, 200

    def delete(self):
        ad = request.args['ad']
        data = pd.read_csv('veriler.csv')
        data = data[data['ad'] != ad]

        data.to_csv('veriler.csv', index=False)
        return {'message': 'Record deleted successfully.'}, 200


class Sehirler(Resource):
    def get(self):
        data = pd.read_csv('veriler.csv', usecols=[2])
        data = data.to_dict('records')

        return {'data': data}, 200


class Yaslar(Resource):
    def get(self):
        data = pd.read_csv('veriler.csv', usecols=[1])
        data = data.to_dict('records')

        return {'data': data}, 200


class Ad(Resource):
    def get(self, ad):
        data = pd.read_csv('veriler.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['ad'] == ad:
                return {'data': entry}, 200
        return {'message': 'Bu ada sahip giriş bulunamadı !'}, 404


# Add URL endpoints
api.add_resource(Ogrenciler, '/ogrenciler')
api.add_resource(Sehirler, '/sehirler')
api.add_resource(Ad, '/<string:ad>')
api.add_resource(Yaslar, '/yaslar')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
app.run()
