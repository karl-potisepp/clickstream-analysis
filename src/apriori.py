# Apriori algorithm for Frequent Itemset Mining
# found from public domain

# count the frequent 1 itemsets
def freq_item_count(transactions, min_support):
    freq_item_list = {}

    for trans in transactions:
        for item in trans:
            if item in freq_item_list:
                freq_item_list[item]+=1
            else:

                freq_item_list[item]=1

    return [x for x in freq_item_list if freq_item_list[x]>=min_support]

# generate itemset_size+1-th candidates from itemset_size-th frequent itemsets
def candidate_gen(k_itemset, itemset_size):
    freq_set_list = []

    for s1 in k_itemset:
        for s2 in k_itemset:
            if itemset_size == 1:
                candidate = set([s1])|set([s2])
            else:
                candidate = set(s1)|set(s2)
            candidate = [x for x in candidate]
            if len(candidate) == itemset_size+1:
                if candidate not in freq_set_list:
                    freq_set_list+=[candidate]

    return freq_set_list

# prune the candidates
def prune(transactions, k_itemset, min_support):
    for candidate in k_itemset:
        if len([trans for trans in transactions if set(candidate)<=set(trans)])<min_support:
            k_itemset.remove(candidate)
    return k_itemset


def print_rules(transactions, min_support):
    itemsets = freq_item_count(transactions, min_support)
    itemset_size=0
    rules = []

    while len(itemsets)!=0:
        print "Itemsets of length %d: " % (itemset_size+1)
        for item in itemsets:
            print item
            
            if type(item) is not list:
                rules.append([item])
            rules.append(item)
    
        itemset_size+=1
        
        candiate_set = candidate_gen(itemsets, itemset_size)
        itemsets = prune(transactions, candiate_set, min_support)    
    
    return rules 

