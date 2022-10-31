from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) # instance of flask app
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:testpwd@some-mysql:3306/scrape_data"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)

class Ad_values(db.Model): # sqlalchemy doesn¨t like tables with no PK
    __tablename__ = "price_info"

    id = db.Column(db.String(20),name="ad_id", primary_key=True)
    price = db.Column(db.Integer, name="ad_price")
    date = db.Column(db.Date, name="date", primary_key=True)



@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("temp3.html")
    else:
        link = request.form["ad_id"]
        # 1048745804
        # some link check, if it 
        query = Ad_values.query.filter(Ad_values.id==link).order_by(Ad_values.date.desc())
        len = 0
        for _ in query:
            len +=1
        if not len:
            return render_template("temp4.html", id = link)
            
        else:
            return render_template("temp2.html", result = query, id = link)


if __name__ == "__main__":
    app.run(debug=True)



