__author__ = 'yashwanth'
from Tkinter import *
master = Tk()

triangle_size = 0.2
cell_score_min = -10
cell_score_max = 12
Width = 150
(x, y) = (5, 5)
actions = ["up", "down", "left", "right"]
Q = {}
board = Canvas(master, width=x*Width, height=y*Width)
player = (4, 0)
playerHasBlock = False
dropoffCount = 0
score = 0
restart = False
walk_reward = -1
currCost = 0
bank = []
text_offset = 17
walls = [(-1,0)]
specials = [(0,0,"blue",12,4),(0,3,"blue",12,4),(2,2,"blue",12,4),(4,4,"blue",12,4),(0,4,"green",12,0),(3,3,"green",12,0)]
cell_scores = {}
text_objects = {}

def create_triangle(i, j, action):
    if action == actions[0]:
        return (board.create_polygon((i + 0.5 - triangle_size) * Width, (j + triangle_size) * Width,
                                     (i + 0.5 + triangle_size) * Width, (j + triangle_size) * Width,
                                     (i + 0.5) * Width, j * Width,
                                     fill="white", width=1),
                board.create_text((i + 0.5) * Width, j * Width + text_offset, text=str(Width), fill="white"))
    elif action == actions[2]:
        return (board.create_polygon((i + 0.5 - triangle_size) * Width, (j + 1 - triangle_size) * Width,
                                     (i + 0.5 + triangle_size) * Width, (j + 1 - triangle_size) * Width,
                                     (i + 0.5) * Width, (j + 1) * Width,
                                     fill="white", width=1),
                board.create_text((i + 0.5) * Width, (j + 1) * Width - text_offset, text=str(Width), fill="white"))
    elif action == actions[1]:
        return (board.create_polygon((i + triangle_size) * Width, (j + 0.5 - triangle_size) * Width,
                                     (i + triangle_size) * Width, (j + 0.5 + triangle_size) * Width,
                                     i * Width, (j + 0.5) * Width,
                                     fill="white", width=1),
                board.create_text(i * Width + text_offset, (j + 0.5) * Width, text=str(Width), fill="white"))
    elif action == actions[3]:
        return (board.create_polygon((i + 1 - triangle_size) * Width, (j + 0.5 - triangle_size) * Width,
                                     (i + 1 - triangle_size) * Width, (j + 0.5 + triangle_size) * Width,
                                     (i + 1) * Width, (j + 0.5) * Width,
                                     fill="white", width=1),
                board.create_text((i + 1) * Width - text_offset, (j + 0.5) * Width, text=str(Width), fill="white"))


def render_grid():
    global specials, walls, Width, x, y, player, playerHasBlock
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            temp_val = {}
            for action in actions:
                (temp[action], temp_val[action]) = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
            text_objects[(i,j)] = temp_val
    for (i, j, c, w, b) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()


def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    if action == 'left':
        action = 'down'
    elif action == 'down':
        action = 'left'
    triangle = cell_scores[state][action]
    text = text_objects[state][action]

    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)
    board.itemconfigure(text, text = str(format(val, '.2f')), fill="black")


def try_move(dx, dy):

    global player, x, y, score, walk_reward, me, restart, playerHasBlock, dropoffCount, currCost, specials
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy

    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
        score += walk_reward
        currCost += walk_reward
    for (i, j, c, w, b) in specials:
        if new_x == i and new_y == j:
            if c == 'blue' and not playerHasBlock and b > 0:
                score += w + 1
                currCost += w + 1
                playerHasBlock = True
                updateSpecials((i, j, c, w, b),-1)
                updateQ((i,j),'pick',w)
            elif c == 'green' and playerHasBlock and b < 8:
                score += w + 1
                currCost += w + 1
                playerHasBlock = False
                dropoffCount += 1
                updateSpecials((i, j, c, w, b),1)
                updateQ((i, j), 'drop', w)
            # print "Score is: ", score, dropoffCount
            if dropoffCount == 16:
                restart = True
                dropoffCount = 0
                currCost = 0
                bank.append(score)
                print ("Restart")
                specials = [(0, 0, "blue", 12, 4), (0, 3, "blue", 12, 4), (2, 2, "blue", 12, 4), (4, 4, "blue", 12, 4),
                            (0, 4, "green", 12, 0), (3, 3, "green", 12, 0)]

            return


def updateQ(s,a,reward,alpha=0.3):
    global playerHasBlock,Q
    val = playerHasBlock
    if reward == 12:
        val = not val
    q = [Q.get((s, act, val), 0.0) for act in ['pick','drop']]
    maxQ = max(q)
    inc = reward + 0.3 * maxQ
    Q[(s, a, val)] = Q.get((s, a, val),0.0) * (1 - alpha)
    Q[(s, a, val)] = float(Q.get((s, a, val),0.0)) + (alpha * inc)


def updateSpecials(tuple,value):
    global specials
    (i, j, c, w, b) = tuple
    specials[specials.index(tuple)] = (i, j, c, w, b+value)
    print specials


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart, playerHasBlock
    playerHasBlock = False
    player = (4, 0)
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()