# -*- coding: utf-8 -*-
# Accessory functions
import amazonproduct
import utils
import blurb.utils
import time
import random

config = {
    'access_key': 'AKIAJAEPJ2CLFMQOKA5A',
    'secret_key': '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',
    'associate_tag': 'blurber-20',
    'locale': 'us'
}

#hard coded for now. call -> getCategoriesOfBooks() for automating it.
# node_ids_genre = ["25", "23"]
# List of tuples [(title,author,desc),(title,author,desc), . . .]
def getBooksFromAmazon():
    """
    :return: Dictionary of {genre_id: [(title, author, descr)...]
    Retrieve the book data from Amazon with the API
    """
    num_records = 10
    genre_dict = getGenreId_GenreName(1000)
    node_ids_genre = genre_dict.keys()
    #node_ids_genre = [25]
    books_dict = {}
    api = amazonproduct.API(cfg=config)
    for alphabet in node_ids_genre:
        print "Genre: " + str(alphabet)
        allbookscount = 0
        lst_tuple = []
        #Expand the data set to thousands
        #inner_children = getCategoriesOfBooks(alphabet)
        #for child in inner_children:
        time.sleep(1)
        items = api.item_search('Books', BrowseNode=alphabet,ResponseGroup="EditorialReview,ItemAttributes,BrowseNodes")
        tup = ()
        count = 0
        #if(len(items) < 3):
        #    continue
        for book in items:
            #print '%s' % book.EditorialReviews.EditorialReview.Content
            #print '%s: "%s"' % (book.ItemAttributes.Author,book.ItemAttributes.Title)
            try:
                tup = (book.ItemAttributes.Title, book.ItemAttributes.Author, blurb.utils.dehtml(book.EditorialReviews.EditorialReview.Content))
            except AttributeError:
                continue

            lst_tuple.insert(count, tup)
            count += 1
            allbookscount += 1
            if allbookscount >= num_records:
                break
        books_dict[alphabet] = lst_tuple
    return books_dict


def getCategoriesOfBooks(nodeid):
    api = amazonproduct.API(cfg=config)
    node_id = nodeid
    result = api.browse_node_lookup(node_id)
    list_of_child_nodes = []
    i = 0
    for child in result.BrowseNodes.BrowseNode.Children.BrowseNode:
        #print '%s (%s)' % (child.Name, child.BrowseNodeId)
        list_of_child_nodes.insert(i, child.BrowseNodeId)
        i += 1
    return list_of_child_nodes


def getGenreId_GenreName(nodeid):
    # Call with 1000 as input
    api = amazonproduct.API(cfg=config)
    node_id = nodeid
    result = api.browse_node_lookup(node_id)
    dict_of_child_nodes = {}
    i = 0
    for child in result.BrowseNodes.BrowseNode.Children.BrowseNode:
        #print '%s (%s)' % (child.Name, child.BrowseNodeId)
        dict_of_child_nodes[child.BrowseNodeId] = child.Name
        i += 1
    return dict_of_child_nodes

def getRandomBooks(all_genre_dict):
    """
    :param all_genre_dict: {genre_id, tuple list}
    :return: [(titles, authors, descr)...]
    """
    #print "Randomness"
    all_random_tuples = []
    i = 0
    for gen_dict in all_genre_dict:
        all_random_tuples.append(all_genre_dict[gen_dict])
    one_list = []
    for tup in all_random_tuples:
        for one_tup in tup:
            one_list.append(one_tup)

    return one_list
