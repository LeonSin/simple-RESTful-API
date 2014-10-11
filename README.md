simple-RESTful-API
==================

a simple RESTful API service to receive HTTP requests which can automatically parse request and store it appropriately, and send an email notification to the sender and a dedicated email account immediately.

##程序依赖:
本项目基于Python2.7开发,使用了`tornado`框架.
##使用方法:
1.将`config.py.example`改名成`config.py`,并按文件中的说明来完成必要配置.
2.执行命令`python server.py`来运行.如果想将日志保存成文件形式,请加上运行参数-log_file_prefix,如`-log_file_prefix=/home/log.txt`.


### Here is the field list for the request:

| field          | Description                        | Type   |
|----------------|------------------------------------|--------|
| **email**      | Sender's email address             | string |
| first_name     | Sender's first name                | string |
| last_name      | Sender's last name                 | string |
| contact_number | Sender's mobile phone number       | string |
| title          | A title for the request            | string |
| content        | a short description of the request | string |
| link           | a web address                      | string |

all fields above are required.
Sample request
--------------
    $ curl -X POST -H "Accept: application/json" -d @data.json http://localhost:8000/rest

    # data.json
    {
        "email": "tester@test.com",
        "first_name": "Peter",
        "last_name": "Pan",
        "contact_number": "86-13227892789",
        "title": "Request Title",
        "content": "Request Content",
        "link": "https://github.com"
    }

