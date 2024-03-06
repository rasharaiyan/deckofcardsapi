import requests

class DeckOfCardsAPI:
    BASE_URL = "https://deckofcardsapi.com/api/deck"

    def __init__(self):
        pass

    def shuffle_deck(self, deck_count=1):
        endpoint = f"{self.BASE_URL}/new/shuffle/"
        params = {'deck_count': deck_count}
        response = requests.get(endpoint, params=params)
        return response

    def draw_cards(self, deck_id, count=2):
        endpoint = f"{self.BASE_URL}/{deck_id}/draw/"
        params = {'count': count}
        response = requests.get(endpoint, params=params)
        return response

    def reshuffle_deck(self, deck_id, remaining=True):
        endpoint = f"{self.BASE_URL}/{deck_id}/shuffle/"
        params = {'remaining': 'true' if remaining else 'false'}
        response = requests.get(endpoint, params=params)
        return response

    def create_new_deck(self):
        endpoint = f"{self.BASE_URL}/new/"
        response = requests.get(endpoint)
        return response


    def create_partial_deck(self, cards):
        endpoint = f"{self.BASE_URL}/new/shuffle/"
        params = {'cards': cards}
        response = requests.get(endpoint, params=params)
        return response


    def add_cards_to_pile(self, deck_id, pile_name, cards):
        endpoint = f"{self.BASE_URL}/{deck_id}/pile/{pile_name}/add/"
        params = {'cards': cards}
        response = requests.get(endpoint, params=params)
        return response
    def shuffle_pile(deck_id, pile_name):
        endpoint = f"{DeckInfra.BASE_URL}/{deck_id}/pile/{pile_name}/shuffle/"
        response = requests.get(endpoint)
        return response.json()
