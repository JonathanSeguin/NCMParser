#!/usr/bin/python

class NCMParser:

    def __init__(self):
        self.NCM = {
                1: {
                     3: "1_3",
                     4: "1_4",
                     5: "1_5",
                     6: "1_6"
                      },
                2: {
                     2: {
                           2: "2_2_2",
                           3: "2_2_3",
                           4: "2_2_4",
                           5: "2_2_5"
                            },
                     3: {
                           2: "2_3_2",
                           3: "2_3_3",
                           4: "2_3_4",
                           5: "2_3_5"
                            },
                     4: {
                           2: "2_4_2",
                           3: "2_4_3",
                           4: "2_4_4"
                            },
                     5: {
                           2: "2_5_2",
                           3: "2_5_3"
                            }
                        }
                    }
        self.ncms = []

    def _check_intersection(self, dot_bracket, reverse=False, left=0):
        stack = 0
        o_stack = 0
        first_dangling = 0
        closing = False
        if reverse:
            openchar = ")"
            closechar = "("
        else:
            openchar = "("
            closechar = ")"
        for i, x in enumerate(dot_bracket):
            if x == openchar:
                o_stack += 1
                if closing and stack == 1:
                    if reverse:
                        try:
                            # print self.NCM[2][left + 2][first_dangling + 2]
                            self.ncms.append(self.NCM[2][left + 2][first_dangling + 2])
                        except:
                            pass
                        return dot_bracket[first_dangling + 1:][::-1]
                    else:
                        return self._check_intersection(dot_bracket[first_dangling + 1:][::-1], reverse=True, left=first_dangling)
                else:
                    stack += 1
                    closing = False
            if x == closechar:
                stack -= 1
                closing = True
            if x == "." and o_stack < 1:
                first_dangling += 1

        if reverse:
            try:
                # print self.NCM[2][left + 2][first_dangling + 2]
                self.ncms.append(self.NCM[2][left + 2][first_dangling + 2])
            except:
                pass
            return dot_bracket[first_dangling + 1:][::-1]
        return dot_bracket

    def _parse_helix(self, dot_bracket, b_idx, e_idx, first=True):
        intersection = self._check_intersection(dot_bracket)
        orig_dot_bracket = dot_bracket # ?

        if intersection != orig_dot_bracket:
            try:
                self.ncmparser(intersection)
                return 0
            except:
                pass

        if len(dot_bracket) > 1:
            l = dot_bracket.pop(0) # left
            r = dot_bracket.pop() # right
            r_cnt = 1 # left count
            l_cnt = 1 # right count
        elif len(dot_bracket) == 1:
            l = dot_bracket.pop()
            l_cnt = 1
        else:
            return 0

        while l == ".":
            try:
                l = dot_bracket.pop(0)
                l_cnt += 1
            except:
                try:
                    print "[ %s ] ncm_nuc_idx : %s, neighbor_idx : %s" % (self.NCM[1][l_cnt + r_cnt + 2],
                            range(b_idx - 1, e_idx + 1), "?")
                    self.ncms.append(self.NCM[1][l_cnt + r_cnt + 2])
                except:
                    pass
                return 0

        while r == ".":
            r_cnt += 1
            r = dot_bracket.pop()

        self._parse_helix(dot_bracket, b_idx + l_cnt, e_idx - r_cnt, False)

        if not first:
            try:
                print "[ %s ] ncm_nuc_idx : %s, neighbor_idx : %s" % (self.NCM[2][l_cnt + 1][r_cnt + 1],
                        range(b_idx - 1, b_idx + l_cnt) + range(e_idx - r_cnt, e_idx + 1), "?")
                self.ncms.append(self.NCM[2][l_cnt + 1][r_cnt + 1])
            except:
                pass

        return 0

    def ncmparser(self, dot_bracket):
        o_stack = 0 # open stack
        c_stack = 0 # close stack
        b_idx = 0 # helix beginning index
        e_idx = 0 # helix end index

        # Check for a first intersection
        dot_bracket = self._check_intersection(dot_bracket)

        for x in dot_bracket:
            e_idx += 1
            if x == "(":
                o_stack += 1
            elif x == ")":
                c_stack += 1
                if o_stack == c_stack:
                    self._parse_helix(list(dot_bracket[b_idx:e_idx]), b_idx, e_idx)
                    b_idx = e_idx

if __name__ == "__main__":
    # parser = NCMParser()
    # parser.ncmparser(list("(.(...).....((.)))"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("(.(..((...).....((.)))).)"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("(((.(.(...)).)))"))
    # print parser.ncms
    parser = NCMParser()
    parser.ncmparser(list("..((((...)))).....(.(.(...)).).((((......)).....))."))
    print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("(((((.(((((.(((((((........)))))))..)).))).)))))"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("(.(...)..)"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("..((((..))))()"))
    # print parser.ncms
