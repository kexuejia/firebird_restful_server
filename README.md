# Firebird RESTful server

Simple python app which makes sql requests to firebird database(s) and returns result in JSON format

## Requirements

 - Python packages: flask, fdb
 - FirebirdSQL client libraries


## Running
   python app.py


## Usage
    - default server running on 0.0.0.0:5000  
    - there are two endpoints available [GET] /select  and [POST] /execute    
## Examples
```
   curl --location --request GET 'http://127.0.0.1:5000/select' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "connect": {
        "db":"127.0.0.1/3050:database_alias",
        "user":"SYSDBA",
        "password": "masterkey",
        "charset" : "WIN1251",
        "sql_dialect" : 1,
        "fb_library_name" : "firebird_osx/libfbclient.dylib"
    },
    "query": "select id,name,photo from dict_employees "


  }'
  ```


  ```
  curl --location --request POST 'http://127.0.0.1:5000/execute' \
--header 'Content-Type: application/json' \
--data-raw '{
    "connect": {
        "db":"127.0.0.1/3050:database_alias",
        "user":"SYSDBA",
        "password": "masterkey",
        "charset" : "WIN1251",
        "sql_dialect" : 1,
        "fb_library_name" : "firebird_osx/libfbclient.dylib"
    },
    "query": "insert into dict_employees(name) values(?)",
    "query_params": ["Rob Lee"]

}'
  ```

## Windows service installation
  Use NSSM - the Non-Sucking Service Manager and PyInstaller

  ```
  python.exe scripts\pyinstaller-script.py --onefile app.py
  nssm.exe install FirebirdRestApiService "c:\firebird_restful_server\dist\app.exe"
  net start FirebirdRestApiService

  ```


## TODO

  - add blobs support for /execute
  - add local configuration file  where store connect options and make connect object in request optional  
