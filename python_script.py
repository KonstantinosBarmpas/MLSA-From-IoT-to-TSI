################################################################################################################
######                                    IMPORT PACKAGES                                               ########
################################################################################################################

import numpy as np
from numpy import genfromtxt
import os
import csv, json
import asyncio
import nest_asyncio
nest_asyncio.apply()
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json

################################################################################################################
######                                    GLOBAL VARIABLES                                              ########
################################################################################################################

local_data_path = './data'
# Namestrings of the CSV file that the device stores
csv_file_path = './data/data_csv.csv'
# Local Namestring for the generated JSON files
json_file_path = './data/data_csv.json'


################################################################################################################
######                                           FUNCTIONS                                              ########
################################################################################################################

# Function to convert a CSV to JSON
def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = []
     
    # Open a csv reader called DictReader
    with open(csvFilePath) as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
             
            # Assuming a column named 'Time' to
            # be the primary key
            key = rows['Date']
            
            # Change timestamp from 2021-05-19 to 2021-05-19T00:00:00Z format
            dateparts = rows['Date']
            timestamp_string = dateparts+"T00:00:00Z"
            # Remove CSVs Time field
            rows.pop('Date', None)
            
            # Change values to float
            new_rows = {k:v for k, v in rows.items()}
                                    
            # Add the TSI Timeseries Identity and Timestamp
            new_rows['DeviceId'] = rows['Device']
            new_rows['timestamp_tsi'] = timestamp_string
            
            # Turn the temperature from String to Float
            new_rows['Temperature'] = float(new_rows['Temperature'])
                        
            # Create JSON Object
            data.append(new_rows)
    
    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

async def send(json_file_path):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string("<STRING-CONNECTION>",
    eventhub_name="<EVENT-HUB-NAME>")
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch
        with open(json_file_path) as f:
            data = json.load(f)
        body_part = json.dumps(data)
        os.remove(json_file_path)
        event_data_batch.add(EventData(body_part))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

################################################################################################################
######                                    MAIN FUNCTION                                                 ########
################################################################################################################
    
def main():
        
    # Create JSON files
    make_json(csv_file_path, json_file_path)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send(json_file_path))
            
################################################################################################################
######                                    RUN MAIN FUNCTION                                             ########
################################################################################################################

main()
