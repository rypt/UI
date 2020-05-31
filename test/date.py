import datetime
b = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(b)
import datetime
d1 = datetime.datetime.strptime('2015-03-05  17:41:20', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2015-03-02 17:41:20', '%Y-%m-%d %H:%M:%S')

if d1>d2:
    print('1')
else:
    print('2')

day=(d1-d2).days
print(day)