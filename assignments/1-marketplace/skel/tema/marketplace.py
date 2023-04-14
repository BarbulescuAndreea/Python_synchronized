"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import unittest
from threading import Lock, Semaphore

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the
    implementation. The producers and consumers use its methods concurrently.
    """
    # keep the corespondence between the producers and their actual_products
    producers = {}
    # variable which is used to increment for assigning the unique identifier of a
    # new cart
    cart_indentifier_update = 0
    # mapping of cart identifiers to item lists, implemented as a dictionary of lists.
    official_carts = {}
    # the actual_products that exists in the marketplace
    actual_products = []
    # mapping between the producer and number of items
    producers_nr_of_actual_products = []

    def __init__(self, queue_size_per_producer):
        """
        Constructor.
        """
        self.publication_limit = queue_size_per_producer
        self.general_lock = Lock()
         # Semphore used to safe-increment the unique value for cart_id and register_id
        self.cart_id_semaphore = Semaphore(value=1)
        self.semaphore_register = Semaphore(value=1)
        self.semaphore_aux = Semaphore(value=1)

    def register_producer(self):
        """ 
        This function returns an ID for the producer. 
        The ID is equal to the producer's index in the list of queue sizes, 
        which represents the position of the producer's queue in the queue 
        manager. This ID can be used by the producer to uniquely identify 
        its own queue and to access its associated resources.
        """
        # The length of the queue sizes may be changed by another registration
        # before this one appends, thus a lock is needed.
        self.semaphore_register.acquire()
        self.producers_nr_of_actual_products[:] = [0] + self.producers_nr_of_actual_products
        # setting prod_id to the index of the last element in the
        # self.producers_nr_of_actual_products list
        nr_prod = len(self.producers_nr_of_actual_products)
        prod_id = nr_prod - 1
        self.producers[prod_id] = True
        self.semaphore_register.release()
        return prod_id

    def publish(self, producer_id, product):
        """ 
        This method adds a new product to the marketplace and associates it with the 
        producer that provided it. It increases the producer's queue size by one to 
        reflect the new addition. The method takes two parameters: the product itself, 
        and the producer_id of the producer that provided it.
        """
        prod_id = int(float(producer_id))
        # If the maximum limit of actual_products for a producer is achieved, then the
        # producer must wait, he can't publish it in that moment
        length = self.producers_nr_of_actual_products[prod_id]
        if length <= self.publication_limit:
            # lock used here because the insert method is not thread-safe
            with self.general_lock:
                self.actual_products.insert(0, product)
            # adding 1 to the size of the actual_products that a producer has
            self.producers_nr_of_actual_products[prod_id] =\
                 self.producers_nr_of_actual_products[prod_id] + 1
            # add the product to the corespondent producer in the producers map.
            self.producers.update({product: prod_id})
            result = True
        else:
            result = False
        return result

    def new_cart(self):
        """ 
        A new cart is created with a unique ID, and a new entry is added 
        to the official_carts dictionary for this cart. The incrementation must be done
        thread-safe, that's why I used a semaphore with value one(equivalent to
        a mutex)
        """
        self.cart_id_semaphore.acquire()
        self.cart_indentifier_update = self.cart_indentifier_update + 1
        cart_id = self.cart_indentifier_update
        self.official_carts[cart_id] = [].copy()
        self.cart_id_semaphore.release()
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        This function adds a product to a cart, which involves removing it 
        from the producer's queue and decrementing the number of goods in that queue.
        """
        # if the cart_id does not exist, return False
        if cart_id not in self.official_carts:
            return False
        # check if the product exists in the existent actual_products
        if product in self.actual_products:
            self.actual_products.remove(product)
            self.semaphore_aux.acquire()
            try:
                producer_id = self.producers[product]
            except KeyError:
                producer_id = None
            # using the semaphore(lock) so multiple threads can t perform to
            # remove the same product at the same time, and insert is not thread-safe
            #self.actual_products = [p for p in self.actual_products if p != product]
            # remove the actual_products from the list of actual_products because it's going
            # to the cart, so the stock is equal to the stock - 1
            self.producers_nr_of_actual_products[producer_id] =\
                self.producers_nr_of_actual_products[producer_id] - 1
            self.official_carts[cart_id].insert(0, product)
            self.semaphore_aux.release()
            result = True
        else:
            result = False
        return result

    def remove_from_cart(self, cart_id, product):
        """
        This function removes a product from a cart, and returns it to the marketplace
        by incrementing the product's producer's queue size. This makes the
        product available for purchase again.
        """
        self.semaphore_aux.acquire()
        self.official_carts[cart_id].remove(product)
        self.actual_products.insert(0, product)
        producer_id = self.producers[product]
        self.producers_nr_of_actual_products[producer_id] =\
            self.producers_nr_of_actual_products[producer_id] + 1
        self.semaphore_aux.release()

    def place_order(self, cart_id):
        """
        Keep a list with all the items in the cart.
        """
        purchased_items = self.official_carts.get(cart_id, None)
        # If the cart_id key exists, we delete it from the cart using the del statement
        if purchased_items is not None:
            del self.official_carts[cart_id]
        return purchased_items

class TestMarketplace(unittest.TestCase):
    """
    Class used to test the functionalities of the marketplace
    """
    def setUp(self):
        self.marketplace = Marketplace(queue_size_per_producer=10)

    def test_register_producer(self):
        """
        The function tests particular case in order to check if the 
        register_producer works fine.
        """
        # test registering a producer
        self.marketplace.register_producer()
        self.assertIn(0, self.marketplace.producers)

        # verify if multiple producers can be added in the producers list
        self.marketplace.register_producer()
        self.marketplace.register_producer()
        self.assertIn(1, self.marketplace.producers)
        self.assertIn(2, self.marketplace.producers)

    def test_publish(self):
        """
        The function tests particular case in order to check if
        publishing a product on marketplace works fine.
        """
        # register a producer
        self.marketplace.register_producer()

        # publish a product
        producer_id = 0
        product = "Tea"
        # test trying to publish a product
        self.marketplace.publish(producer_id, product)
        # verify if the product is now in the Marketplace
        self.assertIn(product, self.marketplace.actual_products)
        # verify the right correspondence between the product and it s producer
        self.assertEqual(self.marketplace.producers[product], producer_id)
        # verify if the nr of actual_products for a producer has been increased
        self.assertEqual(self.marketplace.producers_nr_of_actual_products[producer_id], 1)

    def test_new_cart(self):
        """
        The function tests particular case in order to check if
        creating a new cart works fine.
        """
        # test creating a new cart
        cart_id = self.marketplace.new_cart()
        # verify if the function returns the cart_id
        self.assertIsNotNone(cart_id)
        # verify if the cart_id is in the official_carts
        self.assertIn(cart_id, self.marketplace.official_carts)
        # verify if the cart_id is unique
        cart_id_2 = self.marketplace.new_cart()
        self.assertNotEqual(cart_id_2, cart_id)
        # verify if cart_id_2 is right added in official_carts
        self.assertIn(cart_id_2, self.marketplace.official_carts)

    def test_add_to_cart(self):
        """
        The function tests particular case in order to check if
        adding a new product to the cart works fine.
        """
        # register producer, create product and new cart to be able to test
        # add_to_cart
        self.marketplace.register_producer()
        producer_id = 0
        product = "Tea"
        self.marketplace.publish(producer_id, product)
        cart_id = self.marketplace.new_cart()
        result = self.marketplace.add_to_cart(cart_id, product)
        self.assertTrue(result)
        # verify if the product is in the corresponding cart
        self.assertIn(product, self.marketplace.official_carts[cart_id])
        # verify that you cannot add a product into an invalid cart
        self.marketplace.publish(producer_id, product)
        result = self.marketplace.add_to_cart(100, product)
        self.assertFalse(result)
        # adding an inexistent product should end into an error
        result = self.marketplace.add_to_cart(cart_id, "Invalid product")
        self.assertFalse(result)
        self.assertNotIn("Invalid product", self.marketplace.official_carts[cart_id])

    def test_remove_from_cart(self):
        """
        The function tests particular case in order to check if
        removing a product from the cart works fine.
        """
        # add a product to cart
        self.marketplace.register_producer()
        producer_id = 0
        product = "Tea"
        self.marketplace.publish(producer_id, product)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, product)
        # test removing the product from that cart
        self.marketplace.remove_from_cart(cart_id, product)
        # verify if the product is now back in marketplace
        self.assertIn(product, self.marketplace.actual_products)
        # verify if the cart is now empty
        self.assertEqual(self.marketplace.official_carts[cart_id], [])

    def test_place_order(self):
        """
        The function tests particular case in order to check if
        placing an order works fine.
        """
        self.marketplace.register_producer()
        producer_id = 0
        product = "Tea"
        self.marketplace.publish(producer_id, product)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, product)
        # place the order
        purchased_items = self.marketplace.place_order(cart_id)
        # verify if the purchased_items are present
        self.assertIsNotNone(purchased_items)
        # verify if the purchased_items contains the right item
        self.assertIn("Tea", purchased_items)
        # verify that the cart is removed from the marketplace
        self.assertNotIn(cart_id, self.marketplace.official_carts)
        # verify placing an order for an inexistent cart
        result = self.marketplace.place_order(999)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
    