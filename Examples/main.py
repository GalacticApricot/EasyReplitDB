from EasyReplitDB import db
db['Galactic'] = 'Apricot' # creates entry and/or sets 'Galactic' to 'Apricot'
db['JoinTheDeveloperProject'] = 'https://discord.gg/9HX8aNutES'
print(db['Galactic']) # returns 'Apricot'
print(db.keys()) # outputs ['Galactic', 'JoinTheDeveloperProject']
print(db.prefix('Join')) # outputs ['JoinTheDeveloperProject']
del db['Galactic'] # deletes the entry 'Galactic'
