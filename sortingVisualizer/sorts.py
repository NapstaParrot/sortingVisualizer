def swap(arr, i1, i2) :
    arr[i1], arr[i2] = arr[i2], arr[i1]
    return arr
    

def bubble(arr) :
    sort_states, pointers = [arr.copy()], []
    # pointers[] is for highlights mostly
    
    for i in range(len(arr)) :
        for j in range(len(arr) - i - 1) :
            if arr[j] > arr[j + 1] :
                swap(arr, j, j + 1)
                
            sort_states.append(arr.copy())
            pointers.append([j, j + 1])

    return sort_states, pointers
   

def insertion(arr) :
    sort_states, pointers = [arr.copy()], []
    
    for i in range(len(arr)) :
        while arr[i - 1] > arr[i] and i > 0 :
            swap(arr, i - 1, i)
            i -= 1
            
            sort_states.append(arr.copy())
            pointers.append([i - 1, i])
            
    return sort_states, pointers
    
   
def selection(arr) :
    sort_states, pointers = [arr.copy()], []
    
    for i in range(len(arr)) :
        min = i
        
        for j in range(i, len(arr)) :
            if arr[j] < arr[min] :
                min = j
        
            sort_states.append(arr.copy())
            pointers.append([j, min])
            
        swap(arr, i, min)
        
    return sort_states, pointers