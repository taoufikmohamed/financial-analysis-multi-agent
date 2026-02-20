# Run this quick Python snippet to find your report:
import os
import glob

reports = glob.glob("./generated_reports/*.pdf")
if reports:
    print(f"Found report: {os.path.abspath(reports[-1])}")
else:
    print("Check .html or .txt files instead:")
    print(glob.glob("./generated_reports/*.*"))