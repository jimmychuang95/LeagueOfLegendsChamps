import pandas as pd
import json

#NOTE: change summoner_name_for_save_path to your summoner name
summoner_name_for_save_path = "Owner"

champion_file_path = "../data/champions/champions.json"
with open(champion_file_path, 'r') as file:
    champion_file = json.load(file)

champions_name = []
for champion_info in champion_file['data'].items():
    champion_id = champion_info[1]['id']
    champions_name.append(champion_id.lower())

champion_win_rate_df = pd.DataFrame(index=champions_name, columns=["total"]+champions_name)

# [0,0,0,0]: win, pick, win_rate(win/pick), pick_rate(pick/num_of_games)
# diff position use diff win_rate table
top_champion_win_rate_df = champion_win_rate_df.copy()
top_champion_win_rate_df = top_champion_win_rate_df.applymap(lambda x: [0, 0, 0, 0]) #let all data grid be [0,0,0,0]
jungle_champion_win_rate_df = champion_win_rate_df.copy()
jungle_champion_win_rate_df = jungle_champion_win_rate_df.applymap(lambda x: [0, 0, 0, 0]) #let all data grid be [0,0,0,0]
mid_champion_win_rate_df = champion_win_rate_df.copy()
mid_champion_win_rate_df = mid_champion_win_rate_df.applymap(lambda x: [0, 0, 0, 0]) #let all data grid be [0,0,0,0]
adc_champion_win_rate_df = champion_win_rate_df.copy()
adc_champion_win_rate_df = adc_champion_win_rate_df.applymap(lambda x: [0, 0, 0, 0]) #let all data grid be [0,0,0,0]
support_champion_win_rate_df = champion_win_rate_df.copy()
support_champion_win_rate_df = support_champion_win_rate_df.applymap(lambda x: [0, 0, 0, 0]) #let all data grid be [0,0,0,0]

top_game_num, jungle_game_num, mid_game_num, adc_game_num, support_game_num = 0, 0, 0, 0, 0

game_history_file_path = "../data/summoner/"+ summoner_name_for_save_path +"/game_history/classic_game_history.csv"
game_history_file_df = pd.read_csv(game_history_file_path)

summoner_teams = game_history_file_df['summoner_team'].to_list()
summoner_positions = game_history_file_df['summoner_position'].to_list()
summoner_champions = game_history_file_df['summoner_champion'].to_list()
summoner_winFlags = game_history_file_df['summoner_winFlag'].to_list()
opponent_champions = game_history_file_df['opponent_champion'].to_list()

def update_win_pick_num(position_champion_win_rate_df, summoner_team, summoner_champion, opponent_champion, summoner_winFlag, num_of_games):
        position_champion_win_rate_df.loc[summoner_champion.lower(), opponent_champion.lower()][1] += 1 # pick+=1
        position_champion_win_rate_df.loc[summoner_champion.lower(), "total"][1] += 1 # pick+=1
        if summoner_winFlag == True: # if win   
            position_champion_win_rate_df.loc[summoner_champion.lower(), opponent_champion.lower()][0] += 1 # win+=1
            position_champion_win_rate_df.loc[summoner_champion.lower(), "total"][0] += 1 # win+=1
        win_rate = position_champion_win_rate_df.loc[summoner_champion.lower(), opponent_champion.lower()][0] / position_champion_win_rate_df.loc[summoner_champion.lower(), opponent_champion.lower()][1] # win_rate = win/pick
        pick_rate = position_champion_win_rate_df.loc[summoner_champion.lower(), opponent_champion.lower()][1] / num_of_games # pick_rate = pick/num_of_games
        position_champion_win_rate_df.loc[summoner_champion.lower(), opponent_champion.lower()][2] = f"{win_rate:.2%}"
        position_champion_win_rate_df.loc[summoner_champion.lower(), opponent_champion.lower()][3] = f"{pick_rate:.2%}"

        total_win_rate = position_champion_win_rate_df.loc[summoner_champion.lower(), "total"][0] / position_champion_win_rate_df.loc[summoner_champion.lower(), "total"][1] # win_rate = win/pick
        total_pick_rate = position_champion_win_rate_df.loc[summoner_champion.lower(), "total"][1] / num_of_games # pick_rate = pick/num_of_games
        position_champion_win_rate_df.loc[summoner_champion.lower(), "total"][2] = f"{total_win_rate:.2%}"
        position_champion_win_rate_df.loc[summoner_champion.lower(), "total"][3] = f"{total_pick_rate:.2%}"

def remove_spec_row_col(target_df, pattern):
    # Drop rows where all values match the pattern
    target_df = target_df.loc[~target_df.isin([pattern]).all(axis=1)]
    # Drop columns where all values match the pattern
    target_df = target_df.loc[:, ~target_df.isin([pattern]).all(axis=0)]
    return target_df

for summoner_team, summoner_position, summoner_champion, summoner_winFlag, opponent_champion in zip(summoner_teams, summoner_positions, summoner_champions, summoner_winFlags, opponent_champions):
    if summoner_position == 'TOP':
        top_game_num += 1
        update_win_pick_num(top_champion_win_rate_df, summoner_team, summoner_champion, opponent_champion, summoner_winFlag, top_game_num)
    elif summoner_position == 'JUNGLE':
        jungle_game_num += 1
        update_win_pick_num(jungle_champion_win_rate_df, summoner_team, summoner_champion, opponent_champion, summoner_winFlag, jungle_game_num)
    elif summoner_position == 'MIDDLE':
        mid_game_num += 1
        update_win_pick_num(mid_champion_win_rate_df, summoner_team, summoner_champion, opponent_champion, summoner_winFlag, mid_game_num)
    elif summoner_position == 'BOTTOM':
        adc_game_num += 1
        update_win_pick_num(adc_champion_win_rate_df, summoner_team, summoner_champion, opponent_champion, summoner_winFlag, adc_game_num)
    elif summoner_position == 'UTILITY':
        support_game_num += 1
        update_win_pick_num(support_champion_win_rate_df, summoner_team, summoner_champion, opponent_champion, summoner_winFlag, support_game_num)


top_champion_win_rate_df = remove_spec_row_col(top_champion_win_rate_df, [0,0,0,0])
jungle_champion_win_rate_df = remove_spec_row_col(jungle_champion_win_rate_df, [0,0,0,0])
mid_champion_win_rate_df = remove_spec_row_col(mid_champion_win_rate_df, [0,0,0,0])
adc_champion_win_rate_df = remove_spec_row_col(adc_champion_win_rate_df, [0,0,0,0])
support_champion_win_rate_df = remove_spec_row_col(support_champion_win_rate_df, [0,0,0,0])

top_champion_win_rate_df.to_csv("../data/summoner/"+ summoner_name_for_save_path +"/summoner_win_pick/top_champion_win_pick.csv", index=True)
jungle_champion_win_rate_df.to_csv("../data/summoner/"+ summoner_name_for_save_path +"/summoner_win_pick/jungle_champion_win_pick.csv", index=True)
mid_champion_win_rate_df.to_csv("../data/summoner/"+ summoner_name_for_save_path +"/summoner_win_pick/mid_champion_win_pick.csv", index=True)
adc_champion_win_rate_df.to_csv("../data/summoner/"+ summoner_name_for_save_path +"/summoner_win_pick/adc_champion_win_pick.csv", index=True)
support_champion_win_rate_df.to_csv("../data/summoner/"+ summoner_name_for_save_path +"/summoner_win_pick/support_champion_win_pick.csv", index=True)
