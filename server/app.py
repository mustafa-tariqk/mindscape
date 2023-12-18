from models import create_app

# Initialize the Flask app
app = create_app()

# Define your routes here
@app.route('/')
def index():
    return "Hello world"

if __name__ == '__main__':
    app.run(debug=True)
