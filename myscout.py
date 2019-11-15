import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sns.set(style="ticks")

def load_data():
    player_stats = ["short_name","age","height_cm","club","overall","potential","value_eur","wage_eur",
                    "player_positions","preferred_foot","international_reputation","weak_foot",
                    "body_type","release_clause_eur","team_position","loaned_from","joined","contract_valid_until",
                    "nation_position","pace","shooting","passing","dribbling","defending","physic",
                    "player_traits","attacking_crossing","attacking_finishing","attacking_heading_accuracy",
                    "attacking_short_passing","attacking_volleys","skill_dribbling","skill_curve","skill_fk_accuracy",
                    "skill_long_passing","skill_ball_control","movement_acceleration","movement_sprint_speed","movement_agility",
                    "movement_reactions","movement_balance","power_shot_power","power_jumping","power_stamina",
                    "power_strength","power_long_shots","mentality_aggression","mentality_interceptions",
                    "mentality_positioning","mentality_vision","mentality_penalties","mentality_composure","defending_marking",
                    "defending_standing_tackle","defending_sliding_tackle"]
    
    
    
    
    
    complete_player_df = pd.read_csv("players_20.csv",low_memory=False)
    
    
    player_df = complete_player_df[player_stats]
    del complete_player_df
    # Few rows of data
    return player_df

def preprocess_data(data):
    for column in data: 
        data[column]= data[column].astype('str')
    return data
    
def get_positions(df):
    
    positions = df.player_positions.unique()
    pos_liste = []
    for posis in positions:
        posis = posis.split(", ")
        for pos in posis:
            if pos not in pos_liste:
                pos_liste.append(pos)
                
    
    return pos_liste,

def search_player(df):
    pos = "LB"
    max_age = 22 
    min_pot = 85
    min_overall = 70
    
    return df[(df.player_positions == pos) & (df.potential >= min_pot) & (df.overall >= min_overall) & (df.age <= max_age)]

def print_result(df):
    strip_list = ["short_name","age","height_cm","club","overall","potential","value_eur","wage_eur",
                    "player_positions","preferred_foot","release_clause_eur","contract_valid_until","pace","shooting","passing","dribbling","defending","physic"]
    df_strip = df[strip_list]    
    
    df_print = df_strip[["short_name","age","height_cm","club","overall","potential","value_eur","wage_eur",
                    "player_positions","preferred_foot","release_clause_eur","contract_valid_until"]]
    
    print(df.short_name)
    
    count = 1
    for row in df_print.iterrows():
        for entry in row:
            print(entry)
        count += 1
        if count >15 :
            break
     
    df_diagramm = df_strip[["short_name","overall","pace","shooting","passing","dribbling","defending","physic"]]    
    '''
    sns.relplot(x="shooting", y="pace", hue="short_name", 
            sizes=(40, 400), alpha=.5, palette="muted",
            height=6, data=df_diagramm)
    '''        
    df_diagramm.plot(x="short_name", y=["overall","pace","shooting","passing","dribbling","defending","physic"], kind="bar" )     
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

    #for players in df_strip:
        


if __name__=="__main__":
    df = load_data()
    #df_prep = preprocess_data(df.select_dtypes(include='object'))
    #print(df.info(verbose=True))
    
    #positions = get_positions(df)
    #print("Choose from one of the following positions: \n")
    #for w in positions:
    #    print(w)


    df_res = search_player(df)
    
    print_result(df_res)
    
    