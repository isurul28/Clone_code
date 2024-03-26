#!/usr/bin/env python3

import os
import shutil
import zipfile
import requests

def extract_zip(zip_file, extract_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    return os.path.splitext(os.path.basename(zip_file))[0]

def download_jdbc_driver(database):
    drivers = {
        "mysql": "https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.27/mysql-connector-java-8.0.27.jar",
        "postgresql": "https://repo1.maven.org/maven2/org/postgresql/postgresql/42.3.3/postgresql-42.3.3.jar",
        # Add more database drivers as needed
    }
    driver_url = drivers.get(database.lower())
    if driver_url:
        response = requests.get(driver_url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to download JDBC driver for {database}")
            return None
    else:
        print(f"JDBC driver for {database} is not supported")
        return None

def add_datasource_to_toml(clone_dir, id, url, username, password, driver, max_active=50, max_wait=60000, test_on_borrow=True):
    toml_file = os.path.join(clone_dir, 'conf', 'deployment.toml')
    with open(toml_file, 'a') as f:
        f.write("[[datasource]]\n")
        f.write(f"id = \"{id}\"\n")
        f.write(f"url = \"{url}\"\n")
        f.write(f"username = \"{username}\"\n")
        f.write(f"password = \"{password}\"\n")
        f.write(f"driver = \"{driver}\"\n")
        f.write(f"pool_options.maxActive = {max_active}\n")
        f.write(f"pool_options.maxWait = {max_wait}\n")
        f.write(f"pool_options.testOnBorrow = {str(test_on_borrow).lower()}\n\n")

def create_folder_clones(zip_file, cloning_number, database_info):
    # Check if the zip file exists
    if not os.path.isfile(zip_file):
        print(f"Error: File '{zip_file}' does not exist!")
        return

    # Check if cloning_number is a positive integer
    try:
        cloning_number = int(cloning_number)
        if cloning_number <= 0:
            raise ValueError
    except ValueError:
        print("Error: Cloning number must be a positive integer!")
        return

    # Extract the zip file
    extracted_folder = extract_zip(zip_file, '.')

    # Get the directory where the zip file is located
    zip_dir = os.path.dirname(os.path.abspath(zip_file))

    # Download JDBC driver
    jdbc_driver = download_jdbc_driver(database_info['driver'])
    if jdbc_driver is None:
        return

    # Create clones
    for i in range(1, cloning_number + 1):
        clone_folder = os.path.join(zip_dir, f"{extracted_folder}_clone_{i}")
        shutil.copytree(extracted_folder, clone_folder)
        lib_dir = os.path.join(clone_folder, 'lib')
        os.makedirs(lib_dir, exist_ok=True)
        # Save JDBC driver to lib directory
        driver_path = os.path.join(lib_dir, f"{database_info['driver'].lower()}-jdbc-driver.jar")
        with open(driver_path, 'wb') as driver_file:
            driver_file.write(jdbc_driver)
        print(f"Clone {i} created: {clone_folder}")

        # Add datasource to deployment.toml
        add_datasource_to_toml(clone_folder, **database_info)


    # Debugging: Print the extracted folder path before deleting
    print(f"Extracted folder path: {extracted_folder}")

    # Delete the extracted folder
    shutil.rmtree(extracted_folder)

if __name__ == "__main__":
    # Prompt the user for zip file name, cloning number, and database information
    zip_file = input("Enter zip file name: ")
    cloning_number = input("Enter cloning number: ")

    print("Enter details for the Database WSO2_COORDINATION_DB:")
    db_type = input("Enter database type (e.g., MySQL, PostgreSQL): ")
    db_id = input("Enter datasource id (default: WSO2_COORDINATION_DB): ")
    db_url = input("Enter datasource URL: ")
    db_username = input("Enter datasource username: ")
    db_password = input("Enter datasource password: ")
    db_max_active = input("Enter max active connections (default 50): ")
    db_max_active = int(db_max_active) if db_max_active else 50
    db_max_wait = input("Enter max wait time (default 60000): ")
    db_max_wait = int(db_max_wait) if db_max_wait else 60000
    db_test_on_borrow = input("Test on borrow (default true): ").lower()
    db_test_on_borrow = db_test_on_borrow == 'true'

    print("Enter details for the Database WSO2CarbonDB:")
    db_type2 = input("Enter database type (e.g., MySQL, PostgreSQL): ")
    db_id2 = input("Enter datasource id (default: WSO2CarbonDB): ")
    db_url2 = input("Enter datasource URL: ")
    db_username2 = input("Enter datasource username: ")
    db_password2 = input("Enter datasource password: ")
    db_max_active2 = input("Enter max active connections (default 50): ")
    db_max_active2 = int(db_max_active) if db_max_active else 50
    db_max_wait2 = input("Enter max wait time (default 60000): ")
    db_max_wait2 = int(db_max_wait) if db_max_wait else 60000
    db_test_on_borrow2 = input("Test on borrow (default true): ").lower()
    db_test_on_borrow2 = db_test_on_borrow == 'true'

    database_info = {
        'id': db_id,
        'url': db_url,
        'username': db_username,
        'password': db_password,
        'driver': db_type.lower(),
        'max_active': db_max_active,
        'max_wait': db_max_wait,
        'test_on_borrow': db_test_on_borrow
    }

    database_info2 = {
        'id': db_id2,
        'url': db_url2,
        'username': db_username2,
        'password': db_password2,
        'driver': db_type2.lower(),
        'max_active': db_max_active2,
        'max_wait': db_max_wait2,
        'test_on_borrow': db_test_on_borrow2
    }

    create_folder_clones(zip_file, cloning_number, database_info)
