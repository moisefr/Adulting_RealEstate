# Importing required functions
from flask import Flask, render_template, request, Response, url_for, redirect
import json
import os
import pandas
from fileinput import filename
import folium
from geopy.geocoders import Nominatim

# Initialize the Flask application
app = Flask(__name__)
#Key Data Objects In the End

###Future Functions
##Input the City from the form


Zip_Code_Level_Data = []
House_Level_Data = []

#Calculation Functions

#Map Creation
def create_Area_Map():
    # Initialize Nominatim geocoder
    geolocator = Nominatim(user_agent="folium_city_map")

    # Get location details for a city
    city_name = "Philadelphia, Pennsylvania"
    location = geolocator.geocode(city_name)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        print(f"Coordinates for {city_name}: Latitude={latitude}, Longitude={longitude}")
    mapObj = folium.Map(location=[latitude, longitude],zoom_start=11)

    #Adding Neighborhoods
    #geo_file = 'https://github.com/opendataphilly/open-geo-data/blob/cd29c106382ef844f08e3212a82772cea0c9a55e/philadelphia-neighborhoods/philadelphia-neighborhoods.geojson'
    geo_file = os.path.join(app.static_folder, 'data', 'Zipcodes_Poly.geojson')

    folium.GeoJson(geo_file, zoom_on_click=True).add_to(mapObj)

    return mapObj

def create_Marker(input_map):
    html = folium.Html(
        f"""
            <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Address Location</title>
        <!-- Bootstrap 5 CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        </head>
        <body class="bg-light mw-100" style="width: 750px;" >

        <!-- Header -->
        <div class="container my-4">
            <h1 class="text-center" style="font-family: Calibri; color: black;">
            <strong><u>Address Location</u></strong>
            </h1>
        </div>

        <!-- Accordion -->
        <div class="container">
            <div class="accordion" id="accordionExample" >

            <!-- First Item -->
            <div class="accordion-item">
                <h2 class="accordion-header" id="headingOne">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" 
                        data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne" style="color:blue;">
                    <i class="fa fa-newspaper"></i> 🤫 House Data 
                </button>
                </h2>
                <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                <div class="accordion-body text-justify">
                    Data Place Holder
                </div>
                </div>
            </div>

            <!-- Second Item -->
            <div class="accordion-item">
                <h2 class="accordion-header" id="headingTwo">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" 
                        data-bs-target="#collapseTwo" aria-expanded="true" aria-controls="collapsetwo" style="color:blue;">
                    <i class="fa fa-newspaper"></i> 🤫 Price History
                </button>
                </h2>
                <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingTwo" data-bs-parent="#accordionExample">
                <div class="accordion-body text-justify">
                    Data Place Holder
                </div>
                </div>
            </div>

            <!-- THird Item -->
            <div class="accordion-item">
                <h2 class="accordion-header" id="headingThree">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                        data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree" style="color:blue;">
                    <i class="fa fa-usd"></i> 🤫 ZipCode Data
                </button>
                </h2>
                <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionExample">
                <div class="accordion-body text-justify">
                    Data Place Holder
                </div>
                </div>
            </div>

            </div>
        </div>
        <br/>
        <center>
            <iframe src="https://www.example.com" width="500px" height="90%" title="Embedded Content"></iframe>
        </center>
        <!-- Bootstrap JS -->
            
        </body>
    </html>
        """, 
        script=True)

    detailed_popup  = folium.Popup(html, max_width=1000)
    folium.Marker([input_map.location[0] - 0.04127332, input_map.location[1] - 0.078362],
                popup=detailed_popup).add_to(input_map)
    return 
# Home route
@app.route("/")
def home():
    return render_template('/upload.html')

@app.route('/results', methods=["GET"])
def results():
        #Call Function to Create Map
        final_map =  create_Area_Map()
        #Call functions that take in either zip code or house level data

        #Set Marker
        create_Marker(final_map)
        
        # set iframe width and height
        final_map.get_root().width = "100%"
        final_map.get_root().height = "600px"

        # derive the iframe content to be rendered in the HTML body
        iframe = final_map.get_root()._repr_html_()

        return render_template('/results.html', properties = Zip_Code_Level_Data, final_map = iframe) 

@app.route("/calculations", methods=["GET","POST"])
def calculations():

    # Read the File using Flask request
    file = request.files['file']
    print("di request:", file)
    # save file in local directory
    # file.save(file.filename)

    if request.method == "POST":
        try: 
            data = pandas.read_excel(file)
            print("di panda:", data) 
            #Split into zip code and housing level data
            Zip_Code_Level_Data.append(data)
            return Response(
                response = json.dumps(
                        {"message": "List of Properties injested", 
                        }),
                    status = 200,
                    mimetype='application/json'
            ) and redirect('/results') 
        except:
            return("Error")
    return render_template('/uploads.html') 

    # Parse the data as a Pandas DataFrame type
    
    #Return Results of a Successful Post Request
    # Return HTML snippet that will render the table
    #return data.to_html()
    return "Success!"



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug= True)

