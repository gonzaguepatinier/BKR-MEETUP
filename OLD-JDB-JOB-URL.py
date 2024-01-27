# 
# Testing parsing URL
# 

from urllib.parse import urlparse, urlencode, parse_qs, urlunparse


URL = "https://th.jobsdb.com/th/en/job/senior-devops-engineer-300003002983819?token=0~f827f396-d585-4114-8616-2d004c900537&sectionRank=32&jobId=jobsdb-th-job-300003002983819"

parsed_url = urlparse(URL)

# Access different components of the URL
scheme = parsed_url.scheme
netloc = parsed_url.netloc
path = parsed_url.path
query = parsed_url.query
fragment = parsed_url.fragment

print("Scheme:", scheme)
print("Netloc:", netloc)
print("Path:", path)
print("Query:", query)
print("Fragment:", fragment)

# Parse query string into a dictionary
query_params = parse_qs(parsed_url.query)
print("Query Parameters:", query_params)

# Modify and rebuild the URL
# modified_url = urlunparse(("https", "www.updated-example.com", "/new-path", "", "param1=new_value&param3=new_param", ""))
modified_url = urlunparse((scheme, netloc, path, "", "",""))
print("Modified URL:", modified_url)

print ("-----")
job_Id = query_params['jobId']
print("Job ID :" + job_Id[0])
print("Modified URL:", modified_url)
