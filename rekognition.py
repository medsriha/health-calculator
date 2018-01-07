from __future__ import print_function
import boto3
from decimal import Decimal
import json
import os
import urllib
import argparse
import io
import requests

from google.cloud import vision
from google.cloud.vision import types

rekognition = boto3.client('rekognition')


def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response

def lambda_handler(event, context):
    bucket = 'team4bucket'
    key = event['Records'][0]['s3']['object']['key']
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = 'https://s3.amazonaws.com/' + bucket + '/' + key
    responseG = client.label_detection(image=image)
    labels = responseG.label_annotations
    score = 0
    count = 0
    fincalories = 0
    finfat = 0
    fincarbohydrate = 0
    finprotein = 0
    finfiber = 0
    finsodium = 0
    finsugars = 0
    fincholesterol = 0
    for label in labels:
        count += 1
        tag = str(label.description)
        print (tag)
        headers = {'Content-Type': 'application/json', 'x-app-id': 'b11b4c83', 'x-app-key': 'a6337e35998c02709ce782e12f66c640'}
        body = json.dumps({'query': tag,'timezone': 'US/Eastern'})
        r = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', headers = headers, data=body)
        message = json.loads(r.text)
        if "message" in message and message["message"] == "We couldn't match any of your foods":
            score = score + 0
            print (score)
        else:
            if message["foods"][0]["nf_calories"] is None:
                fincalories = fincalories + 0
                calories = 0
            else:
                fincalories = fincalories + int (message["foods"][0]["nf_calories"])
                calories = int (message["foods"][0]["nf_calories"])

            if message["foods"][0]["nf_total_fat"] is None:
                finfat = finfat + 0
                fat = 0
            else:
                finfat = finfat + int (message["foods"][0]["nf_total_fat"])
                fat = int (message["foods"][0]["nf_total_fat"])

            if message["foods"][0]["nf_total_carbohydrate"] is None:
                fincarbohydrate = fincarbohydrate + 0
                carbohydrate = 0
            else:
                fincarbohydrate = fincarbohydrate + int (message["foods"][0]["nf_total_carbohydrate"])
                carbohydrate = int (message["foods"][0]["nf_total_carbohydrate"])

            if message["foods"][0]["nf_protein"] is None:
                finprotein = finprotein + 0
                protein = 0
            else:
                finprotein = finprotein + int (message["foods"][0]["nf_protein"])
                protein = int (message["foods"][0]["nf_protein"])

            if message["foods"][0]["nf_dietary_fiber"] is None:
                finfiber = finfiber + 0
                fiber = 0
            else:
                finfiber = finfiber + int (message["foods"][0]["nf_dietary_fiber"])
                fiber = int (message["foods"][0]["nf_dietary_fiber"])

            if message["foods"][0]["nf_sodium"] is None:
                finsodium = finsodium + 0
                sodium = 0
            else:
                finsodium = finsodium + int (message["foods"][0]["nf_sodium"])
                sodium = int (message["foods"][0]["nf_sodium"])

            if message["foods"][0]["nf_sugars"] is None:
                finsugars = finsugars + 0
                sugars = 0
            else:
                finsugars = finsugars + int (message["foods"][0]["nf_sugars"])
                sugars = int (message["foods"][0]["nf_sugars"])

            if message["foods"][0]["nf_cholesterol"] is None:
                fincholesterol = fincholesterol + 0
                cholesterol = 0
            else:
                fincholesterol = fincholesterol + int (message["foods"][0]["nf_cholesterol"])
                cholesterol = int (message["foods"][0]["nf_cholesterol"])
            score = score + calories * 0.5 - fiber + fat + carbohydrate * 0.3 + protein * 0.2 + sugars * 0.6 + cholesterol * 0.8 + sodium * 0.5
            print (score)
        if count > 3:
            break
    try:
        response = detect_labels(bucket, key)
        for x in range(4):
            tagA = response['Labels'][x]['Name']
            print (tagA)
            headers = {'Content-Type': 'application/json', 'x-app-id': 'b11b4c83', 'x-app-key': 'a6337e35998c02709ce782e12f66c640'}
            body = json.dumps({'query': tagA,'timezone': 'US/Eastern'})
            r = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', headers = headers, data=body)
            message = json.loads(r.text)
            if "message" in message and message["message"] == "We couldn't match any of your foods":
                score = score + 0
                print (score)
            else:
                if message["foods"][0]["nf_calories"] is None:
                    fincalories = fincalories + 0
                    calories = 0
                else:
                    fincalories = fincalories + int (message["foods"][0]["nf_calories"])
                    calories = int (message["foods"][0]["nf_calories"])

                if message["foods"][0]["nf_total_fat"] is None:
                    finfat = finfat + 0
                    fat = 0
                else:
                    finfat = finfat + int (message["foods"][0]["nf_total_fat"])
                    fat = int (message["foods"][0]["nf_total_fat"])

                if message["foods"][0]["nf_total_carbohydrate"] is None:
                    fincarbohydrate = fincarbohydrate + 0
                    carbohydrate = 0
                else:
                    fincarbohydrate = fincarbohydrate + int (message["foods"][0]["nf_total_carbohydrate"])
                    carbohydrate = int (message["foods"][0]["nf_total_carbohydrate"])

                if message["foods"][0]["nf_protein"] is None:
                    finprotein = finprotein + 0
                    protein = 0
                else:
                    finprotein = finprotein + int (message["foods"][0]["nf_protein"])
                    protein = int (message["foods"][0]["nf_protein"])

                if message["foods"][0]["nf_dietary_fiber"] is None:
                    finfiber = finfiber + 0
                    fiber = 0
                else:
                    finfiber = finfiber + int (message["foods"][0]["nf_dietary_fiber"])
                    fiber = int (message["foods"][0]["nf_dietary_fiber"])

                if message["foods"][0]["nf_sodium"] is None:
                    finsodium = finsodium + 0
                    sodium = 0
                else:
                    finsodium = finsodium + int (message["foods"][0]["nf_sodium"])
                    sodium = int (message["foods"][0]["nf_sodium"])

                if message["foods"][0]["nf_sugars"] is None:
                    finsugars = finsugars + 0
                    sugars = 0
                else:
                    finsugars = finsugars + int (message["foods"][0]["nf_sugars"])
                    sugars = int (message["foods"][0]["nf_sugars"])

                if message["foods"][0]["nf_cholesterol"] is None:
                    fincholesterol = fincholesterol + 0
                    cholesterol = 0
                else:
                    fincholesterol = fincholesterol + int (message["foods"][0]["nf_cholesterol"])
                    cholesterol = int (message["foods"][0]["nf_cholesterol"])
                score = score + calories * 0.5 - fiber + fat + carbohydrate * 0.3 + protein * 0.2 + sugars * 0.6 + cholesterol * 0.8 + sodium * 0.5
                print (score)
        score = score/15
        print (score)
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
    payload = {'score':score, 'calories':fincalories, 'fat':finfat, 'carbohydrate':fincarbohydrate, 'fiber':finfiber, 'protein':finprotein, 'sugars':finsugars,'cholesterol':fincholesterol, 'sodium':finsodium}
    fin = requests.post('http://ec2-52-207-251-163.compute-1.amazonaws.com:3000/', data = payload);
    return fin.status_code
        