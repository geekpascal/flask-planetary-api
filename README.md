# flask-planetary-api
The Flask Planetary API project is a web-based application built with Flask, which provides developers with structured access to information about the planets in our solar system through a variety of endpoints, making it a useful tool for building applications and conducting research.

## Tech Stack (Dependencies) 👩‍💻 

### Dependencies 
Our tech stack will include the following:
 * 💻 **virtualenv** as a tool to create isolated Python environments
 * 🛅 **SQLAlchemy ORM** to be our ORM library of choice
 * 📚 **PostgreSQL** as our database of choice
 * 🐍 **Python3** 
 * 🧪 **Flask** as our server language and server framework
 
You can download and install all the dependencies mentioned above using `pip install -r requirements.txt` 

## Development Setup 
1. **Download the project starter code locally**
```
git clone https://github.com/geekpascal/flask-planetary-api.git
cd flask-planetary-api/ 
```

2. **Create an empty repository in your Github account online.

3. **Initialize and activate a virtualenv using:**

```
python -m venv env
source env/bin/activate  
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you would use the analogous command shown below:
```
source env/Scripts/activate
```

4. **Install the dependencies:** 
```
pip install -r requirements.txt
```

5. **Run the development server:**
```
export FLASK_APP=run.py
export FLASK_ENV=development # enables debug mode
python app.py
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)
