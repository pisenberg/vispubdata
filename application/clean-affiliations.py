import pandas as pd
import re

postfix = '-journals'
data = pd.read_csv("../vispubdata-update/results/DedupedAuthors-Papers-Position-Affiliation"+postfix+".csv", keep_default_na=False)
affiliation_map = pd.read_csv('affiliation-country-alias.csv')
affiliation_map['Affiliation'] = affiliation_map['Affiliation'].str.lower()

# List of known countries to match (extend this list as needed)
known_countries = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda',
    'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
    'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
    'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei',
    'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon',
    'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia',
    'Comoros', 'Congo (Congo-Brazzaville)', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus',
    'Czech Republic', 'Democratic Republic of the Congo', 'Denmark', 'Djibouti',
    'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
    'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji',
    'Finland', 'France', 'Gabon', 'Gambia', 'Germany', 'Ghana', 'Greece',
    'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti',
    'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq',
    'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan',
    'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia',
    'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
    'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
    'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova',
    'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar (Burma)',
    'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger',
    'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan',
    'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru',
    'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda',
    'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
    'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal',
    'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia',
    'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan',
    'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria',
    'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga',
    'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda',
    'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay',
    'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen',
    'Zambia', 'Zimbabwe', 'USA','UK','U.K.','England','Scotland'   # Add "USA" as a synonym. georgia had to be removed to "university of georgia" and "Georgia Institute of Technology"
]

# Function to extract country from affiliation
def extract_country(affiliation):
    for country in known_countries:
        affiliation = affiliation.lower()
        country = country.lower()
        if re.search(rf'\b{re.escape(country)}\b', affiliation):
           if (country == "united kingdom"): return "UK"
           elif (country == "united states"): return "USA"
           elif (country == "usa"): return "USA"
           elif (country == "u.k."): return "UK"
           elif (country == 'uk'): return 'UK'
           elif (country == 'scotland'): return 'UK'
           elif (country == 'england'): return 'UK'
           return country.title()
        
    # Fallback to lookup table
    affiliation_lower = affiliation.lower()
    for i, row in affiliation_map.iterrows():
        if row['Affiliation'] in affiliation_lower:
            return row['Country']
    
    return ''  # Default if no country matched

# Apply the function to the DataFrame
data['Country'] = data['Affiliation'].apply(extract_country)

print(data)

unknown_rows = data[data["Country"] == ""]

# Print the entire rows
data.to_csv("results-affiliation/DedupedAuthors-Papers-Position-Affiliation-Country"+postfix+".csv",index=False)

#Check in this file to see if you need to add any affiliations to the "affiliation-country-alias.csv" file
unknown_rows.to_csv("results-affiliation/Affiliation-Countries-Unknowns"+postfix+".csv",index=False)