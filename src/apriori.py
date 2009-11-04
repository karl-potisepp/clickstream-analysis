# Apriori algorithm for Frequent Itemset Mining
# found from public domain
# guess not very fast

# count the frequent 1 itemsets
import operator

# function for finding all frequent items from transactions
def freq_item_count(transactions, min_support):
    freq_item_list = {}

    # for every transaction
    for trans in transactions:
        # for each item in the transaction
        for item in trans:
            #if the item is already in the frequent item list, add 1 to item count
            if item in freq_item_list:
                freq_item_list[item]+=1
            #if item isn't on the frequent item list, initialize item count to 1
            else:
                freq_item_list[item]=1
    # for every counted item, if it's count is more or equal to min_support
    # return item
    return [x for x in freq_item_list if freq_item_list[x]>=min_support]

# generate itemset_size+1-th candidates from itemset_size-th frequent itemsets
def candidate_gen(k_itemset, itemset_size):
    freq_set_list = []

    for s1 in k_itemset:
        for s2 in k_itemset:
            #generate new itemsets by union of s1 and s2
            if itemset_size == 1:
                candidate = set([s1])|set([s2])
            else:
                candidate = set(s1)|set(s2)
            #convert candidate set to list
            candidate = [x for x in candidate]
            #only add those itemsets to resulting list that are exactly the size of itemset_size+1
            if len(candidate) == itemset_size+1:
                if candidate not in freq_set_list:
                    freq_set_list+=[candidate]

    return freq_set_list

# prune the candidates
def prune(transactions, k_itemset, min_support):
    for candidate in k_itemset:
        #if the number of transactions containing the candidate itemset is less than 
        #min_support, then the candidate is pruned
        if len([trans for trans in transactions if set(candidate)<=set(trans)])<min_support:
            k_itemset.remove(candidate)
    return k_itemset

# extracts all itemsets with support above min_support
def extract_itemsets(transactions, min_support):

    #list of all one element itemsets with support at least equal to min_support
    itemsets = freq_item_count(transactions, min_support)
    itemset_size=0
    rules = []

    while len(itemsets)!=0:
        for item in itemsets:
            if type(item) is not list:
                rules.append([item])
            else:
                rules.append(item)
    
        itemset_size+=1
        
        #generate new candidates
        candidate_set = candidate_gen(itemsets, itemset_size)
        #prune candidates that have less than min_support
        itemsets = prune(transactions, candidate_set, min_support)    
    
    return rules

def calculate_supports(rules, transactions):
    annotated = []
    for itemset1 in rules:
        ##count =  len([trans for trans in transactions if set(itemset)<=set(trans)])
        count = 0
        for trans in transactions:
            if set(itemset1)<=set(trans):
                count +=1
        annotated.append((count, itemset1))
        
    annotated = sorted(annotated, key=operator.itemgetter(0), reverse=True)        
    return annotated

#function to remove all non-maximal itemsets from rules
def extract_maximal_itemsets(rules):

    for superset in rules:
        for subset in rules:
            if set(superset)>=set(subset) and len(superset)!=len(subset):
                rules.remove(subset)

    return rules


def extract_closed_itemsets(items):
    
    closed = []
    while len(items) != 0:
        item = items.pop()
        closed.append(item)
        
        for remaining in items:
            if set(remaining) <= set(item):
                items.remove(remaining)
        
    
    return closed

def print_rules(itemsets):
    
    for rule in itemsets:
        print rule


