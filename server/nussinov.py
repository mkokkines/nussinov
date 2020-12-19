import sys
import copy

def nussinov_alg(rna_sequence, base_pairings):
    n = len(rna_sequence)

    s = [[0] * n for x in range(n)]

    for i in range(n - 1, -1, -1):
        for j in range(n):

            vi = rna_sequence[i]
            vj = rna_sequence[j]

            if i >= j:
                0
            else:
                max_lst = []

                if (vj in base_pairings[vi]):
                    max_lst.append(s[i + 1][j - 1] + 1)
                else:
                    max_lst.append(s[i + 1][j - 1])

                max_lst.append(s[i + 1][j])
                max_lst.append(s[i][j - 1])

                max_skip = max([s[i][k] + s[k + 1][j] for k in range(i + 1, j)], default=0)
                max_lst.append(max_skip)

                s[i][j] = max(max_lst)

    return s

def traceback(s, seq, base_pairings):
    stacks = []
    traceback_lists = []
    paren_lists = []
    results = []

    initial_stack = []
    initial_stack.append((0, len(s) - 1))
    stacks.append(initial_stack)
    initial_traceback = []
    initial_traceback.append((0, len(s) - 1))
    traceback_lists.append(initial_stack)
    initial_paren_list = []
    paren_lists.append(initial_paren_list)

    while len(stacks) != 0:
        prev_stacks = copy.deepcopy(stacks)
        prev_traceback_lists = copy.deepcopy(traceback_lists)
        prev_paren_lists = copy.deepcopy(paren_lists)

        stacks = []
        traceback_lists = []
        paren_lists = []

        for i in range(len(prev_stacks)):
            stack = prev_stacks[i]
            traceback_list = prev_traceback_lists[i]
            paren_list = prev_paren_lists[i]
            
            if len(stack) == 0:
                results.append((traceback_list, paren_list))
                continue
            
            i, j = stack.pop()
            if i >= j:
                stacks.append(stack)
                traceback_lists.append(traceback_list)
                paren_lists.append(paren_list)
                continue
            
            if s[i + 1][j] == s[i][j]:
                stack_c = copy.deepcopy(stack)
                traceback_c = copy.deepcopy(traceback_list)
                paren_list_c = copy.deepcopy(paren_list)
                
                stack_c.append((i + 1, j))
                traceback_c.append((i + 1, j))
               
                stacks.append(stack_c)
                traceback_lists.append(traceback_c)
                paren_lists.append(paren_list_c)

            if s[i][j - 1] == s[i][j]:
                stack_c = copy.deepcopy(stack)
                traceback_c = copy.deepcopy(traceback_list)
                paren_list_c = copy.deepcopy(paren_list)

                stack_c.append((i, j - 1))
                traceback_c.append((i, j - 1))

                stacks.append(stack_c)
                traceback_lists.append(traceback_c)
                paren_lists.append(paren_list_c)

            if s[i + 1][j - 1] + 1 == s[i][j] and seq[i] in base_pairings[seq[j]]:
                stack_c = copy.deepcopy(stack)
                traceback_c = copy.deepcopy(traceback_list)
                paren_list_c = copy.deepcopy(paren_list)

                stack_c.append((i + 1, j - 1))
                traceback_c.append((i + 1, j - 1))
                paren_list_c.append((i, j))
                                      
                stacks.append(stack_c)
                traceback_lists.append(traceback_c)
                paren_lists.append(paren_list_c)

            for k in range(i + 1, j):
                if s[i][k] + s[k + 1][j] == s[i][j]:
                    stack_c = copy.deepcopy(stack)
                    traceback_c = copy.deepcopy(traceback_list)
                    paren_list_c = copy.deepcopy(paren_list)

                    stack_c.append((k + 1, j))
                    stack_c.append((i, k))
                    traceback_c.append((k + 1, j))
                    traceback_c.append((i, k))

                    stacks.append(stack_c)
                    traceback_lists.append(traceback_c)
                    paren_lists.append(paren_list_c)
                
    return results

def get_dot_parentheses_notation(s, traceback_list):
    string = ['.'] * len(s)
    for (i, j) in traceback_list:
        string[i] = '('
        string[j] = ')'
    return ''.join(string)