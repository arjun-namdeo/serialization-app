# serialization_app (tested with Python 2.7.3) 
##  Description :
A Python command line tool which take some sets of personal data (seq, shot, frame, artist) and 
 
* Serialize/de-serialize them into 2 formats ( PICKLE Format and JSON Format) 
* Display it in 2 different ways (HTML Output and TEXT Output) 

**You could manually pass the arguments. If you dont pass any input, It will use template CSV file from database directory.**

#### This package has been written in such a way that it would be easy for a developer:

* To add support for additional storage formats (Easily extend in `/scripts/encoder.py` )
* To query a list of currently supported formats
* To supply an alternative reader/writer for one of the supported formats ( Find in `/scripts/display_output.py` )

## Command line Usage : 
```python
python serialization_app.py # This will use Template CSV file and generate output 
 
python serialization_app.py -seq 10 -shot 200 -frame 78 # This will use user input and show in browser
```


## Package Structure :
* **__./database/__** : Default template csv file lives here
* **__./output_files/__** : All the serialized files and display file will get generate in this directory
* **__./scripts/__** : All Python scripts/modules lives in this directory