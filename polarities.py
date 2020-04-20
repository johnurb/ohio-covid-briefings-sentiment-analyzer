#! usr/bin/env python3
'''
Extract some sentiment information from the pre-processed summary text files
'''
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd
from datetime import datetime

'''
Function to iterate over all of the cleaned text files and compile extracted sentiment information from each one
Returns a dataFrame of the sentiment data
'''
def get_polarities():
    '''
    Setup folder to iterate through. Initialize dataFrame and vader analyzer
    '''
    cleaned_texts_directory = 'cleaned-submissions'
    cleaned_texts = sorted(os.listdir(cleaned_texts_directory))
    results = pd.DataFrame(columns = ['Date', 'Vader Polarity', 'TextBlob Polarity'])
    analyzer = SentimentIntensityAnalyzer()

    # iterate through the preprocessed text files
    for text in cleaned_texts:
        filepath = os.path.join(cleaned_texts_directory, text)
        with open(filepath, 'r') as fin:
            text_content = fin.readlines()

        '''
        Initialize sum variables to later get the averages
        Get the Vader and textBlob sentiment scores
        Get the date of each file being looked at
        Calculate the averages and everything to the master dataFrame
        '''
        vader_score_sum, blob_score_sum = 0, 0
        for sentence in text_content:
            vader_score_sum += analyzer.polarity_scores(sentence.strip())['compound']
            blob_score_sum += TextBlob(sentence.strip()).sentiment[0]
        average_vader_score = round(vader_score_sum / len(text), 2)
        average_blob_score = round(blob_score_sum / len(text), 2)

        date = datetime.strptime(text[:8], '%y-%m-%d').date()
        temp_df = pd.DataFrame([[date, average_vader_score, average_blob_score]], columns=['Date', 'Vader Polarity', 'TextBlob Polarity'])
        results = results.append(temp_df, ignore_index=True)

    return results

if __name__ == '__main__':
    print(get_polarities())
