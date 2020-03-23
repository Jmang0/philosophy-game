import requests
from bs4 import BeautifulSoup

def philosophyGame(url,seen=None,count=0):
    if seen == None:
        seen= []
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    print(soup.h1.string)
    body = soup.find(class_="mw-parser-output")
    for paragraph in body.find_all("p"):
        for link in paragraph.find_all("a"):
            new = link["href"]
            if new.startswith("/wiki/") and not new.startswith(("/wiki/Help:","/wiki/File:")) and "(" not in link.previous_element:
                if new == "/wiki/Philosophy":
                    print("----------")
                    print("Reached Philosophy in %s steps"%(count))
                    print("----------")
                    return None
                elif new in seen:
                    print("----------")
                    print("Reached a loop")
                    print("----------")
                    return None
                seen.append(new)
                return philosophyGame("https://en.wikipedia.org"+new,seen=seen,count=count+1)

print("----- Philosophy Game -----")
print("Legend has it that clicking the first link on a wikipedia page always leads to the page 'Philosophy'")
print("Test it out here!")
while True:
    print()
    print("Where would you like to start?")
    print("1. Wikepedia URL")
    print("2. Google a term")
    print("3. Random page")
    print("4. Exit")
    print()
    choice = int(input("Choose an option: "))
    print("----------")
    if choice == 1:
        search = input("Enter a wikipedia url: ")
        if search.startswith("https://en.wikipedia.org/wiki/"):
            try:
                philosophyGame(search)
            except:
                print("No internet connection you dingus")
        else:
            print("That's not a wikipedia url")
    elif choice == 2:
        headers = {
                'apikey': 'b9ee4b50-de6e-11e9-8e76-ebc82d7b87c0',
        }

        params = (
                ('q',input("Enter a search term: ")),
                ('location', 'Australia'),
                ('search_engine', 'google.com'),
                ('gl', 'AU'),
                ('hl', 'en'),
                ('num',100)
        )

        print("Searching google...")
        try:
            response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
            results = response.json()

            for result in results['organic']:
                    if 'url' in result and result['url'].startswith('https://en.wikipedia.org/wiki/'):
                            wiki = result['url']
                            break
            try:
                print("Found a wiki page:",wiki)
                philosophyGame(wiki)
            except:
                print("There were no wikipedia pages in the first 100 results")

        except:
            print("No internet connection you dingus")
            
    elif choice == 3:
        try:
            philosophyGame("https://en.wikipedia.org/wiki/Special:Random")
        except:
            print("No internet connection you dingus")
    elif choice == 4:
        print("Goodbye!")
        break
