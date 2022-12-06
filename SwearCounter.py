import glob, os
import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import matplotlib
import scipy

def main():
    with open('swear_words.txt') as f:
        swear_words = f.readlines()
    for i in range(len(swear_words)):
        line = swear_words[i]
        comma = line.index(',')
        swear_words[i] = (line[:comma], line[comma+1:-1])

    table = pd.DataFrame(columns=['Filename', 'Views', 'Likes', 'Duration',
                                  'Gender', 'Religious', 'Sex', 'Excrement', 'Slur', 'Censored',
                                  'Freq', 'Like/View'])

    directory = 'Video Transcripts/'
    list = os.listdir(directory)
    for file in list:
        if '.txt' not in file:
            continue

        with open(directory+file) as f:
            lines = f.readlines()
            info = lines[0][:-1].split(',')
            info.insert(0,file)

            t = info[3]
            colon = t.index(':')
            info[3] = int(t[:colon])*60+int(t[colon+1:])

            transcript = (''.join(lines[1:])).lower()
            for s in ['"', '-', ',', '.', ':', ';', '?', '\n', '!']:
                transcript = transcript.replace(s, ' ')

            count = [0,0,0,0]
            sum = 0

            censored = transcript.count('bleep')
            sum += censored
            for word in swear_words:
                type = word[1].lower()
                word = ' ' + word[0].lower() + ' '

                types = ['holy', 'sex', 'excrement', 'slur']

                num = transcript.count(word)
                count[types.index(type)] += num
                sum += num

            freq = sum/info[3]*60 #convert to swearing/minute
            likeview_ratio = int(info[2])/int(info[1])
            table.loc[len(table)]=(info+count+[censored, freq, likeview_ratio])

    for type in ['Religious', 'Sex', 'Excrement', 'Slur']:
        def calc_freq(row):
            return int(row[type])/row['Duration']*60
        table[type + ' Freq'] = table.apply(lambda row:calc_freq(row), axis=1)
        print(type, table[type+' Freq'].mean())
    print('All', table['Freq'].mean())



    '''
    plt.rcParams['text.usetex'] = True
    fig, ax = plt.subplots(1)
    matplotlib.rc('font', family='serif')
    matplotlib.rc('font', serif='CMS')

    plotting = 'Freq'
    x = table[plotting]; y = table['Like/View']

    a, b, r, p_value, std_err = scipy.stats.linregress(x, y)
    a, b = np.polyfit(x, y, 1)
    plt.plot(x, a*x+b, color='grey')
    ax.scatter(x,y, marker='x',color='black')
    plt.text(ax.get_xlim()[1]*0.7, ax.get_ylim()[0]*1.1, '$y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x$', size=14)
    plt.text(ax.get_xlim()[1]*0.82, ax.get_ylim()[0]*1.3,'$R^2 = ' + '{:.2f}'.format(r)+ '$', size=14 )
    ax.set_xlabel('Swear word frequency (words/min)', fontsize=14)
    ax.set_ylabel('Like to view ratio', fontsize=14)

    plt.show()
    '''



if __name__ == '__main__':
  main()
