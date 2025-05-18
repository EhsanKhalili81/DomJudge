places = [0,0,1,1,0]
start = 3
endRight = len(places)
counterRight = 0
step = 1
counterLeft = 0

if start == 0 or start == len(places)-1:
    if start == 0:
        for i in range(1,len(places)):
            if places[0] == 1:
                counterRight += 2
            if places[i] == 0:
                counterRight +=1
            elif places[i] == 1:
                places[i] = 0
                counterRight += 3
    elif start == len(places)-1:
        print("Inja Nemyad")
        # for x in range(start-1,-1):
        #     print("dfgdfgdfgdfgdfgdfgdfd")
        #     if places[start] == 1:
        #         counterLeft += 2
        #     if places[x] == 0:
        #         counterLeft +=1
        #     elif places[x] == 1:
        #         places[x] = 0
        #         counterLeft += 3
else:
    for i in range(start+1,endRight,step):
        if places[start] == 1 :
            places[start] = 0
            counterRight += 2
        if places[i] == 0:
            counterRight += 1
        elif places[i] == 1:
            places[i] = 0
            counterRight += 3
        if i == len(places)-1:
            start = len(places)-1
            endRight = -1
            step *= -1
            for i in range(start-1,endRight,step):
                if places[i] == 0:
                    counterRight += 1
                elif places[i] == 1:
                    places[i] = 0
                    counterRight += 3
    print(counterRight)

    places2 = [0,0,1,1,0]

    endLeft = -1
    step = -1
    start = 2
    for i in range(start-1,endLeft,step):
        if places2[start] == 1:
            places2[start] = 0 
            counterLeft += 2
        if places2[i] == 0:
            counterLeft += 1
        elif places2[i] == 1:
            places2[i] = 0
            counterLeft += 3
        if i == 0:
            start = 1
            endLeft = len(places2)
            step *= -1
            for z in range(start,endLeft,step):
                if places2[z] == 0:
                    counterLeft += 1
                elif places2[z] == 1:
                    places2[z] = 0
                    counterLeft += 3

    print(counterLeft)

if counterLeft > counterRight:
    print("Be Samt Chap Beravid , Hazine : " , counterRight)
else:
    print("Be Samt Rast Beravid , Hazine : " , counterLeft)




