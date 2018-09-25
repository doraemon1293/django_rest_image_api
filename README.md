

# ProgImage API

A project provides API to allowing uploading, rotating and retrieving pictures,coverting the format.

## Running Environment
Windows  
Python 3.5.4  
Virtual environment  
Django 2.1.1  
djangorestframework 3.8.2  


## Quick Start

```bash
git clone https://github.com/doraemon1293/django_rest_image_api.git
cd django_rest_image_api
virtualenv -p python3.4 venv # Note: python3.5 should also work
source venv/bin/activate
pip install -r requirements.txt
cd django_rest_imageupload_backend
python manage.py migrate
python manage.py runserver # starts the server 
```
Please see requirements.txt for more information.

## API

1.  List all images  
   API: ``` image_api/  ```  
   Method: GET  
   Possible Status Code: 200, 50X  
   Example of input: ```http GET http://127.0.0.1:8000/image_api/```  
   Example of output  
```
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 87
Content-Type: application/json
Date: Tue, 25 Sep 2018 20:42:10 GMT
Server: WSGIServer/0.2 CPython/3.5.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "extension": "jpeg",
        "fn": "/images/7033ab72-1bfa-46e4-9428-3b3e780d5972.jpeg",
        "pk": 47
    }
]

```
pk is primary key, fn is the URL of uploaded file, extension is the format of the image  

2.  Get a image  
  URL: ```image_api/<int:pk>/  ```  
   Method: GET  
   Possible Status Code: 200, 404  
   Example of input: ```http GET http://127.0.0.1:8000/image_api/47/```  
   Example of output:  
   ```
   HTTP/1.1 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Length: 85
Content-Type: application/json
Date: Tue, 25 Sep 2018 20:43:29 GMT
Server: WSGIServer/0.2 CPython/3.5.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "extension": "jpeg",
    "fn": "/images/7033ab72-1bfa-46e4-9428-3b3e780d5972.jpeg",
    "pk": 47
}
```


3.  Upload images  
    API: ``` image_api/```  
   Method: POST  
   Possible Status Code: 201, 50X  
Example of input: ```http -f POST http://127.0.0.1:8000/i
mage_api/ fn@C:\1.jpeg```  
Example of output:  
```
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 85
Content-Type: application/json
Date: Tue, 25 Sep 2018 20:49:02 GMT
Server: WSGIServer/0.2 CPython/3.5.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "extension": "jpeg",
    "fn": "/images/275af740-3786-4e2f-b93c-b16cb634b733.jpeg",
    "pk": 48
}
```
4.  Convert format of a image  
    API:```image_api/<int:pk>/transfer/<image_format:extension>/```  
   Method: GET  
   Possible Status Code: 200, 404  
Example of input: ```http GET  http://127.0.0.1:8000/image_api/48/transfer/png/```  
Example of output:  
```
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Length: 98
Content-Type: application/json
Date: Tue, 25 Sep 2018 20:53:13 GMT
Server: WSGIServer/0.2 CPython/3.5.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "extension": "png",
    "fn": "/images/275af740-3786-4e2f-b93c-b16cb634b733.png",
    "pk": 34,
    "source_pk": 48
}
```
pk is primary key, source_pk is the foreign key to original image. fn is the URL of uploaded file, extension is the format of the image.

5.  Rotate image  
    API: ```image_api/<int:pk>/rotate/<int:degree>/```  
   Method: GET  
   Possible Status Code: 200, 404  
Example of input: ```http GET  http://127.0.0.1:8000/image_api/48/rotate/90/```  
Example of output:  
```
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Length: 96
Content-Type: application/json
Date: Tue, 25 Sep 2018 20:57:50 GMT
Server: WSGIServer/0.2 CPython/3.5.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "degree": 90,
    "fn": "/images/275af740-3786-4e2f-b93c-b16cb634b733_90..jpeg",
    "pk": 2,
    "source_pk": 48
}
```
6.  To download file  
  URL: HOSTNAME+fn  
  example:```  
    http http://127.0.0.1:8000/images/7033ab72-1bfa-46e4-9428-3b3e780d5972.jpeg -o download_file_name```
    

## TEST
python manage.py test
1. class ListImagesTest  
  test the api to list all images  
2. class GetImageTest  
  test the api to get a specific all images as per pk  
3. class UploadImageTest  
  upload an Image, get the Image file, download file and compare whether the files is the same with original one  
4. class TransferImageTest  
  upload the image and download the format converted image,
  if _compare_file_required, this method will also compare whether the transfered file is exactly the same with sample file
  As some conversion cannot guarantee the file is always the same, for example from png to jpeg, so should not compare files in that case  
5. class RotateImageTest  
  upload the image and download the rotated image. this method will also compare whether the transfered file is exactly the same with sample file  


##Implementation Discussions
1. What language platform did you select to implement the microservice? Why?  
    Python,django-rest, it is a flexible, simple to develop to RESTful services.  
    
2. How did you store the uploaded images?  
    They're save as file in MEDIA_ROOT folder (local file system)  
    
3. What would you do differently to your implementation if you had more time?  
  - Switch sqlite to another database , for example, mysql for Robust and commercial support, Key-value NoSQL Database (Redis, MongoDB etc.) for fast retrieval.  
  - use cloud storage instead of local file system  
  - use load balance with multiple backend services to have better horizontal scalability  
  - use Docker and Kubernetes to ensure equivalent environment and ease deployment.  


4. How would coordinate your development environment to handle the build and test process?  
    Create separate virtual environments for development, test, and production.  The deployment environment only contains essential dependencies.  

5. What technologies would you use to ease the task of deploying the microservices to a production runtime environment?  
    Continuous Integration/Continuous Deployment Tools such as Jenkins and Travis CI can be employed to ease the task of deploying the microservices.  

6. What testing did (or would) you do, and why?
    Unit test has been added as described in Section XXX.  In the test environment, I would like to run Stress test to understand the robustness of the system.



##Authors
Yan HUANG
