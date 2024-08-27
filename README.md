# CarSeer-AI

## Overview

CarSeer AI is a comprehensive FastAPI project that provides APIs for decoding Vehicle Identification Numbers (VINs) and predicting the market value of a car. The VIN decoding API fetches details about a vehicle based on its VIN, such as make, model, year, and more. The market value prediction API utilizes machine learning models to estimate the current market value of a given car.

## Features

- **VIN Decode**: Retrieve detailed information about a vehicle by providing its VIN.
- **Market Value Prediction**: Predict the market value of a car based on various features.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Carseer-dev/carseer-ai
   cd carseer-ai
   
2. Install Dependencies:

   ```bash
    pip install -r requirements.txt

## Usage

1. Start the FastAPI application:

   ```bash
   uvicorn main:app --reload
   #This will start the server locally, and the APIs will be accessible at http://127.0.0.1:8000.
2. Open the Swagger [documentation](http://127.0.0.1:8000/docs) or [ReDoc documentation](http://127.0.0.1:8000/redoc) to explore and test the VIN decoding and market value prediction APIs.
3. Get Bearer Token, send a POST request to the `/api/v1/jwt-provider` with email and password as a body 
   ````JSON
    {
        "email": "user@example.com",
        "password": "string"
    }
4.  **VIN Decode API:** To decode a VIN, send a GET request to the `/api/v1/decode?vin={vin}` endpoint, where `{vin}` is the VIN you want to decode.
Example:
   ```bash
      curl -X 'GET' \
      'http://127.0.0.1:8000/decode/JTMBD33VX62078038' \
      -H 'accept: application/json'
   ````
   Replace **JTMBD33VX62078038** with the actual VIN you want to decode.

## Output
The current output for the decode API is providing the decoded information about the vin as well as the market value
```JSON
{
  "Make": {
    "ar_name": "تويوتا",
    "en_name": "Toyota"
  },
  "Model": {
    "ar_name": "RAV4 الهجين",
    "en_name": "RAV4 Hybrid"
  },
  "Year": 2006,
  "Manufacturer": "TOYOTA",
  "Region": "Asia",
  "VIN": "JTMBD33VX62078038",
  "WMI": "JTM",
  "Serial": "078038",
  "Market Value": 6602.75
}
```

**Note:** the current request and response for the decoding API might change based on business cases.
