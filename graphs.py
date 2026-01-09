import json
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import numpy as np

def review_time_breakdown():
    """Distribution of number of reviews since the game's release """

    SILKSONG_RELEASE_TIME = 1756994400 # in Epoch
    SECONDS_IN_HOUR = 3600

    cats_numeric_days = ['0-24', '24-48', '48-72', '72-96', '96-120', '120-144', '144-168'] # range of hours within a week
    cats_name_days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']

    # range of hours across 10 weeks 
    cats_numeric_weeks = ['0-168', '168-336', '336-504', '504-672', '672-840', '840-1008', '1008-1176', '1176-1344', '1344-1512', '1512-1680', '1680-5000']
    cats_name_weeks = ['Wk 1', 'Wk 2', 'Wk 3', 'Wk 4', 'Wk 5', 'Wk 6', 'Wk 7', 'Wk 8', 'Wk 9', 'Wk 10', 'More']

    x_bar_days = [0] * len(cats_name_days)
    x_bar_weeks = [0] * len(cats_name_weeks)


    try:
        with open('skong', 'r') as f:
            data = json.load(f)
        
        for review in data["reviews"]:
            review_release_time = review["timestamp_created"] # in Epoch
            hours_since_release = (review_release_time - SILKSONG_RELEASE_TIME)/SECONDS_IN_HOUR


            for i, day in enumerate(cats_numeric_days):
                min_, max_ = day.split('-')

                if (hours_since_release > int(min_)) and (hours_since_release <= int(max_)):
                    x_bar_days[i] += 1
                    break
            
            for i, week in enumerate(cats_numeric_weeks):
                min_, max_ = week.split('-')

                if (hours_since_release > int(min_)) and (hours_since_release <= int(max_)):
                    x_bar_weeks[i] += 1
                    break
                
    except Exception as e:
        print(f'Cannot process file. Error occurred: {e}')
        return 1
    
    
    fig, ax = plt.subplots(1, 2) # create two graphs one next to the other
    ax[0].bar(cats_name_days, x_bar_days) # graph of first week
    ax[1].bar(cats_name_weeks, x_bar_weeks, width = 0.5) # graph of first 10 weeks

    ax[0].set_title('First 7 days'); ax[1].set_title('First 10 weeks and beyond')

    fig.suptitle("Number of reviews since game's release")  # overarching title

    plt.show()
    return 0
    
def enjoyment_vs_playtime_graph():
    """Plots a bar graph that compares game recommendation based on the amount of hours of playtime on the game """

    # ranges of hours
    cats = ['0-10' , '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', '100-3000']

    x_arr_pos = [0] * len(cats)
    x_arr_neg = [0] * len(cats)
 
    try:
        with open('skong', 'r') as f:
            data = json.load(f)
        
        for review in data["reviews"]:
            author_recommends = int(review["voted_up"])
            author_playtime = int(review["author"]["playtime_at_review"])/60  #divide by 60 to get number of hours

            index = -1

            for _index, cat in enumerate(cats):
                min_, max_ = cat.split('-')

                if (author_playtime > int(min_)) and (author_playtime <= int(max_)):
                    index = _index
                    break
            
            if index == -1:
                continue

            if author_recommends:
                x_arr_pos[index]+=1
            else:
                x_arr_neg[index]+=1

        
    except Exception as e:
        print(f"Unable to process data file. Error reached: {e}")
        return 1
    
    w, x = 0.4, np.arange(len(cats))
    plt.bar(x - w/2, x_arr_pos, w, label='Recommends')
    plt.bar(x + w/2, x_arr_neg, w, label='Does not recommend')  

    plt.xticks(x, cats)
    plt.ylabel('Number of reviews')
    plt.xlabel('Playtime in hours')
    plt.title('Game recommendation based on playtime')
    plt.legend()
    plt.show()
    return 0
    
def word_analysis(file: str):
    x_pl, y_pl, label = [], [], []
   
    try:
        with open(file, 'r') as f:
                data = json.load(f)
        
        for text in data:
            text_positive_ratio = data[text]["positive"]/data[text]["total"]
            x_pl.append(data[text]["total"])
            y_pl.append(text_positive_ratio)
            label.append(text)
            
    except Exception as e:
        print(f'Error creating graph: {e}')

    df = pd.DataFrame({
        'Number of Reviews': x_pl,
        'Positivity': y_pl,
        'Custom_Label': label
    })

    fig = px.scatter(df, 
                 x="Number of Reviews", 
                 y="Positivity", 
                hover_name="Custom_Label",
                color="Positivity") 

    fig.show()


    return


def main():
    return

if __name__ == "__main__":
    main()
    

