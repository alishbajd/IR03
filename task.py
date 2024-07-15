# Function to get common elements between two lists
def get_common_elements(list1, list2):
    # Convert the lists to sets
    set1 = set(list1)
    set2 = set(list2)
    set1= {'4, 10, 11, 12, 15, 18, 24, 34, 43, 52, 59, 73'} 
    set2 = {34, 4, 70, 71, 73, 10, 11, 15, 24, 59}
    
    # Find the intersection of the sets
    common_elements_set = set1.intersection(set2)
    
    print(common_elements_set)
    # Convert the set back to a list if you need a list as the result
    common_elements_list = list(common_elements_set)
    
    return common_elements_list

# Example usage
list1 = [4, 10, 11, 12, 15, 18, 24, 34, 43, 52, 59, 73]
list2 = [10, 11, 12, 15, 18, 24, 34, 59, 73, 75]

common_elements = get_common_elements(list1, list2)
print(f'Common elements: {common_elements}')
