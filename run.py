'''
import optimizer

#result = optimizer.parse_string("CISC203,CISC204,CISC220,STAT263", 'F')
result = optimizer.parse_string("CISC221,CISC223,CISC235,CISC271,CLST205", 'W')


print(result[0])
print("----------------------------")
for r in result[1]:
    print(r)
    print("----------------------------")
'''

from webapp import app

app = app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 80)
