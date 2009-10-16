# Apriori algorithm for Frequent Itemset Mining

# count the frequent 1 itemsets
def freq_item_count(transactions, min_support):
  freq_item_list = {}

  for trans in transactions:
    for item in trans:
      if item in freq_item_list:
        freq_item_list[item]+=1
      else:
        #freq_item_list.update({item:1})
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

  while len(itemsets)!=0:
    print "Itemsets of length %d: " % (itemset_size+1)
    for item in itemsets:
      print item
  
    itemset_size+=1
    
    candiate_set = candidate_gen(itemsets, itemset_size)
    itemsets = prune(transactions, candiate_set, min_support)   

def demo():

  transactions = [[1,2,3,4,5,6,7,8],
        [1,2,3,4,5,8,9,10],
        [1,2,3,4,7,8,9,10,11],
        [2,3,4,5,6,7,8,9,29],
        [3,5,6,7,8,12,22],
        [5,6,7,9,12,32],
        [11,23,123,324]
        ]

  min_support = 5
  print_rules(transactions, min_support)           

if __name__ == "__main__":
  demo()