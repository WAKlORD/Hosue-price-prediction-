from flask import Flask, request, render_template
from joblib import load
import pandas as pd

app = Flask(__name__, template_folder='templates')

model = load(r"C:\Users\Anand\Desktop\all job related project\SBMP\real_estate_price_prediction_pipeline.joblib")

locations = ['Airoli', 'Ambernath East', 'Ambernath West', 'Andheri', 'Andheri East', 'Andheri West', 'Badlapur', 'Badlapur East', 'Badlapur West', 'Bandra East', 'Bandra West', 'Belapur', 'Bhandup West', 'Bhayandar East', 'Bhiwandi', 'Boisar', 'Borivali East', 'Borivali West', 'Chembur', 'Chembur East', 'Dahisar', 'Dahisar East', 'Dahisar West', 'Dattapada', 'Dombivali', 'Dombivali East', 'Dombivli (West)', 'Dronagiri', 'Ghansoli', 'Ghatkopar', 'Ghatkopar East', 'Ghatkopar West', 'Goregaon', 'Goregaon East', 'Goregaon West', 'Hiranandani Estates', 'Jogeshwari East', 'Jogeshwari West', 'Juhu', 'Kalamboli', 'Kalwa', 'Kalyan East', 'Kalyan West', 'Kamothe', 'Kandivali East', 'Kandivali West', 'Kanjurmarg', 'Karanjade', 'Karjat', 'Kewale', 'Khar', 'Khar West', 'Kharghar', 'Kolshet Road', 'Koparkhairane Station Road', 'Koper Khairane', 'Koproli', 'Kurla', 'Kurla West', 'Lower Parel', 'Magathane', 'Majiwada', 'Malad East', 'Malad West', 'Matunga', 'Mira Road East', 'Mira Road and Beyond', 'Mulund', 'Mulund East', 'Mulund West', 'Naigaon East', 'Nala Sopara', 'Nalasopara East', 'Nalasopara West', 'Navi Basti', 'Nerul', 'PARSIK NAGAR', 'Palava', 'Palghar', 'Panvel', 'Parel', 'Powai', 'Prabhadevi', 'Rajendra Nagar', 'Sainath Nagar', 'Sanpada', 'Santacruz East', 'Santacruz West', 'Seawoods', 'Sector 10', 'Sector 17 Ulwe', 'Sector 18 Kharghar', 'Sector 19 Kharghar', 'Sector 20 Kharghar', 'Sector 21 Kamothe', 'Sector 22 Kamothe', 'Sector-18 Ulwe', 'Sector-3 Ulwe', 'Sector-8 Ulwe', 'Sector12 Kamothe', 'Sector9 Kamothe', 'Shil Phata', 'Sion', 'Taloja', 'Thakur Village', 'Thane', 'Thane West', 'Titwala', 'Ulwe', 'Vasai', 'Vasai West', 'Vasai east', 'Vasant Vihar', 'Vashi', 'Vikhroli', 'Ville Parle East', 'Ville Parle West', 'Virar', 'Virar East', 'Virar West', 'Wadala', 'Wadala East Wadala', 'Worli', 'kandivali', 'kavesar', 'matunga east', 'mumbai', 'other', 'taloja panchanand', 'vile parle west']

@app.route('/', methods=['GET', 'POST'])
def home():
    location = ""
    area = ""
    bedrooms = ""
    prediction = None

    if request.method == 'POST':
        location = request.form.get('location')
        area = request.form.get('area')  # Get as string to directly pass back to form
        bedrooms = request.form.get('bedrooms')
        # Prepare the input data in the same format as your model expects
        try:
            area_float = float(area)
            bedrooms_int = int(bedrooms)
            input_data = {
                'Location': [location],
                'Area': [area_float],
                'No. of Bedrooms': [bedrooms_int]
            }
            predicted_price = model.predict(pd.DataFrame(input_data))[0]
            prediction_rounded = round(predicted_price, 2)
            prediction = "Not Available" if prediction_rounded < 0 else f"₹ {prediction_rounded}"
        except ValueError:
            prediction = "Invalid Input"
        return render_template('index.html', locations=locations, prediction=prediction, location=location, area=area, bedrooms=bedrooms)
    return render_template('index.html', locations=locations, location=location, area=area, bedrooms=bedrooms)

if __name__ == '__main__':
    app.run(debug=True)