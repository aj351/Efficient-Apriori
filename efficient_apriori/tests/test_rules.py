#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 20:03:20 2018

@author: tommy
"""
import os
import pytest
import collections
import itertools
import random
import collections

from efficient_apriori.itemsets import itemsets_from_transactions
from efficient_apriori.rules import Rule, generate_rules_simple
from efficient_apriori.tests.test_itemsets import generate_transactions

def generate_rules_naively(itemsets, min_confidence):
    """
    Generate association rules naively, for testing purposes.

    """
    
    def proper_subsets(itemset:set):
        """
        Yield every proper subset of a set.
        """
        size = range(1, len(itemset))
        arg = [itertools.combinations(itemset, i) for i in size]
        yield from itertools.chain(*arg)
            
    def count(itemset):
        """
        Helper function to find the count of an itemset in the transactions.
        """
        return itemsets[len(itemset)][itemset]
    
    rules = []
    
    # For every itemset size greater than 1, yield every itemset of that size
    itemsets_gen = (iset for size in filter(lambda x: x > 1, itemsets.keys()) 
                    for iset in itemsets[size].keys())
        
    
    for itemset in itemsets_gen:
        count_full = count(itemset)
        
        # For every subset, get the difference, create a rule and check
        for lhs in proper_subsets(itemset):
            rhs = set(itemset).difference(set(lhs))
            rhs = tuple(sorted(list(rhs)))
            rule = Rule(lhs, rhs, count_full, count(lhs), count(rhs))
            
            # If the confidence of the rule is high enough, yield it
            if rule.confidence >= min_confidence:
                yield rule

input_data = [list(generate_transactions(num_transactions=random.randint(5, 25), 
                                    unique_items=random.randint(1, 8), 
                                    items_row=(1, random.randint(2, 8)))) 
                                    for i in range(10)]
@pytest.mark.parametrize("transactions", input_data)
def test_generate_rules_simple_vs_naive(transactions):
    """
    Test the naive rule finder vs. the simple one from the paper.
    """
    
    itemsets = itemsets_from_transactions(transactions, 0.5)
    
    min_conf = 0.5
    rules_naive = generate_rules_naively(itemsets, min_conf)
    rules_simple = generate_rules_simple(itemsets, min_conf)
    assert set(rules_naive) == set(rules_simple)


if __name__ == '__main__':
    pytest.main(args=['.', '--doctest-modules', '-v'])