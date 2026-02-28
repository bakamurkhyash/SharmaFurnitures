from flask import Flask, render_template
import cloudinary
import cloudinary.api
from cloudinary.utils import cloudinary_url

app = Flask(__name__)

cloudinary.config(
    cloud_name="dlkjvnxpu",
    api_key="288393286726996",
    api_secret="i3pm1Q9GRnMwY-HAh62mbj1caz0"
)

result = cloudinary.api.resources(type = "upload", max_results = 77)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return result

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', images=result.get('resources', []))

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

if __name__ == '__main__':
    app.run(debug=True)
