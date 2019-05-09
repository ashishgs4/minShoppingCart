#!/usr/bin/env python
'''
Shopping Helper

Given a list of store inventories and a shopping list, return the minimum number of
store visits required to satisfy the shopping list.

For example, given the following stores & shopping list:

  Shopping List: 10 apples, 4 pears, 3 avocados, 1 peach

  Kroger: 4 apples, 5 pears, 10 peaches
  CostCo: 3 oranges, 4 apples, 4 pears, 3 avocados
  ALDI: 1 avocado, 10 apples
  Meijer: 2 apples

The minimum number of stores to satisfy this shopping list would be 3:
Kroger, CostCo and ALDI.
or
Kroger, CostCo and Meijer.

Shopping lists and store inventories will be passed in JSON format,
an example of which will be attached in the email.  Sample outputs for the
given inputs should also be attached as well.

Usage: shopping_helper.py (shopping_list.json) (inventories.json)
'''

import argparse
import copy
import json


# to help you get started, we have provided some boiler plate code
def satisfy_shopping_list(shopping_list_json, inventory_json):
    # find out minimum combination of stores that would satisfy shopping list
    stores = inventory_json['stores']
    stores_with_scores = {}
    #initialize node map
    for store in stores:
        current_score = getScore(store['inventory'], shopping_list_json)
        if current_score > 0:
            stores_with_scores[store['name']] = current_score
    combos = getStoreCombiations(stores_with_scores, stores, shopping_list_json)
    shopping_list_satisfiable = len(combos) > 0
    if shopping_list_satisfiable:
        # print out number of stores and corresponding combinations
        num_stores = len(combos) 
        print "The shopping list can be satisfied by visiting {} store(s):".format(num_stores)
        for combination in combos:
            print_store_combination(combination)
        pass
    else:
        print "No combination of given stores can satisfy this shopping list :("
        pass

def getStoreCombiations(scores, stores, shopping_list):
    combo = list()
    for i in range(2, len(stores)):
        test_set = [None]*i
        getCombiations(stores, copy.deepcopy(shopping_list), test_set, 0, len(stores), 0, i, combo)
    return combo

def getCombiations(stores, shopping_list, data, start, end, index, subset_size, valid_combinations): #create an n-ary tree of combos and recurse up to find the shortest branch
    if(index == subset_size):
        should_add = True 
        shopping_list_copy = copy.deepcopy(shopping_list)
        for k in range(subset_size):
            should_add = removeItemFromShoppingCart(data[k]['inventory'], shopping_list_copy)
            if not should_add :
                break
        if should_add and shoppingListValid(shopping_list_copy):
            valid_combo_list = []
            for d in data:
                valid_combo_list.append(d['name']) 
            valid_combinations.append(valid_combo_list)
    i = start
    while i < end and index < subset_size: 
        data[index] = stores[i]
        getCombiations(stores, shopping_list, data, i + 1, end, index + 1, subset_size, valid_combinations)
        i = i + 1

#Initial score based on the shopping list and inventory
def getScore(store, shopping_list):
    score = 0
    for item in shopping_list:
        for inventory in store:
            if item == inventory:
                score = score  + 1
                if store[inventory] >= shopping_list[item]:
                    score = score + 10
    return score


#Check if the shopping list is empty
def shoppingListValid(shopping_list_json):
    for key in shopping_list_json:
        if shopping_list_json[key] != 0:
            return False
    return True


def removeItemFromShoppingCart(inventory, shopping_list):
    score = False
    for item in shopping_list:
        if item in inventory and shopping_list[item] > 0:
            if inventory[item] >= shopping_list[item]:
                score = True
                shopping_list[item] = 0
            elif inventory[item] < shopping_list[item]:
                score = False
                shopping_list[item] = shopping_list[item] = inventory[item]
    return score


def print_store_combination(store_combination):
    '''
    Print store combination in the desired format.

    Args:
        store_combination: store list to print
        type: list of str
    '''
    store_combination_copy = copy.deepcopy(store_combination)
    store_combination_copy.sort()
    print ', '.join(store_combination_copy)

def main():
    args = parse_args()
    with open(args.shopping_list_json_path) as shopping_list_json_file, open(args.inventory_json_path) as inventory_json_file:
        shopping_list_json = json.load(shopping_list_json_file)
        inventory_json = json.load(inventory_json_file)
        satisfy_shopping_list(shopping_list_json, inventory_json)


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('shopping_list_json_path')
    p.add_argument('inventory_json_path')

    args = p.parse_args()
    return args


if __name__ == '__main__':
    main()
