import pickle

database= database = pickle.load(open('userData/database.p','rb'))
userName = raw_input('Please enter your name: ')
if userName in database:
    database[userName]['logins'] += 1
    print('welcome back ' + userName + '.')
    print 'Your  successful attempts: '
    print "Digit 0 : " , database[userName]['digit0attempted']
    print "Digit 1 : " , database[userName]['digit1attempted']
    print "Digit 2 : " , database[userName]['digit2attempted']
    print "Digit 3 : " , database[userName]['digit3attempted']
    print "Digit 4 : " , database[userName]['digit4attempted']
    print "Digit 5 : " , database[userName]['digit5attempted']
    print "Digit 6 : " , database[userName]['digit6attempted']
    print "Digit 7 : " , database[userName]['digit7attempted']
    print "Digit 8 : " , database[userName]['digit8attempted']
    print "Digit 9 : " , database[userName]['digit9attempted']
else:



    database[userName] = { 'logins' : 1, 'digit0attempted': 0 ,'digit1attempted': 0 , 'digit2attempted': 0,
                           'digit3attempted': 0, 'digit4attempted': 0, 'digit5attempted': 0,'digit6attempted': 0,
                           'digit7attempted': 0, 'digit8attempted': 0, 'digit9attempted': 0}
    print('welcome ' + userName + '.')
    print('Your  successful attempts: ')
    print "Digit 0 : " , database[userName]['digit0attempted']
    print "Digit 1 : " , database[userName]['digit1attempted']
    print "Digit 2 : " , database[userName]['digit2attempted']
    print "Digit 3 : " , database[userName]['digit3attempted']
    print "Digit 4 : " , database[userName]['digit4attempted']
    print "Digit 5 : " , database[userName]['digit5attempted']
    print "Digit 6 : " , database[userName]['digit6attempted']
    print "Digit 7 : " , database[userName]['digit7attempted']
    print "Digit 8 : " , database[userName]['digit8attempted']
    print "Digit 9 : " , database[userName]['digit9attempted']
print database
pickle.dump(database,open('userData/database.p','wb'))

