#!/usr/bin/env python

import json
import ipaddress


def jsonfiledate():
    from datetime import datetime

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
    st_file = "ServiceTags_Public_20250203.json"

    with open(st_file, mode="r") as file:
        output = json.load(file)
    return output


def validate_ipaddress(address):
    try:
        ipaddress.ip_address(address)
        print("The address", address, "is valid")
    except ValueError:
        print("The address", address, "is invalid")
        exit(1)


def is_in_prefix(address_to_check, servicetag_prefix):
    if ipaddress.ip_address(address_to_check) in ipaddress.ip_network(
        servicetag_prefix
    ):
        print("Present in prefix:", servicetag_prefix, end=" ")
        return address_to_check
    else:
        pass


def main():
    userinput = str(input("Please enter the IP address to be queried: "))
    validate_ipaddress(userinput)
    jsonfiledate()
    servicetags = loadjson()
    matches = []
    for tag in servicetags["values"]:
        # print(tag["properties"])
        for addressprefix in tag["properties"]["addressPrefixes"]:
            if is_in_prefix(userinput, addressprefix):
                print("in the ServiceTag:", tag["name"])


# Could do with a positive negative if there's no results found
# Defintely need a dynamic retrieval of tags if the current JSON file is > 6 days old

if __name__ == "__main__":
    main()
