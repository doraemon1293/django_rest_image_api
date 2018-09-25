# django_rest_image_api

A project provides api to allowing uploading rotating and retrieving pictures,coverting the format.

### Quick Start

1 clone the project

2 virtualenv -p python3.4 venv # Note: python3.5 should also work
  source venv/bin/activate
  pip install -r requirements.txt
  cd django_rest_image_api
  python manage.py migrate
  python manage.py runserver # starts the server 

Please see requirements.txt for more information.

## API

1 get image list api
  URL: image_api/
  example:
    http GET http://127.0.0.1:8000/image_api/
    response:
            [
                {
                    "pk": 47,
                    "fn": "/images/7033ab72-1bfa-46e4-9428-3b3e780d5972.jpeg",
                    "extension": "jpeg"
                }
            ]
    # pk is primary key, fn the url of uploaded file, extension is the format of the image

2 get a image
  URL: image_api/<int:pk>/
  example:
  http GET http://127.0.0.1:8000/image_api/47
  response  
        {
            "extension": "jpeg",
            "fn": "/images/7033ab72-1bfa-46e4-9428-3b3e780d5972.jpeg",
            "pk": 47
        }

3 to download file
  URL: HOSTNAME+fn
  example:
    http http://127.0.0.1:8000/images/7033ab72-1bfa-46e4-9428-3b3e780d5972.jpeg -o download_file_name
    
2 covert format of a image
  URL: image_api/<int:pk>/transfer/<image_format:extension>/
  example:
  http GET http://127.0.0.1:8000/image_api/47/transfer/png/
  response.data
    {
    "extension": "png",
    "fn": "/images/7033ab72-1bfa-46e4-9428-3b3e780d5972.png",
    "pk": 32,
    "source_pk": 47
}

4 rotate image
  URL: image_api/<int:pk>/rotate/<int:degree>/
  http GET http://127.0.0.1:8000/image_api/47/rotate/90/
  response.data
  {
    "degree": 90,
    "fn": "/images/7033ab72-1bfa-46e4-9428-3b3e780d5972_90..jpeg",
    "pk": 1,
    "source_pk": 47
}




