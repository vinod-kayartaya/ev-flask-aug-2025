import requests


def main():
    title = input('Enter movie title to search: ')
    key = '30d67521'
    url = f'https://omdbapi.com/?apikey={key}&s={title}'
    r = requests.get(url)

    if r.status_code == 200:
        resp = r.json()
        movies = resp['Search']
        print(f'Found {resp['totalResults']} entries')
        print('-'*25)
        for m in movies:
            print(f'{m['Title']} --> {m['Year']}')
    else:
        print(f'Got an error: {r.text}')


if __name__ == '__main__':
    main()
