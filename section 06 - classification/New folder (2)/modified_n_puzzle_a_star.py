class Node:
    
    def __init__(self,state,gCost,fCost,tile_value,direction,parent):
        #create object of the node
        self.state = state
        self.gCost = gCost
        self.fCost = fCost
        self.direction = direction
        self.tile_value = tile_value
        self.parent = parent
    
    def expand_node(self):
        
        dash= self.find_positions_of_dash()
        x1,y1,x2,y2 = dash[0][0],dash[0][1],dash[1][0],dash[1][1]
        plist1 = [[x1,y1-1],[x1,y1+1],[x1-1,y1],[x1+1,y1]]
        plist2 = [[x2,y2-1],[x2,y2+1],[x2-1,y2],[x2+1,y2]]
        expanded_states=[]
        moves = []
        for i in range(4):
            successor1 = self.swap_tile_dash(x1,y1,x2,y2,plist1[i][0],plist1[i][1])
            successor2 = self.swap_tile_dash(x2,y2,x1,y1,plist2[i][0],plist2[i][1])
            if(successor1 is not None):
#                 moves.append(successor1[1:])
                next_node = Node(successor1[0],0,0,successor1[1],successor1[2],self)
                expanded_states.append(next_node)
            if(successor2 is not None):
#                 moves.append(successor2[1:])
                next_node = Node(successor2[0],0,0,successor2[1],successor2[2],self)
                expanded_states.append(next_node)
        return expanded_states
    
    def find_positions_of_dash(self):
        dash_positions = []
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if(self.state[i][j] == '-'):
                    dash_positions.append([i,j])
        return dash_positions
    
    def swap_tile_dash(self,dash_i,dash_j,dash_x,dash_y,x,y):
        if(x>=0 and x<len(self.state) and y>=0 and y<len(self.state) and not (dash_x==x and dash_y==y) ):
            current_state = self.copy_list(self.state)
            value = current_state[x][y]
            current_state[x][y] = current_state[dash_i][dash_j]
            current_state[dash_i][dash_j] = value
            return [current_state,value,self.find_direction(dash_i,dash_j,x,y)]
        else:
            return None
        
    def find_direction(self,dash_i,dash_j,x,y):
        direction = ""
        if(dash_i==x):
            if(dash_j>y):
                direction="Right"
            else:
                direction = "Left"
        else:
            if(dash_i>x):
                direction="Down"
            else:
                direction="Up"
        return direction
    
    def copy_list(self,list_input):
        out = []
        for i in list_input:
            t = []
            for j in i:
                t.append(j)
            out.append(t)
        return out  
            
            
class N_Puzzle:
    def __init__(self,heuristic):
        self.size_n = 0
        self.OPEN = []
        self.CLOSED = []
        self.heuristic = heuristic
    
    def calculate_f(self,start,goal):
        return self.calculate_h(start.state,goal)+start.gCost
    
    def calculate_h(self,start,goal):
        if(self.heuristic == "Misplaced"):
            total_misplaced = 0
            for i in range(0,self.size_n):
                for j in range(0,self.size_n):
                    if start[i][j] != goal[i][j] and start[i][j] != '-':
                        total_misplaced += 1
            return total_misplaced
        elif(self.heuristic == "Manhatton"):
            total_distance = 0
            start_conf=[i for row in start for i in row ]
            goal_conf=[i for row in goal for i in row ]
            n = self.size_n
            for t in range(len(start_conf)):
                if(start_conf[t]!='-'):
                    g_index = goal_conf.index(start_conf[t])
                    total_distance += abs(g_index//n - t//n) + abs(g_index%n - t%n)  
            return total_distance
        
    def get_move_sequence(self,goal_node):
        moves=[]
        while(goal_node.parent!=None):
            moves.append([goal_node.tile_value,goal_node.direction])
            goal_node = goal_node.parent
        moves.reverse()
        move_seq=", ".join(["("+",".join(move)+")" for move in moves])
        return move_seq,len(moves)
    
    def A_star_algorithm(self,start,goal):
        
        start_list= start
        goal_list = goal
        
        self.size_n = len(start_list)
        
        if(len(start_list)==0 or start_list==None):
            return False
        
        start_node = Node(start_list,0,0, None,None,None)
        start_node.fCost = self.calculate_f(start_node,goal_list)
        
        self.OPEN.append(start_node)
        
        if(start_node.state == goal_list):
            return start_node.fCost
        output = None;
        while(True):
#             print(output)
            if(len(self.OPEN)==0):
                output="False"
                break
            current_state = self.OPEN[0]
            
            if(self.calculate_h(current_state.state,goal_list) == 0):
                output = current_state.fCost
                output = self.get_move_sequence(current_state)
                break

            childs_moves = current_state.expand_node()
            for child in childs_moves:
                nodes = []
                nodes.extend(self.OPEN)
                nodes.extend(self.CLOSED)
                node_state_list = [node.state for node in nodes]
                closed_node = [node.state for node in self.CLOSED]
                if(child.state not in node_state_list):
                    child.gCost = current_state.gCost + 1
                    child.fCost = self.calculate_f(child,goal_list)
                    self.OPEN.append(child)
                else:
                    child.gCost = min(child.gCost,current_state.gCost + 1)
                    prev_fCost = child.fCost
                    child.fCost = self.calculate_f(child,goal_list)
                    if(prev_fCost> child.fCost and (child.state in closed_node)):
                        self.OPEN.append(child)
                        del self.CLOSED[closed_node.index(child.state)]
            del self.OPEN[0]
            self.CLOSED.append(current_state)
            self.OPEN.sort(key = lambda x:x.fCost,reverse=False)
        return output
            
            
startFilepath = input('Enter start file relative path : ') # Start.txt
goalFilepath = input('Enter goal file relative path : ')
startFile = open(startFilepath,"r")
goalFile = open(goalFilepath,"r")
start_list= [list(row.strip('\n').split('\t')) for row in startFile]
goal_list = [list(row.strip('\n').split('\t')) for row in goalFile]

startFile.close()
goalFile.close()

    
puzzle_test_Manhatton = N_Puzzle("Manhatton")
move_sequence_manhatton, move_number_manhatton = puzzle_test_Manhatton.A_star_algorithm(start_list,goal_list)
#output the sequence of moves
output_conf_file=open("Output_sequence_manhatton.txt","w")
output_conf_file.write(move_sequence_manhatton)
output_conf_file.close() 

puzzle_test_Misplaced = N_Puzzle("Misplaced")
move_sequence_Misplaced, move_number_Misplaced = puzzle_test_Misplaced.A_star_algorithm(start_list,goal_list)
#output the sequence of moves
output_conf_file=open("Output_sequence_misplaced.txt","w")
output_conf_file.write(move_sequence_Misplaced)
output_conf_file.close() 
