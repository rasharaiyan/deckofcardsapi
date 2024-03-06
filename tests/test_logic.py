import unittest
from logic.DeckManager import DeckLogic


class TestDeckAPI(unittest.TestCase):
    def setUp(self):
        self.logic = DeckLogic()
        new_deck_response = self.logic.shuffle_and_get_deck()
        self.assertTrue(new_deck_response['success'])
        self.deck_id = new_deck_response['deck_id']

    def test_shuffle_deck(self):
        # Test that the deck can be shuffled and check response
        response = self.logic.shuffle_and_get_deck()
        self.assertEqual(response['success'], True)
        self.assertIn('deck_id', response)
        self.assertEqual(response['shuffled'], True)
        self.assertEqual(response['remaining'], 52)

    def test_draw_cards(self):
            # Test drawing two cards and validate the dynamic response structure
        response = self.logic.draw_cards_from_deck(count=2)

            # Check basic response structure
        self.assertEqual(response['success'], True)
        self.assertIsNotNone(response['deck_id'])
        self.assertEqual(len(response['cards']), 2)
        self.assertEqual(response['remaining'], 50)

            # Define valid values for cards
        valid_suits = {"HEARTS", "DIAMONDS", "CLUBS", "SPADES"}
        valid_values = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "JACK", "QUEEN", "KING", "ACE"}

            # Validate each drawn card
        for card in response['cards']:
            self.assertIn(card['suit'], valid_suits)
            self.assertIn(card['value'], valid_values)
            self.assertIsNotNone(card['code'])
            # Check that the 'image' URL starts with the expected base path. This ensures that the image URL is correctly formatted and points to the expected server and directory. It's a way to validate that the response includes a valid image URL for the standard (non-SVG, non-PNG) card image.
            self.assertTrue(card['image'].startswith('https://deckofcardsapi.com/static/img/'))
            # Check that the SVG image URL (accessible via 'images.svg') starts with the expected base path. This is important for verifying that the SVG version of the card image is correctly hosted and provided, ensuring it points to the right server and directory for SVG images.
            self.assertTrue(card['images']['svg'].startswith('https://deckofcardsapi.com/static/img/'))
            # Check that the PNG image URL (accessible via 'images.png') starts with the expected base path. Similar to the SVG check, this ensures the PNG version of the card image is correctly hosted and provided, confirming it points to the correct server and directory for PNG images.
            self.assertTrue(card['images']['png'].startswith('https://deckofcardsapi.com/static/img/'))

    def test_reshuffle_deck(self):
        # Test reshuffling the deck and validate the response using the dynamically obtained deck_id
        response = self.logic.reshuffle_deck(self.deck_id)

        # Check basic response structure and values
        self.assertEqual(response['success'], True)
        self.assertEqual(response['shuffled'], True)
        self.assertEqual(response['deck_id'], self.deck_id)
        self.assertEqual(response['remaining'], 52)

    def test_create_new_deck(self):
        # Test creating a new deck and validate the response
        response = self.logic.create_new_deck()
        # Check basic response structure and values
        self.assertEqual(response['success'], True)
        self.assertIsInstance(response['deck_id'], str)
        self.assertEqual(response['shuffled'], False)
        self.assertEqual(response['remaining'], 52)

    def test_create_and_shuffle_partial_deck(self):
        # Specific cards for partial deck
        cards = 'AS,2S,KS,AD,2D,KD,AC,2C,KC,AH,2H,KH'

        # Test creating and shuffling a partial deck and validate the response
        response = self.logic.create_and_shuffle_partial_deck(cards)

        # Check basic response structure and values
        self.assertEqual(response['success'], True)
        self.assertIsInstance(response['deck_id'], str)  # We ensure that a deck_id is provided and is a string type.
        self.assertEqual(response['shuffled'], True) # We confirm that the deck is indeed shuffled
        self.assertEqual(response['remaining'], 12) #We verify that the number of cards remaining in the deck matches the number of specified cards


    def test_draw_cards_from_deck(self):
        # Create a new deck to ensure the test is isolated
        new_deck_response = self.logic.create_new_deck()
        self.assertTrue(new_deck_response['success'])
        deck_id = new_deck_response['deck_id']
        initial_remaining = new_deck_response['remaining']  # Capture the initial number of cards

        # Number of cards to draw
        cards_to_draw = 2

        # Draw cards from the newly created deck
        draw_response = self.logic.draw_cards_from_deck(deck_id, count=cards_to_draw)

        # Check basic response structure and values
        self.assertEqual(draw_response['success'], True)
        self.assertEqual(draw_response['deck_id'], deck_id)
        self.assertEqual(len(draw_response['cards']), cards_to_draw)  # Verify the number of drawn cards
        self.assertIsInstance(draw_response['remaining'], int)  # Ensure 'remaining' is an integer

        # Calculate and assert the expected number of remaining cards dynamically
        expected_remaining = initial_remaining - cards_to_draw
        self.assertEqual(draw_response['remaining'], expected_remaining)


        valid_suits = {"HEARTS", "DIAMONDS", "CLUBS", "SPADES"}
        for card in draw_response['cards']:
            self.assertIn(card['suit'], valid_suits)
            self.assertIn(card['value'], {"2", "3", "4", "5", "6", "7", "8", "9", "10", "JACK", "QUEEN", "KING", "ACE"})
            self.assertTrue(card['image'].startswith('https://deckofcardsapi.com/static/img/'))
            self.assertTrue(card['images']['svg'].startswith('https://deckofcardsapi.com/static/img/'))
            self.assertTrue(card['images']['png'].startswith('https://deckofcardsapi.com/static/img/'))

    def test_add_cards_to_pile(self):
        # Create a new deck to ensure the test is isolated
        new_deck_response = self.logic.create_new_deck()
        self.assertTrue(new_deck_response['success'])
        deck_id = new_deck_response['deck_id']

        # Name of the pile
        pile_name = "player1Hand"

        # Cards to add to the pile
        cards = "AS,AD"

        # Add cards to the specified pile
        add_cards_response = self.logic.add_cards_to_pile(deck_id, pile_name, cards)

        # Check if the request was successful
        if add_cards_response['success']:
            # Check basic response structure and values
            self.assertEqual(add_cards_response['deck_id'], deck_id)
        else:
            # If the request failed, print the error message
            print(f"Error occurred: {add_cards_response['error']}")

        # Assert the success status returned from the function
        self.assertEqual(add_cards_response['success'], True)

    def test_shuffle_piles(self):

        deck_id = "77vjh43p4f2u"
        pile_name = "player1Hand"

        # Shuffle the piles
        shuffle_response = self.logic.shuffle_piles(deck_id, pile_name)

        # Check if the request was successful
        self.assertTrue(shuffle_response['success'])

        # Check if the deck_id returned is correct
        self.assertEqual(shuffle_response['deck_id'], deck_id)

        # Check if the remaining cards in the deck are as expected
        self.assertEqual(shuffle_response['remaining'], 8)
        # Check if the pile exists and contains the correct number of cards
        self.assertIn('piles', shuffle_response)
        self.assertIn(pile_name, shuffle_response['piles'])
        self.assertEqual(shuffle_response['piles'][pile_name]['remaining'], 2)