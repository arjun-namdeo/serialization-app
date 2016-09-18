# serialization_app
##  Description :
A Python command line tool which shows how you would take some sets of personal data (seq, shot, frame, status) and serialize/de-serialize them into 2 formats ( PICKLE Format and JSON Format) and display it in at least 2 different ways (HTML Output and TEXT Output) You could manually pass the arguments or use the Template CSV file to use as in input. This package has been written in such a way that it would be easy for a developer:

* To add support for additional storage formats (Easily extend in /scripts/encoder.py )
* To query a list of currently supported formats
* To supply an alternative reader/writer for one of the supported formats ( Find in /scripts/display_output.py )

## Command line Usage : 
```python
python serialization_app.py # This will use Template CSV file and generate output or python serialization_app.py -seq 010 -shot 200 -frame 78 # This will use user input and show in browser
```


## Package Structure :
* ./database/ : Default template csv file lives here
* ./output_files/ : All the serialized files and display file will get generate in this directory
* ./scripts/ : All Python scripts/modules lives in this directory