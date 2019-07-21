import optimizer

result = optimizer.parse_string("CISC203,CISC204,CISC220,STAT263,CLST205", 'F')

print(result[0])
for r in result[1]:
    print(r)
