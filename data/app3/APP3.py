import math
file_names = {'1':'paris_v4.csv', '2':"lyon.csv", '3':"lille.csv", '4':"bordeaux.csv"}
stations = {}
stations_list = []


def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371000
    return c*r


def Show_trip(L, show_details=False):     #print a given trip with all stations and connections 
    trip, time_trip = L

    if trip is None:
        print("\n❗ERROR: No trip found")

    else:
        n_connection = 0
        station_start = trip[0][0]
        line_start = trip[0][1] 

        print(f"\n\n> Monter station {station_start}, ligne {line_start}") 
        for i in range(1, len(trip)): # Connections
            station = trip[i][0] 
            line = trip[i][1] 
            if line != trip[i - 1][1]: # Is a connection
                print(f"> Correspondance station {trip[i - 1][0]} pour ligne {line}") 
                n_connection += 1
            if show_details == True and i < len(trip)-1: 
                print(f"  Continuer station {station} sur {line}") 

        station_end = trip[-1][0] 
        line_end = trip[-1][1] 
        print(f"> Descendre station {station_end}\n") 

        # Total time and connections
        print(f"> Temps de trajet total:{Format_time(time_trip)}") 
        print(f"> Nombre de correspondances :{n_connection}") 


def Format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}h {minutes:02d}min {seconds:02d}s"


def Explore_L(L:list, word:str): #Explore a sorted list by dichotomy
    a = 0
    b = len(L)

    if L != []:
        while a < b:
            i = (a+b)//2
            if word < L[i].lower():
                b = i
            else:
                a = i+1
    return a

def Near_words(L:list, word:str, n:int): #Show the words close to the searched one
    i = Explore_L(L, word)
    L_show = [L[i+h] for h in range(-n, n+1) if 0<=i+h<len(L) and word != L[i+h]]
    for w in L:
        if word in w.lower() and w not in L_show:
            L_show.append(w)
    return L_show


def Print_near_stations(station_name, stations_list):
    print(f"\n❗ERROR: Station '{station_name}' does not exist")
    print("Similar station names: ", end="")
    stations_list_similar = Near_words(stations_list, station_name, 2)
    i_max = len(stations_list_similar)-1
    for i, station in enumerate(stations_list_similar):
        print(station, end="")
        if i != i_max:
            print(", ", end="")


def Menu():
    while True:
        answer = input("Choose a City:\n 1. Paris \n 2. Lyon \n 3. Lille \n 4. Bordeaux\n>>> ")
        if answer in file_names.keys():
            stations = Generate_dict_stations(file_names[answer])
            stations_list = sorted(stations.keys())
            break
        else:
            print("\n❗ERROR: Invalid answer")

    while True:
        station_start = input("\nEnter start station name:\n>>> ")

        if station_start not in stations:
            Print_near_stations(station_start, stations_list)
        else:
            break

    while True:
        station_end = input("\nEnter end station name:\n>>> ")
        if station_end not in stations:
            Print_near_stations(station_end, stations_list)
        else:
            break
    
    Show_trip(dijkstra(stations, station_start, station_end), True)


def File_to_List(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        L_file = f.readlines()
        for i, line in enumerate(L_file):
            line = line.strip()
            line = line.split(";")
            L_file[i] = line
            L_file[i][2] = [float(n) for n in L_file[i][2].split(',')]
            
            word = ''
            current_line = ''
            connections = {}
            for j,l in enumerate(line[3]):
                if l == ':':
                    current_line=word
                    connections[current_line]=[]
                    if line[3][j+1] == ",":
                        connections[current_line].append(line[1])
                    word = ''

                elif l == ',' and word != '':
                    connections[current_line].append(word)
                    word = ""

                elif j == len(line[3])-1:
                    word += l
                    connections[current_line].append(word)
                    word = ""
                
                elif l != "," and l != ":":
                    word += l

            L_file[i][3] = connections
                
        return L_file


def Generate_dict_stations(file_name):
    stations = {}
    L_file = File_to_List(file_name)
    for Line in L_file:
        if Line[1] not in stations:
            stations[Line[1]] = {}

        for l in Line[3]:
            if Line[3][l][0] != Line[1]:
                stations[Line[1]][l] = [Line[3][l], Line[2]]
    return stations


def dijkstra(stations, station_start, station_end):
    costs = {node: float('inf') for node in stations}
    costs[station_start] = 0
    paths = {station_start: [(station_start, None)]}
    priority_queue = [(0, station_start)]

    while priority_queue:
        # on recherche le nœud avec le coût le plus faible
        current_cost, current_node = min(priority_queue, key=lambda x: x[0])
        priority_queue.remove((current_cost, current_node))
        if current_node == station_end:
            return (paths[station_end], costs[station_end])

        for line, l in stations[current_node].items():
            if paths[station_start][-1][1] is None:
                paths[station_start] = [(station_start, line)]
            for neighbor in l[0]:
                new_cost = current_cost + 60
                if line != paths[current_node][-1][1]:
                    new_cost += int(haversine(stations[neighbor][line][1][0],stations[neighbor][line][1][1], l[1][0], l[1][1])/1.39) + 120
                elif 'METRO' in line:
                    new_cost += int(haversine(stations[neighbor][line][1][0],stations[neighbor][line][1][1], l[1][0], l[1][1])/14)
                elif 'TRAM' in line:
                    new_cost += int(haversine(stations[neighbor][line][1][0],stations[neighbor][line][1][1], l[1][0], l[1][1])/10)

                if new_cost < costs[neighbor]:
                    paths[station_start] = [(station_start, line)]
                    costs[neighbor] = new_cost 
                    paths[neighbor] = paths[current_node] + [(neighbor, line)]
                    priority_queue.append((new_cost, neighbor))
    return None, 0


Menu()