#! usr/bin/env python3
'''
Reddit user has been sharing summaries of the briefings held by Ohio Governor DeWine.
Pull down all of the summaries from his Reddit post history and save them as text files to be worked with
'''
import os
import praw
import re
import datetime

'''
Function uses a RegEx to clean the raw text data for output to saved text file
Returns tuple of the cleaned title and text contents
'''
def get_title_and_text(submission):
    return (re.sub(r'[^a-z0-9-!.?]', '', submission.title.lower().replace('/', '-').strip()),
            re.sub(r'[^a-z0-9-!.? \n]', '', submission.selftext.lower().replace('/', '-')))

'''
Function to pull the date from a PRAW submission object
Returns a string representing the date of the post
'''
def get_date(submission):
	return str(datetime.datetime.fromtimestamp(submission.created)).split()[0]

'''
Function to save the processed text contents of a Reddit post to a text file for later use
'''
def save_submission(submission):
    output_directory = "submission-texts"
    try:
        os.mkdir(output_directory)
    except Exception:
        pass

    output_title, output_text = get_title_and_text(submission)
    output_filename = f'{output_title}-{get_date(submission)}.txt'
    output_path = os.path.join(output_directory, output_filename)
    with open(output_path, 'w') as fout:
        fout.write(output_text)

'''
Function to query Reddit using PRAW to get the briefing summaries posted by specific user
'''
def query_reddit():
    '''
    Initialize PRAW
    '''
    credentials_file = "creds.txt"
    with open(credentials_file) as fin:
        client_id, client_secret = fin.readlines()

    client_id = client_id.split(",")[1].strip()
    client_secret = client_secret.split(",")[1].strip()
    user_agent = "get-briefings"

    reddit = praw.Reddit(client_id=client_id, \
                         client_secret=client_secret, \
                         user_agent=user_agent)

    '''
    Pull down the posts from specific Reddit user
    Iterate over his submitted posts and save the desired posts as text files
    '''
    user = reddit.redditor('PeaceIsSoftcoreWar')
    comments = user.submissions.new(limit=None)
    saved_dates = []
    for comment in comments:
        submission = reddit.submission(id=comment)
        submission_date = get_date(submission)
        if 'sum' in submission.title.lower() and submission_date not in saved_dates:
            save_submission(submission)
            saved_dates.append(submission_date)
        else:
            pass

if __name__ == "__main__":
    query_reddit()
