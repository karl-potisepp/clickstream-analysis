# Apriori algorithm for Frequent Itemset Mining
# found from public domain

def freq_item_count(transactions, min_support):
    """function for finding all frequent 1-items from transactions"""
    freq_item_list = {}

    for trans in transactions:
        for item in trans:
            if item in freq_item_list:
                freq_item_list[item]+=1
            else:
                freq_item_list[item]=1
    sets = []
    support_db = {}
    for x in freq_item_list:
        if freq_item_list[x]>=min_support:
            sets.append(x)
            support_db[tuple(x)] = freq_item_list[x]
    return sets, support_db

def candidate_gen(k_itemset, itemset_size):
    """generate itemset_size+1-th candidates from itemset_size-th frequent itemsets"""
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
    hold = []
    supports = {}
    for candidate in k_itemset:
        candidate_support = len([trans for trans in transactions if set(candidate)<=set(trans)])
        
        if candidate_support >=min_support:
            supports.setdefault(tuple(candidate), candidate_support)
            hold.append(candidate)
    return hold, supports

# extracts all itemsets with support above min_support
def extract_itemsets(transactions, min_support):

    #list of all one element itemsets with support at least equal to min_support
    itemsets, support_db = freq_item_count(transactions, min_support)
    itemset_size=0
    rules = []
    supports = {}

    
    while len(itemsets)!=0:
        for item in itemsets:
            add = item
            if type(item) is not list:
                add = [item]
            supports[tuple(add)] = support_db[tuple(item)]
            rules.append(add)
        itemset_size+=1
        
        #generate new candidates
        candidate_set = candidate_gen(itemsets, itemset_size)
        #prune candidates that have less than min_support
        itemsets, support_db = prune(transactions, candidate_set, min_support)    
    
    return filter_duplicates(rules, supports)

def filter_duplicates(rules, supports):
  filtered = []
  for item in rules:
    add = True
    for g in filtered:
      if set(item) == set(g):
        add = False
    if add: filtered.append(item)
  
  return filtered

def extract_closed_itemsets(items, supports):
    def present(closed, item):
        for i in closed:
            if set(i) == set(item):
                return True
        return False
    max = len(items[-1])
    closed = []
    
    for item in items:
        support = supports[tuple(item)]
        #size = len(item)
        if len(item) == max and not present(closed, item):
            closed.append(item)
            continue
        for remaining in items:
            if set(remaining) >= set(item) and supports[tuple(remaining)] < support and not present(closed, item):
                  closed.append(item)
                  break
    
    return closed
