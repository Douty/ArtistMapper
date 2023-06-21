"# Artist-Mapper" 

**To run on your own machine**
1. Create a virtual environment and install the required packages, found in "requirements.txt".
2. create a .env file and input the API keys which could be obtained at https://developer.spotify.com/, following the .env_sample format.
3. In "app.py" remove the function ```def create_app()``` and the ```return app```.
4. Fix the indentation
5. Remove ```serve(app, host='0.0.0.0',port=8080,threads=2)``` and replace it with ```app.run()```
6. In the terminal, write this command ```Flask run```


