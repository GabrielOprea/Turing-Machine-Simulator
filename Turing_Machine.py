"""
function that reads a string interpretation of a file and
builds a dictionary representation of a Turing machine,
with the keys: no_states, final_states, transitions 
"""

def readTM(file_content):
    lines = file_content.split('\n')
    TM = {}
    TM['no_states'] = int(lines[0])
    final_states = []
    
    #if we have any final state,we use list comprehension
    #on the words in the second line to build the list
    if not lines[1].startswith('-'):
        final_states = [int(i) for i in lines[1].split(' ')]
    TM['final_states'] = final_states
    
    #a list of tuples containing 5 elements describing a specific transition
    transitions = []
    for i in range(2, len(lines)):
        crt_transition = tuple(x for x in lines[i].split(' '))
        transitions.append(crt_transition)
    TM['transitions'] = transitions
    return TM

"""
auxiliary function used to add # on the tape if the words in the left
or right of the cursor are empty strings
"""
def add_empty(u):
    if not u:
        return'#'
    else:
        return u

    
#computes a step in the execution of the machine
def step(config, TM):
    #config is a tuple (u, q, v), so we extract the elements
    crt_state = config[1]
    u = config[0]
    v = config[2]
    
    u = add_empty(u) # added if needed
    v = add_empty(v)
    
    for trans in TM['transitions']:

        #checks if we can make a transition from the current state
        if int(trans[0]) == crt_state and trans[1] == v[0]:
            #gets the direction(L, H or R)
            cmd = trans[4]
            crt_state = int(trans[2])
            write = trans[3] #the symbol that must be writen
            if cmd == 'L':
                v = write + v[1:]
                v = u[-1] + v
                u = u[:-1]
            elif cmd == 'R':
                u += write
                v = v[1:]
            elif cmd == 'H':
                v = write + v[1:]
            #we check again if u or v are equal to epsilon
            u = add_empty(u)
            v = add_empty(v)
            
            #we return the next configuration
            return (u, crt_state, v)
        
    #if no transition from the current state and symbol can be found
    return False


#writes a word on the tape and accepts, rejects or loops
def accept(TM, w):
    eps = ''
    config = (eps, 0, w) #initial configuration
    
    #we get all configs, if we reach a final state then accept, if
    #the machine hangs then reject
    while True:
        config = step(config, TM)
        if config == False:
            return False
        if config[1] in TM['final_states']:
            return True

"""
same as previous function but in k steps, this time the
Turing machine can only accept or reject a word
"""
def k_accept(TM, w, k):
    eps = ''
    config = (eps, 0, w)
    while k > 0 :
        config = step(config, TM)
        if config == False:
            return False
        if config[1] in TM['final_states']:
            return True
        k -= 1
    return False

def main():
    file = ""
    #reads from stdin until EOF and builds the file string
    while True:
        try:
            inp = input()
            file += inp + '\n'
        except EOFError:
            break
    
    #gets a list of lines
    lines = file.split('\n')
    del lines[-1] #since it only contains a newline character
    
    if lines[0] == 'step':  #task type
        configurations = lines[1].split(' ')  #all TM configs
        lines = lines[2:]  #input for readTM function
        tm_content = '\n'.join((elem) for elem in lines)
        TM = readTM(tm_content)
        for elem in configurations:
            #extract the important values and add them in tuple
            values = elem.replace('(', '').replace(')', '').split(',')
            config = (values[0], int(values[1]), values[2])
            #formats result and prints it to stdout
            result = str(step(config, TM)).replace("'", "").replace(" ", "")
            print(result + ' ', end = '')
            
    elif lines[0] == 'accept':
        words = lines[1].split(' ')
        lines = lines[2:]
        tm_content = '\n'.join((elem) for elem in lines)
        TM = readTM(tm_content)
        #iterates through words and check if they are accepted
        for w in words:
            print(str(accept(TM, w)) + " ", end = '')
    elif lines[0] == 'k_accept':
        #builds pairs of word and value k
        pairs = lines[1].split(' ')
        lines = lines[2:]
        tm_content = '\n'.join((elem) for elem in lines)
        TM = readTM(tm_content)
        for p in pairs:
            w = p.split(',')[0]
            k = int(p.split(',')[1])
            print(str(k_accept(TM, w, k)) + " ", end = '')

if __name__ == '__main__':
    main()