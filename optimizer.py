import parser
resp = parser.parse_request("MATH121,CISC121,MATH111,CISC102,ECON112,CLST102,CISC124")
for response in resp:
    print(response)
