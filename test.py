import wikipedia
wikipedia.donate()
a = str(input("Search: "))
print(wikipedia.suggest(a))

search_results = wikipedia.search(a, results=5)
print(search_results)
for result in search_results:
    result = result.replace("-", "")
    print(result)
    print("="*10)
    try:
        summary = wikipedia.summary(result)
        if(len(summary) > 200): summary = summary[:200]
        print(summary)
    except:
        print("null")
        print("\n"*3)
        continue
    print("\n"*3)