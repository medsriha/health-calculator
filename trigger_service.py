from flask import Flask, request
import boto3
import random

app = Flask(__name__, static_url_path='')

DESTINATION_BUCKET = 'team4bucket'

@app.route("/trigger", methods=['GET'])
def handle():

    if request.method == 'GET':
        print request
        source_bucket_name = request.args.get('bucketName')
        print source_bucket_name
        s3 = boto3.client('s3')
        s4 = boto3.resource('s3')
        source_bucket = s4.Bucket(source_bucket_name)
        dest_bucket = s4.Bucket(DESTINATION_BUCKET)
    
        keyslist = []
        for file in source_bucket.objects.all():
            keyslist.append(file.key)

        total = len(keyslist)
        randomIndex = random.randint(0,total-1) 
        source_key = keyslist[randomIndex]   
 
        source= '{0}/{1}'.format(source_bucket, source_key)
        s3.copy_object(Bucket=DESTINATION_BUCKET, CopySource=source_bucket_name + '/' + source_key, Key=source_key)

        return 'success'            
if __name__ == '__main__':
    app.run(threaded=True, debug=True, host="0.0.0.0", port=7000)

