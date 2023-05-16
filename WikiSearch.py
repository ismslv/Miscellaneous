import requests
import operator


def wikipedia_search(query, languages, pages_limit, results_limit, sort="size", exact=True):
    """
    Search in the text of wikipedia articles
    :param query: text to search, without quotes
    :param languages: list of wikipedia locales to search in
    :param pages_limit: how many pages to search in for each language
    :param results_limit: how many results to show combined
    :param sort: what to sort results by (title, size, lang), default is "size"
    :param exact: search for entire input as is, default is True
    :return:
    """
    # Surround with quotes if query must be exact
    if exact:
        query = f'"{query}"'

    results = []
    for lang in languages:
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "utf8": 1,
            "srsearch": query,
            "srlimit": pages_limit,
            "srinterwiki": 1,
        }

        response = requests.get(url, params=params).json()

        for item in response['query']['search']:
            results.append({
                "title": item['title'],
                "size": item['size'],
                "lang": lang
            })

    # Sort by size
    results.sort(key=operator.itemgetter(sort), reverse=True)

    # Trim to results limit
    results = results[:results_limit]

    # Print
    for result in results:
        print(f"Title: {result['title']}, Size: {result['size']}, Language: {result['lang']}")


wikipedia_search(
    query="絵文字",
    languages=['en', 'jp'],
    pages_limit=100,
    results_limit=20,
    sort="size",
    exact=True
)

# Suggested changes to the code:
#   [Required]
#     - internet error handling
#     - check for incorrect input (negative limits, empty query)
#     - check if languages exist in wikipedia (add the langs list)
#   [Suggested]
#     - output language name instead of shortcode
#     - output warning if result is empty
#     - show progress indication
#     - alternative cases (search without limits etc.)
