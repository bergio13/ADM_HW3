import os
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Extract course name from the HTML page
def extract_course_name(page_soup):
    course_name_h1 = page_soup.find('h1', class_='course-header__course-title')
    if course_name_h1:
        return course_name_h1.get_text(strip=True)
    else:
        return ''

# Extract university name from the HTML page
def extract_university_name(page_soup):
    university_name_a = page_soup.find('a', class_='course-header__institution')
    if university_name_a:
        return university_name_a.get_text(strip=True)
    else:
        return ''

# Extract faculty name from the HTML page   
def extract_faculty_name(page_soup):
    faculty_name_a = page_soup.find('a', class_='course-header__department')
    if faculty_name_a:
        return faculty_name_a.get_text(strip=True)
    else:
        return ''

# Extract time information from the HTML page   
def extract_full_time_info(page_soup):
    full_time_info_a = page_soup.find('a', class_='inheritFont concealLink text-decoration-none text-gray-600')
    if full_time_info_a:
        return full_time_info_a.get_text(strip=True)
    else:
        return ''

# Extract course description from the HTML page
def extract_course_description(page_soup):
        description_div = page_soup.find('div', class_='course-sections__description')
        # Check if the element was found
        if description_div:
            # Find the div with id 'Snippet' to extract the course description
            snippet_div = description_div.find('div', id='Snippet')
            # Check if the element was found
            if snippet_div:
                # Extract and return the text of the div
                return snippet_div.get_text(strip=True)
        else:
            return ''

# Extract course start date from the HTML page      
def extract_course_start_date(page_soup):
    start_date_span = page_soup.find('span', class_='key-info__start-date')

    # Check if the element was found
    if start_date_span:
        # Extract and return the text of the span
        return start_date_span.get_text(strip=True)
    else:
        return ''

# Extract course fees from the HTML page
def extract_course_fees(page_soup):
    fees_div = page_soup.find('div', class_='course-sections__fees')
    if fees_div:
        # Find the p element within the fees_div
        fees_p = fees_div.find('p')
        # Check if the element was found
        if fees_p:
            # Extract and return the text of the p element
            return fees_p.get_text(strip=True)
    else:
        return ''

# Extract course modality from the HTML page   
def exract_course_modality(page_soup):
    modality_span = page_soup.find('span', class_='key-info__qualification')
    if modality_span:
        return modality_span.get_text(strip=True)
    else:
        return ''

# Extract course duration from the HTML page
def exract_course_duration(page_soup):
    duration_span = page_soup.find('span', class_='key-info__duration')
    if duration_span:
        return duration_span.get_text(strip=True)
    else:
        return ''

# Extract course city from the HTML page   
def extract_course_city(page_soup):
    city_link = page_soup.find('a', class_='course-data__city')
    if city_link:
        return city_link.get_text(strip=True)
    else:
        return ''

# Extract course country from the HTML page   
def extract_course_country(page_soup):
    country_link = page_soup.find('a', class_='course-data__country')
    if country_link:
        return country_link.get_text(strip=True)
    else:
        return ''

# Extract course administration from the HTML page
def extract_course_administration(page_soup):
    ad_link = page_soup.find('a', class_='course-data__on-campus')
    if ad_link:
        return ad_link.get_text(strip=True)
    else:
        return ''
    
    
# Extract course information from the HTML page
def extract_course_info(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract desired information from the HTML page using the functions defined above
        course_name = extract_course_name(soup)
        university_name = extract_university_name(soup)
        faculty_name = extract_faculty_name(soup)
        full_time_info = extract_full_time_info(soup)
        description = extract_course_description(soup)
        start_date = extract_course_start_date(soup)
        fees = extract_course_fees(soup)
        modality = exract_course_modality(soup)
        duration = exract_course_duration(soup)
        city = extract_course_city(soup)
        country = extract_course_country(soup)
        administration = extract_course_administration(soup)
        url = soup.find('link', rel='canonical')['href']

        return course_name, university_name, faculty_name, full_time_info, description, start_date, fees, modality, duration, city, country, administration, url
    
    except Exception as e:
        print(f"Error extracting info: {e}")
        return None

# Save course information to a TSV file   
def save_course_info_to_tsv(course_info, output_folder, course_number):
    file_path = os.path.join(output_folder, f"course_{course_number}.tsv")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\t'.join(course_info))

# Process all the HTML files in the master_pages folder
def process_master_pages(master_pages_folder, output_folder):
    course_number = 1

    # Iterate over all the folders in the master_pages folder
    for folder_name in sorted(os.listdir(master_pages_folder)):
        # Get the path of the folder
        folder_path = os.path.join(master_pages_folder, folder_name)

        # Iterate over all the HTML files in the folder
        for html_file_name in sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[1].split('.')[0])):
            try:
                # Get the path of the HTML file
                html_file_path = os.path.join(folder_path, html_file_name)

                # Read the HTML content from the saved file
                with open(html_file_path, 'r', encoding='utf-8') as html_file:
                    html_content = html_file.read()

                # Extract course information
                course_info = extract_course_info(html_content)

                # Save course information to a TSV file
                save_course_info_to_tsv(course_info, output_folder, course_number)
                # Increment the course number
                course_number += 1

            except Exception as e:
                print(f"Error extracting info for {folder_name}/{html_file_name}: {e}")
                
# Read all the TSV files in the course_info folder and return a single dataframe
def read_tsv(file_path, columns):
    # Create an empty list to store the dataframes
    dataframes = []
    # Iterate over all the files in the folder
    for filename in sorted(os.listdir(file_path), key=lambda x: int(x.split('_')[1].split('.')[0])):
        # Check if the file is a TSV file
        if filename.endswith(".tsv"):
            # Read the TSV file using pandas and append it to the list, use CSV reader to avoid errors
            dataframes.append(pd.read_csv(os.path.join(file_path, filename), sep='\t', names=columns, quoting=csv.QUOTE_NONE, encoding='utf-8'))
            
    return pd.concat(dataframes)
                


if __name__ == "__main__":
    process_master_pages(master_pages_folder="master_pages", output_folder="course_info")
    columns = ['courseName', 'universityName', 'facultyName', 'isItFullTime', 'description', 'startDate', 'fees', 'modality', 'duration', 'city', 'country', 'administration', 'url']
    df = read_tsv("course_info", columns=columns)
    df.to_csv('course_info.tsv', sep='\t', index=False)