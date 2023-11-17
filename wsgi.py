"""Application entry point."""
from webapp import create_app
from waitress import serve
 
app = create_app()

if __name__ == "__main__":
    # serve(app, host="127.0.0.1", load_dotenv=True, port=8083, debug=True)
    app.run(host="127.0.0.1", load_dotenv=True, port=8083, debug=True)