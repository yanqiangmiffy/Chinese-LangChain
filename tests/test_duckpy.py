from duckpy import Client

client = Client()

results = client.search("Python Wikipedia")

# Prints first result title
print(results[0].title)

# Prints first result URL
print(results[0].url)

# Prints first result description
print(results[0].description)
# https://github.com/AmanoTeam/duckpy