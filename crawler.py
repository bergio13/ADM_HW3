import requests
from bs4 import BeautifulSoup
import time
import os

def get_master_urls(pages, url):
    """Get the URLs of all the master's degree courses from the FindAMasters website. 
    The function takes two arguments: the number of pages to scrape and the base URL.
    """
    # Create an empty list to store the master's degree URLs
    master_urls = []

    # Loop through all the pages
    for page_num in range(1, pages + 1):
        page_url = url + str(page_num)

        # Try to access the page and raise an exception if the request fails
        try:
            result = requests.get(page_url)
            # Check for status code and raise exception if not 200
            result.raise_for_status()

            # Parse the HTML content of the page
            soup = BeautifulSoup(result.text, 'html.parser')

            # Find all the links to master's degree courses with the class 'courseLink'
            course_links = soup.find_all('a', class_='courseLink')

            # For each link, extract the 'href' attribute and append it to the master_urls list
            for link in course_links:
                master_urls.append(link['href'])
            
            # Sleep for 1 second to avoid overloading the server
            time.sleep(1)

        # Catch any exceptions and print the error message
        except requests.RequestException as e:
            print(f"Error accessing page {page_num}: {e}")

    return master_urls


def save_text(file_path, data):
    """Save a list of URLs to a text file.

    Args:
        file_path (str): The path to the file to be saved.
        data (list): The data to be saved to the file.
    """
    with open(file_path, 'w') as file:
        # Loop through the list of URLs and write each one to a new line
        for item in data:
            file.write("%s\n" % item)

# Read the URLs from a text file
def read_master_urls(path):
    with open(path, 'r') as file:
        master_urls = [line.strip() for line in file.readlines()]
    return master_urls
            


def download_html_pages(master_urls, output_folder, pages_per_folder=15, start_index=1):
    """Download the HTML pages for each master's degree course and save them to a folder. 

    Args:
        master_urls (list): A list of URLs for the master's degree courses.
        output_folder (str): The path to the folder where the HTML pages will be saved.
        pages_per_folder (int): Defaults to 15. The number of HTML pages to save in each folder.
        start_index (int): Defaults to 1. The index from which to start downloading the HTML pages.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through the master_urls list starting from the start_index
    for i, master_url in enumerate(master_urls[start_index - 1:], start=start_index):
        # Try to access the page and raise an exception if the request fails
        try:
            master_url = "https://www.findamasters.com" + master_url
            response = requests.get(master_url)
            # Check for status code and raise exception if not 200
            response.raise_for_status()

            # Calculate the folder index based on the number of html pages per folder
            page_index = (i - 1) // pages_per_folder + 1

            # Create a new folder for each set of pages
            page_folder = os.path.join(output_folder, f"page_{page_index}")
            os.makedirs(page_folder, exist_ok=True)

            # Save HTML content to a file within the page folder
            file_path = os.path.join(page_folder, f"master_{i % pages_per_folder or pages_per_folder}.html")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)

            # Introduce a short delay to avoid overloading the server
            time.sleep(1)
        
        # Catch any exceptions and print the error message
        except requests.RequestException as e:
            print(f"Error downloading page {i}: {e}")
        
        # Introduce a short delay even in case of an exception
        time.sleep(1)

if __name__ == "__main__":
    url = "https://www.findamasters.com/masters-degrees/msc-degrees/?PG="
    #master_urls = get_master_urls(pages=400, url=url)
    #save_text("master_urls.txt", master_urls)
    master_urls = read_master_urls("master_urls.txt")
    download_html_pages(master_urls, output_folder="master_pages", start_index=4404)
