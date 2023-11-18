#!/bin/bash

output_file="merged_file.tsv"
msc_file="msc_file.tsv"
# Column names
header="courseName\tuniversityName\tfacultyName\tisItFullTime\tdescription\tstartDate\tfees\tmodality\tduration\tcity\tcountry\tadministration\turl"

echo -e "$header" > "$output_file"

for file in *.tsv; do
    if [ "$file" != "$output_file" ]; then
        cat "$file"
    fi
done >> "$output_file"

echo "Merging complete. Output file: $output_file"

#all msc offering countries
echo -e "$header" > "$msc_file"

grep -i -P '\t.*Msc.*\t' merged_file.tsv >> "$msc_file"

# count country occurences and sort wrt count of countries in descending
awk -F'\t' '{count[$11]++} END {for (country in count) print count[country], country}' msc_file.tsv | sort -nr | head -1 > country_count.txt

echo "Country that offers most Msc degrees: "
cut -f2- -d' ' country_count.txt

awk -F'\t' '{count[$10]++} END {for (city in count) print count[city], city}' msc_file.tsv | sort -nr | head -1 > city_count.txt

echo "City in that country that offers most Msc degrees: "
cut -f2- -d' ' city_count.txt

#How many colleges offer Part-Time education?
echo "How many colleges offer Part-Time education?"
awk -F'\t' '$4 == "Part time"{count[$4]++} END {for (isFulltime in count) print count[isFulltime], isFulltime}' merged_file.tsv

#Print the percentage of courses in Engineering (the word "Engineer" is contained in the course's name).
engcourse="engcourse.tsv"
echo -e "$header" > "$engcourse"
awk -F'\t' '$1 ~ /Engineering/' merged_file.tsv > engcourse.tsv
engcourse_count=$(cut -f1 -d$'\t' engcourse.tsv | sort | uniq | wc -l)
echo "Engineering courses count: $engcourse_count"
totalcourse_count=$(cut -f1 -d$'\t' merged_file.tsv | sort | uniq | wc -l)
echo "Total Courses count: $totalcourse_count"
percentage=$((engcourse_count * 100 / totalcourse_count))
echo "The percentage of courses in Engineering (the word "Engineer" is contained in the course's name): $percentage%"
