This folder has the following files:

1) UnderstandingFlightDelays.pdf : This is my final project report. All the work has been encompassed in this document and care has been taken to properly format the document.

2) MergingDatasetFlights.ipynb : This is a google collab notebook containing code to combine monthly airport data into a single csv, importing weather data, combining it with our airport dataset, training baseline and other models, plotting some graphs about interesting findings, etc. This was mainly used to test the executability and correctness of my code. This is not the main project code.

3) Weather-processing.ipynb : This file includes the steps for preprocessing weather dataset and also includes some interesting findings and analysis of the dataset.

4) combined.ipynb : This file includes the steps for preprocessing the flight delays dataset and also includes some interesting findings and analysis of the dataset.

5) project4 : This is the main folder containing the Django application. This folder contains various subfolders and python files required to create and run a Django application. The backend specific code can be found in project4\network\views.py. The front end HTML files can be found in project4\network\templates\network. Since this is a Django application, the steps to run the project are as follows:

Steps to run the application:

1) Open a cmd terminal and take it to the project4 directory.

2) Over here, run the command "python manage.py makemigrations". It is not a necessary step but rather a precautionary good practise to find any changes in the database schema since the last run. However it is mandatory to run for a first time usage in any machine.

3) After successfully running the above command, run the command "python manage.py migrate". It is not a necessary step but rather a precautionary good practise to make changes in the database schema since the last run. However it is mandatory to run for a first time usage in any machine.

4) Finally, run the command "python manage.py runserver"

5) The above command would provide you with an IP address (most likely: http://127.0.0.1:8000/)

6) Open Google Chrome or any suitable browser and copy paste the IP address, the tool will start running.

7) The tool may require to register or sign in before it allows usage of functionalities. Please register as a user and it will automatically log in. This functionality of log in and register has been provided due to a specific reason (mentioned in future works section of the "UnderstandingFlightDelays.pdf" report)