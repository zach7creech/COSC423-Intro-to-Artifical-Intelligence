"""
Author: Zachery Creech.

This file 'main.py' contains four function definitions for analyzing an applicant's scores.
The body of running code follows the four definitions. A .csv file called 'applicants.csv'
is read in and examined line by line, each line representing one applicant's scores. If an
applicant's scores pass each of the four tests (each function must return True) then
'ACCEPT' is written to a .csv file called 'results.csv'. If the applicant does not pass,
'REJECT' is written instead.
"""
import csv

def analyze_applicant1(scores):
    """
    Given the GPAs of a single applicant, return True if they are qualified.
    
    Qualification: An applicant is qualified if...
    - The average of all their grades is above 85.

    @param scores: a list of GPAs (strings that must be converted to integers)
    @return True if the applicant qualifies
    """
    # accumulate total of all scores
    total = 0
    for score in scores:
        total += int(score)
    # qualifier: average is total / 6
    if total / 6 > 85:
        return True
    else:
        return False

def analyze_applicant2(scores):
    """
    Given the GPAs of a single applicant, return True if they are qualified.
    
    Qualification: An applicant is qualified if...
    - None of their grades are below 65.
    
    @param scores: a list of GPAs (strings that must be converted to integers)
    @return True if the applicant qualifies
    """
    # check every score
    for score in scores:
        # qualifier
        if int(score) < 65:
            return False
    return True

def analyze_applicant3(scores):
    """
    Given the GPAs of a single applicant, return True if they are qualified.
    
    Qualification: An applicant is qualified if...
    - They have at least 4 grades above 85.
    
    @param scores: a list of GPAs (strings that must be converted to integers)
    @return True if the applicant qualifies
    """
    # keep track of how many scores applicant has above 85
    passed = 0
    # check every score
    for score in scores:
        if int(score) > 85:
            passed += 1
    # qualifier
    if passed >= 4:
        return True
    else:
        return False

def analyze_applicant4(scores):
    """
    Given the GPAs of a single applicant, return True if they are qualified.
    
    Qualification: An applicant is qualified if...
    - Their average in their 5 CS courses is above 85 (score indices 0-4).
    
    @param scores: a list of GPAs (strings that must be converted to integers)
    @return True if the applicant qualifies
    """
    # keep track of which score is examined, do not examine 6th score (non-CS GPA)
    index = 0
    # accumulate total of all CS scores
    total = 0
    while index < 5:
        total += int(scores[index])
        index += 1
    # qualifier: average is total / 5
    if total / 5 > 85:
        return True
    else:
        return False

# open applicants.csv for reading
with open('applicants.csv', newline='') as fin:
    # open results.csv for writing
    with open('results.csv', 'w', newline='') as fout:
        # open fin and fout for csv reading and writing respectively
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        # run algorithm on each row, a row being a list of a single applicant's scores
        for row in reader:
            # skip the headers
            if row[0] == 'IntroToCS':
                continue
            # if all functions return True, then the applicant is accepted (write ACCEPT)
            if analyze_applicant1(row) and analyze_applicant2(row) and analyze_applicant3(row) and analyze_applicant4(row):
                writer.writerow(['ACCEPT'])
            # otherwise the applicant is rejected (write REJECT)
            else:
                writer.writerow(['REJECT'])
