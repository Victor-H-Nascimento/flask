from src.app import app, make_imports_into_app
make_imports_into_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
