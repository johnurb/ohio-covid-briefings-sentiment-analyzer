#! usr/bin/env python3
'''
Process the extracted Reddit summaries of the briefings
'''
import os
import re

'''
Function to clean up the scraped briefing text files for later use in extracting sentiment values
'''
def process_files():
    '''
    Set the directories to work with and iterate over the saved text files and output processed files
    '''
    directory = 'submission-texts'
    output_directory = 'cleaned-submissions'
    try:
        os.mkdir(output_directory)
    except Exception:
        pass
    briefings = os.listdir(directory)
    for briefing in briefings:
        if briefing == '.DS_Store':
            pass
        else:
            file_name = os.path.join(directory, briefing)
            with open(file_name) as fin:
                file_lines = fin.readlines()

            '''
            Ignore the lines in the briefing summaries up until where the gov.,lt gov., and DoH are speaking
            '''
            reached_content = False
            wanted_lines = []
            for line in file_lines:
                if 'the stream ended' in line:
                    break
                elif reached_content == True: #content from here until the ending marker is what we want to work with for polarity extraction
                    '''Regular expression to pick out lines that are only a notifiation that someone new is speaking
                    3 digits followed by a space then 2 letters - corresponds to a time marker, ex: 315 pm
                    '''
                    if line.strip() == '' or re.match('^\d{3} [a-z]{2} ', line.lstrip()):
                        pass
                    else:
                        wanted_lines.append(line.lstrip())
                else:
                    if 'the governor starts' in line or 'the governor begins' in line
                     or 'the governor started' in line or 'the governor began' in line:
                        reached_content = True

            ''' Output processed text files '''
            cleaned_file_name = f'{briefing[-12:-4]}-cleaned-briefing.txt'
            output_path = os.path.join(output_directory, cleaned_file_name)
            output_text = ' '.join(wanted_lines).strip()
            with open(output_path, 'w') as fout:
                fout.write(' '.join(wanted_lines))

if __name__ == '__main__':
    process_files()
