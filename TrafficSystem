class Car:
    def __init__(self, initial_position, initial_velocity):
        self.position = initial_position
        self.v = initial_velocity
        self.distance_to_next = 1
    
    def __repr__(self):
        return 'V:'+str(self.v)+' P:'+str(self.position)
    
    def accelerate(self, v_max):
        if self.distance_to_next > self.v + 1 and v_max > self.v:
            self.v += 1
        
    def decelerate(self):
        if self.v >= self.distance_to_next:
            self.v = self.distance_to_next - 1
        
    def randomise(self, p):
        if self.v > 0 and random.random() < p:
            self.v -= 1  
            
    def change_speed(self, v_max, p):
        self.accelerate(v_max)
        self.decelerate()
        self.randomise(p)
    
    
    def move(self):
        self.position += self.v


class Road:
    def __init__(self, length, density, p, v_max,no_lanes,roadworks):
        self.length = length
        self.p = p
        self.density = density
        self.roadworks = roadworks
        self.v_max = v_max
        self.lanes = []
        self.cars = []
        self.no_lanes = no_lanes
        self.timestepcounter =1 
        self.build_road()
        
    def __repr__(self):
            return str(self.lanes)

        
        
    def build_road(self):
        distance_to_next = self.v_max+1
        position = self.length-1 
            
        self.lanes = np.zeros((self.no_lanes,self.length),dtype = object)
        lane= [' ' for L in range(self.length)]
            
        for i in range(0,self.no_lanes):
            self.lanes[i]=lane
            
   

            
        while 0<=position:
            if random.random()<self.density:
                for i in range(0,self.no_lanes):
                    v_init = int(min(np.round(self.v_max*random.random()),distance_to_next))
                        
                    self.lanes[i][position] = Car(initial_position = position, initial_velocity = v_init)
                    distance_to_next = 0
            distance_to_next += 1
            position -= 1
         
        if self.roadworks != [0,0,0]:
            self.lanes[self.roadworks[0]][self.roadworks[1]:self.roadworks[2]] = 'R'
        
            
            
    def lanechanging(self):
        self.timestepcounter += 1
        
        changed_lanes = self.lanes
        gapminus = self.v_max
        o=0
        if self.timestepcounter %2 ==0: 
            for h in range(0,self.no_lanes):

                g = h+1 

                if g==self.no_lanes:
                    g=9999

                for car in self.lanes[h]:
                    if car!= ' ' and car !='R':
                        distfg=1
                        distbg=1
                        disth = 1
                        if car.position < self.length:
                            for k in range(1,self.length-car.position):
                                if self.lanes[h][car.position+k]==' ':
                                    disth += 1
                                else:
                                    break
                                if k + car.position == self.length-1:
                                    disth += self.v_max
                            for j in range(1,self.length-car.position):
                                if g!=9999 and self.lanes[g][car.position]==' ':
                                    if self.lanes[g][car.position+j]==' ':
                                        distfg+=1
                                    else:
                                        break
                                    if j + car.position == self.length-1:
                                        distfg += self.v_max
                            for o in range(1,car.position):
                                if g!=9999 and self.lanes[g][car.position]==' ':
                                    if self.lanes[g][car.position-o]==' ':
                                        distbg+=1
                                    else:
                                        break
                            if g!=9999 and self.lanes[g][car.position-o]=='R':
                                distbg=9999


                            if disth < distfg and distbg> self.v_max and car.position<self.length:
                                #self.lanes[g][car.position]=car
                                car.distance_to_next = distfg
                            else:
                                car.distance_to_next=disth

                            if car.position == self.length-1:

                                car.distance_to_next = self.v_max

                
        if self.timestepcounter%2 != 0:
            for h in range(0,self.no_lanes):

                g = h-1 

                if g==-1:
                    g=9999


                for car in self.lanes[h]:
                    if car!= ' ' and car !='R':
                        distfg=1
                        distbg=1
                        disth = 1
                        if car.position < self.length:
                            for k in range(1,self.length-car.position):
                                if self.lanes[h][car.position+k]==' ':
                                    disth += 1

                                else:
                                    break
                                if k + car.position == self.length-1:
                                    disth += self.v_max
                            for j in range(1,self.length-car.position):
                                if g!=9999 and self.lanes[g][car.position]==' ':
                                    if self.lanes[g][car.position+j]==' ':
                                        distfg+=1
                                    else:
                                        break
                                if j + car.position == self.length-1:
                                    distfg += self.v_max 
                            for o in range(1,car.position):
                               # print(car.position)

                                if g!=9999 and self.lanes[g][car.position]==' ':
                                    if self.lanes[g][car.position-o]==' ':
                                        distbg+=1
                                    else:
                                        break
                            if g!=9999 and self.lanes[g][car.position-o]=='R':
                                distbg=9999


                            if disth < distfg and distbg> self.v_max and car.position<self.length:
                                self.lanes[g][car.position]=car
                                car.distance_to_next = distfg
                            else:
                                car.distance_to_next=disth

                            if car.position == self.length-1:

                                car.distance_to_next = self.v_max

            
    
    def timestep(self):
        self.lanechanging()
        if self.timestepcounter% 3 ==0:
            next_lanes = np.zeros((self.no_lanes,self.length),dtype = object)
            for o in range(self.no_lanes):
                next_lanes[o]= [' '] * self.length

            if self.roadworks != [0,0,0]:
                next_lanes[self.roadworks[0]][self.roadworks[1]:self.roadworks[2]] = 'R'

            

            for i in range(0,self.no_lanes):
                for car in self.lanes[i]:
                    if car != ' ':
                        if car != 'R':
                            car.change_speed(self.v_max,self.p)
                            car.move()

                            if car.position < self.length and next_lanes[i][car.position]!='R':
                                next_lanes[i][int(car.position)]=car


                if next_lanes[i][0] == ' ' and random.random() < self.v_max*self.density:
                    next_lanes[i][0] = Car(initial_position = 0, initial_velocity = int(np.round(self.v_max*random.random())))
                if next_lanes[i][self.length-1] != ' ' and next_lanes[i][self.length-1]!= 'R':
                    next_lanes[i][self.length-1]==' '

                self.lanes[i]=next_lanes[i]
                        
    def road_to_values(self, init_lane = False):
        vals = np.full((self.no_lanes, self.length), -1)
        if init_lane:
            init_lane_ = np.full((self.no_lanes, self.length), -1)
        for i, lane in enumerate(self.lanes):
            for j, car in enumerate(lane):
                if car != ' ':
                    if car == 'R':
                        vals[i,j] = -2
                    else:
                        vals[i,j] = car.v
                        if init_lane:
                            init_lane_[i,j] = car.initial_lane
                        
        if init_lane:
            return vals, init_lane_
                
        return vals
