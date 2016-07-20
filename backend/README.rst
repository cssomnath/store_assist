-------------
Hackthon Demo
-------------
System requirements:
--------------------
python3, OS X.

Other requirements:
-------------------
- Register with Microsoft face(https://www.microsoft.com/cognitive-services/en-us/face-api), get the subscription key.
- Setup DynamoDB as echo would use.
- Setup Slack API key, and create channel for demo.

Steps to setup:
---------------
- Install opencv3:
   - brew tap homebrew/science
   - brew install opencv3 --with-contrib --with-python3
   - ln -s path_to_opencv_python_library path_to_python_site_package_with_library_name

| Example of path_to_opencv_python_library:
| /usr/local/Cellar/opencv3/3.1.0_3/lib/python3.5/site-packages/cv2.cpython-35m-darwin.so
| Example of path_to_python_site_package_with_library_name:
| /Users/username/.virtualenvs/virturlenvname/lib/python3.x/site-packages/cv2.cpython-35m-darwin.so

- Install python requirements:
   - pip install -r requirements.txt

| The requirements in the requirements.txt is far more than needed, please clean the requirements.txt if you have a chance.

Configuration:
--------------
In app.config, fill in the configuration details. You can still run it without slack integration, but please comment out line 36 and line 71 in ochestrator.py.

Run:
----
- python ochestrator.py

| This process will kept running, you can use nohup to free out the terminal, but if doing so please remember to kill the process when no longer needed.

- python HackDemo/manage.py runserver port_you_provided(e.g. 8080)

| This will spin up the web server.

- Open browser, open localhost:port(e.g. 127.0.0.1:8080).
