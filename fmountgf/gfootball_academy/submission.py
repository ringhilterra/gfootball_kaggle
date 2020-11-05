from math import sqrt, atan2, pi
from kaggle_environments.envs.football.helpers import *

def angle(src, tgt):
    xdir = tgt[0] - src[0]
    ydir = tgt[1] - src[1]
    theta = round(atan2(xdir, -ydir) * 180 / pi, 2)
    while theta < 0:
        theta += 360
    return theta


def direction(src, tgt):
    theta = angle(src, tgt)

    if theta >= 360 - 22.5 or theta <= 0 + 22.5:
        return Action.Top
    if 45 - 22.5 <= theta <= 45 + 22.5:
        return Action.TopRight
    if 90 - 22.5 <= theta <= 90 + 22.5:
        return Action.Right
    if 135 - 22.5 <= theta <= 135 + 22.5:
        return Action.BottomRight
    if 180 - 22.5 <= theta <= 180 + 22.5:
        return Action.Bottom
    if 225 - 22.5 <= theta <= 225 + 22.5:
        return Action.BottomLeft
    if 270 - 22.5 <= theta <= 270 + 22.5:
        return Action.Left
    return Action.TopLeft

@human_readable_agent
def agent(obs):
    goal_pos = [1, 0]
    ball_pos = obs["ball"]
    
    player_pos = obs["left_team"][obs["active"]]
    player_x, player_y = player_pos
    
    ball_owned = (obs["ball_owned_team"] == 0 and 
                  obs["ball_owned_player"] == obs["active"])

    def shot(shot_dir):
        if shot_dir not in obs["sticky_actions"]:
            return shot_dir
        return Action.Shot
    
    def high_pass(pass_dir):
        if pass_dir not in obs["sticky_actions"]:
            return pass_dir
        return Action.HighPass   
    
    if  player_x < 0.6:
        if Action.Sprint not in obs['sticky_actions']:
            return Action.Sprint
    else:
        if Action.Sprint in obs['sticky_actions'] and ball_owned:
            return Action.ReleaseSprint
    
    if ball_owned:
        goal_dir = direction(player_pos, goal_pos)
        if player_x < -0.6:
            return shot(goal_dir)
        if player_x < -0.4:
            return high_pass(goal_dir)
        if player_x > 0.6:
            return shot(goal_dir)
        if player_x > 0.4 and abs(player_y) < 0.2:
            return shot(goal_dir)
        return goal_dir
        
    return direction(player_pos, ball_pos)
