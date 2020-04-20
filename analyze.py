#! usr/bin/env python3
'''
Bring everything together - combine the cases, deaths stats with briefing sentiment values.
See if there's any meaningful relationship(s) between the cases, deaths and sentiment values from the briefings.
Probably not though.
'''
import pandas as pd
from datetime import datetime
from covid_stats import get_stats
from polarities import get_polarities
import matplotlib.pyplot as plt
import seaborn as sns

'''
Function to combine the pulled covid and briefing information
Returns a new dataFrame from two input dataFrames passed in via an array
'''
def combine_data(mixed_data):
    temp = mixed_data

    # Combines the two dataframes with data in chronological order
    for i, df in enumerate(temp):
        s = temp[i].copy()
        cols = s.columns.tolist()
        cols[0] = 'Date'
        s.columns = cols
        s['Date'] = pd.to_datetime(s['Date'])
        s.set_index('Date', inplace=True)
        temp[i] = s

    return pd.concat(temp, axis=1).reset_index()


'''
Play around with the data
'''
if __name__ == '__main__':
    data = combine_data([get_stats(), get_polarities()])
    data['Average Polarity'] = data[['Vader Polarity', 'TextBlob Polarity']].mean(axis=1)
    data['Delta Cases'] = round(data['Cases'].pct_change(), 2)
    data['Delta Polarity'] = round(data['Average Polarity'].pct_change(), 2)

    print(data)

    plt.figure(figsize=(10,7))
    ax = sns.regplot(x='Delta Cases', y='Delta Polarity', data=data)
    ax.grid(True)
    ax.set_title('Effect of Change in COVID-19 Cases to Polarity of Daily Briefing Speech Polarity')
    ax.set_ylabel('% Change - Polarity Score')
    ax.set_xlabel('% Change - Confirmed Cases')
    plt.show()

    '''
    Regression line is pretty much horizontal, meaning there is no relationship between % change in confirmed COVID cases...
    ...and the % change in the polarity of speeches from the briefings.
    '''
