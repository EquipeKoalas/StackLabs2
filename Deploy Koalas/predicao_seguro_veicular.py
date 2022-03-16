import pickle
import pandas as pd
from flask import Flask, render_template, request

# Pastas de template e assets
application = Flask(__name__, template_folder='template', static_folder='template/assets')

# Modelo Treinado
modelo = pickle.load(open('./models/modelo.pkl', 'rb'))

@application.route('/')
def home():
    return render_template("homepage.html")


@application.route('/predicao_seguro_veicular')
def predicao_seguro_veicular():
    return render_template("form.html")


@application.route('/about')
def about():
    return render_template("about.html")


def get_data():
    Annual_Premium = request.form.get('Annual_Premium')
    Vintage = request.form.get('Vintage')
    Age = request.form.get('Age')
    Vehicle_Damage = request.form.get('Vehicle_Damage')
    Previously_Insured = request.form.get('Previously_Insured')

    d_dict = {'Annual_Premium': [Annual_Premium],
              'Vintage': [Vintage],
              'Age': [Age],
              'Vehicle_Damage': [Vehicle_Damage],
              'Previously_Insured': [Previously_Insured]}

    return pd.DataFrame.from_dict(d_dict, orient='columns')


@application.route('/send', methods=['POST'])
def show_data():
    df = get_data()
    df['Annual_Premium'] = df['Annual_Premium'].astype('float32')
    df['Vintage'] = df['Vintage'].astype('int64')
    df['Age'] = df['Age'].astype('int64')
    df['Vehicle_Damage'] = df['Vehicle_Damage'].astype('int64')
    df['Previously_Insured'] = df['Previously_Insured'].astype('int64')
    df = df[['Annual_Premium', 'Vintage', 'Age', 'Vehicle_Damage', 'Previously_Insured']]

    prediction = modelo.predict(df)
    outcome = 'Cliente tem interesse, vamos pra cimaaa galeraaaa!'
    imagem = 'felicidade.jpg'
    if prediction == 0:
        outcome = 'Cliente não tem interesse! Que pena, vamos continuar tentando.'
        imagem = 'tristeza.jpg'

    return render_template('result.html', tables=[df.to_html(classes='data', header=True, col_space=10)],
                           result=outcome, imagem=imagem)


if __name__ == "__main__":
    application.run(debug=True)
