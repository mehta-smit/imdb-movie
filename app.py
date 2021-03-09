from imdb import create_flask_app

flask_app = create_flask_app()


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port='5000', debug=True)
