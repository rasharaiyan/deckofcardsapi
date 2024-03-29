import requests
from infra.api_wrapper import DeckOfCardsAPI

class DeckLogic:


    def __init__(self):
        self.client = DeckOfCardsAPI()

    def shuffle_and_get_deck(self, deck_count=1):
        response = self.client.shuffle_deck(deck_count)
        return response.json()

    def draw_cards_from_deck(self, deck_id, count=2):
        response = self.client.draw_cards(deck_id, count)
        return response.json()

    def reshuffle_deck(self, deck_id, remaining=True):
        response = self.client.reshuffle_deck(deck_id, remaining)
        return response.json()

    def create_new_deck(self):
        response = self.client.create_new_deck()
        return response.json()

    def create_and_shuffle_partial_deck(self, cards):
        response = self.client.create_partial_deck(cards)
        return response.json()

    def add_cards_to_pile(self, deck_id, pile_name, cards):
        try:
            response = self.client.add_cards_to_pile(deck_id, pile_name, cards)
            return response
        except requests.RequestException as e:
            # Handle any network or HTTP-related errors
            print(f"Error occurred: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error occurred: {e}")
            return {'success': False, 'error': str(e)}

    def shuffle_piles(self, deck_id, pile_name):
        try:
            response = self.client.shuffle_piles(deck_id, pile_name)
            return response
        except requests.RequestException as e:
            # Handle any network or HTTP-related errors
            print(f"Error occurred: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error occurred: {e}")
            return {'success': False, 'error': str(e)}

