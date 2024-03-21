from Sound import Generate_Depart_Annonce, Generate_Passing_Train, Generate_Delete_Train, AlarmSignal, GenerateStrike, GenerateDynamicDisplayOff
from flask import Flask, request, jsonify, send_file, Response
from io import BytesIO

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    # Vous pouvez personnaliser la réponse à l'erreur 404 ici
    return send_file('404.html')

@app.route('/')
def welcome():
    return send_file('index.html')

@app.route('/index.html')
def welcome2():
    return send_file('index.html')

@app.route('/TrainDeparture')
def TrainDeparture():
    # Extraire les paramètres de la requête URL
    train_name = request.args.get('train_name')
    train_number = request.args.get('train_number')
    plateform_type = request.args.get('plateform_type')
    plateform_indicator = request.args.get('plateform_indicator')
    arrival_station = request.args.get('arrival_station')
    departure_Hours = request.args.get('departure_Hours')
    departure_Minutes = request.args.get('departure_Minutes')
    TypeJingle = request.args.get('TypeJingle')
    path = Generate_Depart_Annonce(train_name, train_number, plateform_type, plateform_indicator, arrival_station, departure_Hours, departure_Minutes, TypeJingle)
    # Appeler la fonction generate_voicemail avec les paramètres extraits
    return path

@app.route('/PassingTrain')
def PassingTrain():
    # Extraire les paramètres de la requête URL
    Sidding_type = request.args.get('Sidding_type')
    Sidding_indicator = request.args.get('Sidding_indicator')

    path = Generate_Passing_Train(Sidding_type, Sidding_indicator)

    return path

# train supprimé :
@app.route('/DeleteTrain')
def DeleteTrain():
    # Extraire les paramètres de la requête URL
    train_name = request.args.get('train_name')
    train_number = request.args.get('train_number')
    train_destination = request.args.get('train_destination')
    departure_Hours = request.args.get('departure_Hours')
    departure_Minutes = request.args.get('departure_Minutes')

    path = Generate_Delete_Train(train_name, train_number, train_destination, departure_Hours, departure_Minutes)

    return path

@app.route('/Strike')
def Strike():
    return GenerateStrike()

@app.route('/AlarmInBord')
def AlarmInBord():
    train_name = request.args.get('train_name')
    return AlarmSignal(train_name)

@app.route('/DynamicDisplayOff')
def DynamicDisplayOff():
    return GenerateDynamicDisplayOff()

if __name__ == '__main__':
    app.run(debug=True)

    
# requette : http://127.0.0.1:5000/TrainDeparture?train_name=TGV&train_number=234&plateform_type=Q&plateform_indicator=H&arrival_station=Marseille&departure_Hours=10&departure_Minutes=30&TypeJingle=Station