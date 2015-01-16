#class NCM:
#    ?
# import pdb
# pdb.set_trace()
class NCMParser:
    def __init__(self, dot_bracket):
        self.dot_bracket = dot_bracket

ncm = {}

dot_bracket_index = 0 # dbg

def parse(dot_bracket, dangling=0):
    global dot_bracket_index # dbg
    open_var = False
    unpaired_left = 0
    while dot_bracket:
        x = dot_bracket.pop(0)
        dot_bracket_index += 1
        if x == "." and dangling > 0:
            unpaired_left += 1
        elif x == "(":
            dangling += 1
            unpaired_right, end = parse(dot_bracket, dangling)
            dangling -= 1
            open_var = True
            if not end:
                print "left : " + str(unpaired_left) + ", right : " + str(unpaired_right) + ", dangling : " + str(dangling) + ", index : " + str(dot_bracket_index)
            # get_ncm(unpaired_left, unpaired_right)
        elif x == ")":
            if unpaired_left and not open_var:
                print "single of " + str(unpaired_left)
                return 0, False
            if dangling == 1:
                return 0, True
            return unpaired_left, False

if __name__ == "__main__":
    # p = NCMParser("..((.)).")

    # parse(list("..((.))."))
    parse(list("..((((...)))).....(.(.(...)).).((((......)).....))."))
# ..((((...)))).....(.(.(...)).).((((......)).....))."))
