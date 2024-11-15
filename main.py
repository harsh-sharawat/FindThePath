import pygame
import random
from collections import deque 
import  heapq
import sys

pygame.init()
width=900
height=1000

screen = pygame.display.set_mode((width,height))
font=pygame.font.Font('freesansbold.ttf',25)

N = 20
T = 10
rows=N
col=N
tile_size = 900//rows

def updateN(n):
    global N,T,rows,col,tile_size

    N = n
    T = 0
    rows=N
    col=N
    tile_size = 900//rows
   


grid =    [[0 for _ in range(col)] for _ in range(rows)]
visited = [[0 for _ in range(col)] for _ in range(rows)]
parent = {
    (-1,-1) : (-1,-1),
}

def reset_visited():
     global visited ,parent
     visited= [[0 for _ in range(col)] for _ in range(rows)]
     parent = {
    (-1,-1) : (-1,-1)
    }

def reset_grid():
    global grid,dist
    dist = 'inf'
    grid = [[0 for _ in range(col)] for _ in range(rows)]
    grid_update()





 

#changing grid
def grid_update():
    global grid
    if start_node :
        
            y,x = mouse_to_ind(start_node)
            if grid[y][x] in [0,-1]:
                grid[y][x] = 2
        
        
    if end_node :
        y,x = mouse_to_ind(end_node) 
        if grid[y][x] in [0,-1]:
            grid[y][x] = 3
        
        

    if mouse_pos:
        y,x = mouse_to_ind(mouse_pos)
        if grid[y][x] == 0:
            grid[y][x] =- 1
        elif grid[y][x] == -1:
            grid[y][x] = 0

def randomize_canvas():
    global grid
    for row in range(rows):
        for c in range( col ):

            if grid[row][c] == 0:
                grid[row][c] = random.choice([-1,0,0])


# coloring squares based on state of grid and visited
   
def draw_canvas():
   
    for row in range(rows):
        for c in range(col):

            x= c * tile_size
            y= row * tile_size + 100

            if grid[row][c] == 2:
                screen.fill((0,255,0),(x,y,tile_size,tile_size))
            elif grid[row][c] == 3:
                screen.fill((255,0,0),(x,y,tile_size,tile_size))
            elif grid[row][c] == -1:
                screen.fill((40,40,40),(x,y,tile_size,tile_size))
            elif visited[row][c] in [1,10,11]:
                screen.fill((110,110,0),(x,y,tile_size,tile_size))
            # elif visited[row][c] == 1 :
            #     screen.fill((110,110,110),(x,y,tile_size,tile_size))
            elif visited[row][c] == 5:
                screen.fill((255, 192, 203),(x,y,tile_size,tile_size))




            pygame.draw.rect(screen,(0,0,0),(x,y,tile_size,tile_size),1)
            
    
        
    
    

    


def draw_msg_block(x=0,y=0, h=50,w=160,color=(120,120,120),text=""):
    screen.fill(color,(x,y,w,h))
    pygame.draw.rect(screen,(0,0,0),(x,y,w,h),2)
    fcolor=(0 ,0,0)
    if node_status =='start_node':
        fcolor=(0,255,0)
    elif node_status == 'end_node':
        fcolor= (255,0,0)
    else: 
        fcolor = (0,0,255)
    
    
    msg=font.render(text,True,fcolor)
    screen.blit(msg,(x+20,y+10))


#selecting no of rows and cols

def draw_curr_N(x=0,y=50, h=50,w=160,color=(120,120,120),text=""):

    screen.fill(color,(x,y,w,h))
    pygame.draw.rect(screen,(0,0,0),(x,y,w,h),2)
    msg=font.render('N = '+str(N),True,(0,255,0))
    screen.blit(msg,(x+20,y+20))

    if n_drop_down:
        for i , option in enumerate(n_option):
            screen.fill(color,(x,50*i+100,w,h))

            pygame.draw.rect(screen,(0,0,0),n_option_rects[i],2)
            newn= font.render(str(option),True,(0,255,0))
            screen.blit(newn,(n_option_rects[i].x+20,n_option_rects[i].y+20))



#selecting algorithm
def current_algo_selector(x=160,y=0, h=100,w=160,color=(120,120,120),text='dfs'):
    screen.fill(color,(x,y,w,h))
    pygame.draw.rect(screen,(0,0,0),(x,y,w,h),2)
    msg=font.render(text,True,(0,255,0))
    screen.blit(msg,(x+20,y+20))

    if drop_down:
        for i , option in enumerate(algo_option):
            screen.fill(color,(x,100*(i+1),w,h))

            pygame.draw.rect(screen,(0,0,0),option_rects[i],2)
            algo_name= font.render(option,True,(0,255,0))
            screen.blit(algo_name,(option_rects[i].x+20,option_rects[i].y+20))
          



def pause_play(x=320,y=0, h=100,w=100,color=(120,120,120)):
    screen.fill(color,(x,y,w,h))
    pygame.draw.rect(screen,(0,0,0),(x,y,w,h),2)
    text='play' if algo_state == False else 'pause'
    msg=font.render(text,True,(0,255,0))
    screen.blit(msg,(x+20,y+20))


# set random grid state
def random_button(x=420,y=0, h=100,w=140,color=(120,120,120),text="randomize"):
    screen.fill(color,(x,y,w,h))
    pygame.draw.rect(screen,(0,0,0),(x,y,w,h),2)
    msg=font.render(text,True,(0,255,0))
    screen.blit(msg,(x+5,y+20))


def reset_button(x=560,y=0, h=100,w=140,color=(120,120,120),text="reset_grid"):
    screen.fill(color,(x,y,w,h))
    pygame.draw.rect(screen,(0,0,0),(x,y,w,h),2)
    msg=font.render(text,True,(0,255,0))
    screen.blit(msg,(x+10,y+20))


#show path distance
def distance(x=700,y=0, h=100,w=200,color=(120,120,120),text="Distance:"):
    screen.fill(color,(x,y,w,h))
    pygame.draw.rect(screen,(0,0,0),(x,y,w,h),2)
    msg=font.render(text+dist,True,(0,255,0))
    screen.blit(msg,(x+20,y+20))



#mouse position to grid index
def mouse_to_ind(nn):
    return ((nn[1]-100)//tile_size,nn[0]//tile_size)


#direction selctors
delrow = [-1, 0, 1, 0]
delcol = [0, 1, 0, -1]

#algorithms 


def dfs(start_node, end_node):
    stack = [start_node]
    Flag = False
    while stack:
        x, y = stack.pop()
        visited[x][y] = 1

        if (x, y) == end_node:
            Flag = True
            break

        for i in range(4):
            nr = x + delrow[i]
            nc = y + delcol[i]

            if 0 <= nr < rows and 0 <= nc < col and grid[nr][nc] != -1 and grid[nr][nc] != 2 and not visited[nr][nc]:
                parent[(nr,nc)] = (x,y)
                stack.append((nr, nc))

        draw_canvas()
        pygame.time.delay(T)
        pygame.display.update()
    if Flag:
        
        p = (0, 0 )
        node = end_node
        d = 0 
        while node != start_node:
            d+=1     
            p = parent[node]        
            visited[p[0]][p[1]] = 5
            node = p
            draw_canvas()
            pygame.time.delay(T)
            pygame.display.update()
        global dist 
        dist = str(d)
           
    return Flag


#bfs
def bfs(start_node, end_node):
    queue = deque([start_node])
    Flag = False
    while queue:
        x, y = queue.popleft()       

        if (x, y) == end_node:            
            Flag =  True
            break

        for i in range(4):
            nr = x + delrow[i]
            nc = y + delcol[i]

            if (0 <= nr < rows and 0 <= nc < col
                and grid[nr][nc] != -1 and grid[nr][nc] != 2 
                and not visited[nr][nc]):
                parent[(nr,nc)] = (x,y)
                queue.append((nr,nc))
                visited[nr][nc] = 1

        draw_canvas()
        pygame.time.delay(T)
        pygame.display.update()


    if Flag:
        d = 0
        p = (0, 0)
        node = end_node
        while node != start_node:
            d+=1
            p = parent[node]         
            visited[p[0]][p[1]] = 5
            node = p

            draw_canvas()
            pygame.time.delay(T)
            pygame.display.update()
        global dist
        dist = str(d)

    return Flag


# a-star search
def heu(node1,node2):
    return ((node1[0]-node2[0])**2) + ((node1[1]-node2[1])**2)

def a_star(start_node, end_node):
    heap = [(heu(start_node,end_node),start_node,0)]
    Flag = False

    while(heap):
        node = heapq.heappop(heap)
        x,y  = node[1]
        if( (x,y ) == end_node):
            Flag= True
            break

        for i in range(4):
            nr = x + delrow[i]
            nc = y + delcol[i]

            if (0 <= nr < rows and 0 <= nc < col
                and grid[nr][nc] != -1 and grid[nr][nc] != 2
                and not visited[nr][nc]):
                gn = node[2]+1
                hn = heu((nr,nc),end_node)
                fn= gn+hn
                heapq.heappush(heap,(fn,(nr,nc),gn))
                parent[(nr,nc)] = (x,y)
                visited[nr][nc] = 1
        draw_canvas()
        pygame.time.delay(T)
        pygame.display.update()


    if Flag:
        p = (0, 0 )
        node = end_node
        d=0
        while node != start_node:
            d+=1           
            p = parent[node]             
            visited[p[0]][p[1]] = 5
            node = p

            draw_canvas()
            pygame.time.delay(T)
            pygame.display.update()
        
        global dist 
        dist = str(d)
    
    return Flag


def best_first(start_node, end_node):
    heap = [(heu(start_node,end_node),start_node)]
    Flag = False

    while(heap):
        node = heapq.heappop(heap)
        x,y  = node[1]
        if( (x,y ) == end_node):
            Flag= True
            break

        for i in range(4):
            nr = x + delrow[i]
            nc = y + delcol[i]
            if (0 <= nr < rows and 0 <= nc < col
                and grid[nr][nc] != -1 and grid[nr][nc] != 2 
                and not visited[nr][nc]):
                
                hn = heu((nr,nc),end_node)
                
                heapq.heappush(heap,(hn,(nr,nc)))
                parent[(nr,nc)] = (x,y)
                visited[nr][nc] = 1

        draw_canvas()
        pygame.time.delay(T)
        pygame.display.update()
    if Flag:        
        p = (0, 0)
        d=0
        node = end_node
        while node != start_node:
            d+=1           
            p = parent[node]
                      
            visited[p[0]][p[1]] = 5
            node = p

            draw_canvas()
            pygame.time.delay(T)
            pygame.display.update()
        
        global dist 
        dist = str(d)


    
    return Flag


def bidirectional_search(start_node, end_node):
    Flag = False
    start_to_goal = start_node
    goal_to_start = end_node

    queue_start = deque([start_node])
    queue_goal = deque([end_node])  

    while queue_start and queue_goal and not Flag:
        # Expand from the start side
        if queue_start:
            x, y = queue_start.popleft()
            for i in range(4):
                nr = x + delrow[i]
                nc = y + delcol[i]
                
                if (0 <= nr < rows and 0 <= nc < col 
                            and grid[nr][nc] != -1 
                          and visited[nr][nc]!=10
                          ):
                    if(visited[nr][nc] == 11):
                        start_to_goal = (x,y)
                        goal_to_start = (nr, nc)
                        Flag = True
                        break

                    queue_start.append((nr, nc))
                    visited[nr][nc] =10
                    parent[(nr, nc)] = (x, y)
                    
                    
                    

        # Expand from the goal side
        if queue_goal and not Flag:
            x, y = queue_goal.popleft()
            for i in range(4):
                nr = x + delrow[i]
                nc = y + delcol[i]
                
                if (0 <= nr < rows and 0 <= nc < col and grid[nr][nc] != -1 
                        and  visited[nr][nc]!= 11):
                    if(visited[nr][nc] == 10):
                        start_to_goal = (nr, nc)
                        goal_to_start = (x,y)
                        Flag = True
                        break

                    queue_goal.append((nr, nc))
                    visited[nr][nc] =11
                    parent[(nr, nc)] = (x, y)       
        
        draw_canvas()  
        pygame.time.delay(T)
        pygame.display.update()

    if Flag:
        d = 1
        node1 = start_to_goal
        node2 = goal_to_start        

        while node1 != start_node and node2 != end_node:
            d += 2
            visited[node1[0]][node1[1]] = 5
            node1 = parent[node1]
            visited[node2[0]][node2[1]] = 5
            node2  = parent[node2]
            
            draw_canvas()
            pygame.time.delay(T)
            pygame.display.update()
        
        
        while node1 != start_node:
            d += 1
            visited[node1[0]][node1[1]] = 5
            node1 = parent[node1]
            draw_canvas()
            pygame.time.delay(T)
            pygame.display.update()
        
        # Trace the path back to the end node
        while node2 != end_node:
            d += 1
            visited[node2[0]][node2[1]] = 5
            p = parent[node2]
            node2 = p
            draw_canvas()
            pygame.time.delay(T)
            pygame.display.update()     
        
        global dist
        dist = str(d)
        
    return Flag  



node_status='start_node'
drop_down = False
n_drop_down = False
start_node=None
end_node=None
mouse_pos=None
running = True
dist = 'inf'

algo_state = False
algo_option=['dfs','bfs','A*','best_first','bi_direc']
n_option = [i for i in range(10,101,10)]
option_rects = [pygame.Rect(160, (i+1) * 100, 160, 100) for i in range(len(algo_option))]
n_option_rects = [pygame.Rect(0, 100 + i * 50, 160, 50) for i in range(len(n_option))]
selected_algo = 'dfs'

functions = {
    'dfs' : dfs,
    'bfs' : bfs,
    'A*' : a_star,
    'best_first' : best_first,
    'bi_direc' : bidirectional_search
}
while running:
   
    screen.fill((200, 201, 200),(0,100,1000,900))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 160<pygame.mouse.get_pos()[0]<=320 and 0<pygame.mouse.get_pos()[1]<=100:
                drop_down = True

            elif 0<pygame.mouse.get_pos()[0]<=160 and 50<pygame.mouse.get_pos()[1]<=100:
                n_drop_down = True
            elif drop_down :
                    for i,rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            selected_algo = algo_option[i]

                            drop_down = False
                            break
                    else:
                        drop_down = False

            elif n_drop_down:
                for i,rect in enumerate(n_option_rects):
                        if rect.collidepoint(event.pos):
                            updateN(n_option[i])

                            node_status = 'start_node'
                            start_node=None
                            end_node=None
                            mouse_pos=None
                            dist = 'inf'
                            reset_grid()
                            reset_visited()


                            n_drop_down = False
                            break
                else:
                    n_drop_down = False

            elif node_status == 'start_node':
                if pygame.mouse.get_pos()[1]>=100:
                    start_node=pygame.mouse.get_pos()
                    grid_update()
                    node_status = 'end_node'
            elif node_status == 'end_node':
                if pygame.mouse.get_pos()[1]>=100:
                    end_node=pygame.mouse.get_pos()
                    if end_node == start_node:
                        end_node = None
                    else:

                        grid_update()
                        node_status = 'ready'
            else:
                try:
                    if pygame.mouse.get_pos()[1]>=100 :
                        algo_state=False
                        mouse_pos = pygame.mouse.get_pos()
                       
                        grid_update()                       
                        
                        reset_visited()
                        
                        node_status='ready'

                    #click on ready - pause False = paused // True = running
                    elif 320<pygame.mouse.get_pos()[0]<=420:

                        
                        if  algo_state == False:
                            reset_visited()
                            node_status='running'
                            draw_msg_block(text=node_status)
                        


                                                
                        algo_state = not algo_state

                    #randomize the canvas
                    elif 420<pygame.mouse.get_pos()[0]<=560:
                        algo_state = False
                        reset_grid()
                        reset_visited()
                        randomize_canvas()
                        node_status='ready'

                    #reset grid
                    elif 560<pygame.mouse.get_pos()[0]<=700:
                        start_node=None
                        end_node= None
                        reset_grid()
                        reset_visited()
                        node_status = 'start_node'
                        algo_state=False
                        mouse_pos=None

                    

                except Exception as e:
                    print(e)
                    pass
                          

    if node_status == 'running' and algo_state:
        functions[selected_algo](mouse_to_ind(start_node), mouse_to_ind(end_node))
        node_status='done'
        algo_state = False               


    draw_canvas()
    draw_msg_block(text=node_status)
    
    draw_curr_N()
    pause_play()
    random_button()
    reset_button()
    distance()
    current_algo_selector(text = selected_algo)
    pygame.display.update()

    