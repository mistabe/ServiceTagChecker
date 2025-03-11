"""
Parses current service tags from MS and informs the user
where in the service tags the IP address exists
"""

#!/usr/bin/env python

import json
import sys
import ipaddress
from datetime import datetime


def jsonfiledate():
    """
    Gets human readable date time of the Service Tags
    JSON file to be displayed on parsing.
    """

    # Your input string
    filename = "ServiceTags_Public_20250203.json"

    # Extract the date part (assuming the date is always in the same position)
    date_str = filename.split("_")[2].split(".")[0]

    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y%m%d")

    # Format it into a human-friendly format
    human_readable_date = date_obj.strftime("%B %d, %Y")  # Example: February 03, 2025

    # Display the result
    print("Service Tags published on:", human_readable_date)


def loadjson():
    """
    Loads Service Tags JSON file from filesystem
    """
    st_file = "ServiceTags_Public_20250203.json"

    with open(st_file, mode="r", encoding="us-ascii") as file:
        output = json.load(file)
    return output


def validate_ipaddress(address):
    """
    Checks if the input provided is even a valid
    IP address
    """
    try:
        ipaddress.ip_address(address)
        print("The address", address, "is valid")
    except ValueError:
        print("The address", address, "is invalid")
        sys.exit(1)


def is_in_prefix(address_to_check, addressprefix):
    """
    Checks if IP address provided is in any Service Tags
    """
    if ipaddress.ip_address(address_to_check) in ipaddress.ip_network(
        addressprefix
    ):
        print("Present in prefix:", addressprefix, end=" ")
        return address_to_check


def resolve_ip(flask_query):
    """
    Takes input from the Flask app and returns a list
    """
    validate_ipaddress(flask_query)
    jsonfiledate()
    servicetags = loadjson()
    matches = []
    for tag in servicetags["values"]:
        # print(tag["properties"])
        for addressprefix in tag["properties"]["addressPrefixes"]:
            if is_in_prefix(flask_query, addressprefix):
                hit = (f"in the ServiceTag:", tag["name"])
                hit = str(hit)
                matches.extend(hit)
    return matches


def main():
    """
    Main application
    """
    userinput = str(input("Please enter the IP address to be queried: "))
    validate_ipaddress(userinput)
    jsonfiledate()
    servicetags = loadjson()
    # matches = []
    for tag in servicetags["values"]:
        # print(tag["properties"])
        for addressprefix in tag["properties"]["addressPrefixes"]:
            if is_in_prefix(userinput, addressprefix):
                print("in the ServiceTag:", tag["name"])


# Could do with a positive negative if there's no results found
# Defintely need a dynamic retrieval of tags if the current JSON file is > 6 days old

if __name__ == "__main__":
    main()
