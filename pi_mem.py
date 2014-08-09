def main():
    pi="3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844"
    usr = raw_input("pi? ")
    print pi
    print usr

    incorrect = ""
    for i in range(0,len(usr)):
        if usr[i] == pi[i]:
            incorrect+=" "
        else:
            incorrect+= pi[i]
    
    if incorrect.strip()=='':
        print str(len(usr) - 1) + ' digits perfect!'
    else:
        print incorrect
        
    print "next 3 digits: " + pi[len(usr):len(usr)+3]
