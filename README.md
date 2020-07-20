# FIHR_API

This API library was created to retrieve patient data in FHIR format as part of the Philips Healthsuite Hackaton: 

http://www.usa.philips.com/healthcare-about/events-calendar/hackathon

## get_patient_data.py

This script fetches the patient data from the repository. The data has a metadata (Patient data) and observations. The script produces blended records, taking relevant fields from the metadata and adding them to each observation, to produce a file of JSON objects, each corresponding to a blended record

## build_stats.py

This script transforms a file with JSON objects into a CSV file, which can then be more easily visualized with tools such as Tableau.
