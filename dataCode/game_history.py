import pandas as pd
import json

champion_file_path = "../data/champions/champions.json"
with open(champion_file_path, 'r') as file:
    champion_file = json.load(file)

champions_name = []
for champion_info in champion_file['data'].items():
    champion_id = champion_info[1]['id']
    champions_name.append(champion_id.lower())


champion_win_rate_df = pd.DataFrame(index=champions_name, columns=["total"]+champions_name)

# win, pick, win_rate(win/pick), pick_rate(pick/num_of_games)
champion_win_rate_df = champion_win_rate_df.applymap(lambda x: [0, 0, 0, 0]) #let all data grid be [0,0,0,0]

# diff position use diff win_rate table
top_champion_win_rate_df = champion_win_rate_df.copy()
jungle_champion_win_rate_df = champion_win_rate_df.copy()
mid_champion_win_rate_df = champion_win_rate_df.copy()
adc_champion_win_rate_df = champion_win_rate_df.copy()
support_champion_win_rate_df = champion_win_rate_df.copy()

top_game_num, jungle_game_num, mid_game_num, adc_game_num, support_game_num = 0, 0, 0, 0, 0

game_history_file_path = "../data/game_history/classic_game_history.csv"
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



output_file_path = 'champion_win_rate.csv'  # 您可以更改路径和文件名
mid_champion_win_rate_df.to_csv(output_file_path, index=True)

