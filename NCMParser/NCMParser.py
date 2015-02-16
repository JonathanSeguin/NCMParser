#!/usr/bin/python
import pprint
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
        self.front_removed = 0
        self.dot_bracket = ""

    def _clean(self, idx_lst):
        try:
            idx_lst.remove(-1)
        except:
            pass

        try:
            idx_lst.remove(len(self.dot_bracket))
        except:
            pass
        return idx_lst

    def _check_intersection(self, dot_bracket, b_idx, e_idx, reverse=False, left=0, first=True):
        stack = 0
        o_stack = 0
        first_dangling = 0
        closing = False

        if reverse:
            openchar, closechar = ")", "("
        else:
            openchar, closechar = "(", ")"

        for i, x in enumerate(dot_bracket):
            if x == openchar:
                o_stack += 1
                if closing and stack == 1:
                    if reverse:
                        if not first:
                            try:
                                range1 = range(e_idx - left - 2, e_idx)
                                range2 = range(b_idx, b_idx + first_dangling + 2)
                                self.ncms.append({self.NCM[2][left + 2][first_dangling + 2]: self._clean(range1 + range2)})
                                pass
                            except:
                                pass
                        return dot_bracket[first_dangling + 1:][::-1], e_idx
                    else:
                        return self._check_intersection(dot_bracket[first_dangling + 1:][::-1],
                               b_idx=(e_idx - 1),  e_idx=(b_idx + first_dangling + 1), reverse=True, left=first_dangling, first=first)
                else:
                    stack += 1
                    closing = False
            if x == closechar:
                stack -= 1
                closing = True
            if x == "." and o_stack < 1:
                first_dangling += 1

        return dot_bracket, 0

    def _parse_helix(self, dot_bracket, b_idx, e_idx, int_b_idx, first=True):

        intersection, tmp_int_b_idx = self._check_intersection(dot_bracket, b_idx, e_idx, first=first)
        if intersection != dot_bracket:
            tmp_int_b_idx = tmp_int_b_idx + int_b_idx
            self.ncmparser(intersection, tmp_int_b_idx, first=True)
            return 0

        if len(dot_bracket) > 1:
            l = dot_bracket.pop(0) # left
            r = dot_bracket.pop() # right
            r_cnt = 1 # left count
            l_cnt = 1 # right count
        elif len(dot_bracket) == 1:
            l = dot_bracket.pop()
            l_cnt = 1
            r_cnt = 0
        else:
            return 0

        while l == ".":
            try:
                l = dot_bracket.pop(0)
                l_cnt += 1
            except:
                try:
                    self.ncms.append({self.NCM[1][l_cnt + r_cnt + 2]: self._clean(range(b_idx + int_b_idx - 2, e_idx + int_b_idx + 2))})
                except:
                    pass
                return 0

        while r == ".":
            r_cnt += 1
            r = dot_bracket.pop()

        self._parse_helix(dot_bracket, b_idx + l_cnt, e_idx - r_cnt, int_b_idx, False)

        if not first:
            try:
                range1 = range(b_idx + int_b_idx - 2, b_idx + int_b_idx + l_cnt + 1)
                range2 = range(e_idx + int_b_idx - r_cnt - 1, e_idx + int_b_idx + 2)

                self.ncms.append({self.NCM[2][l_cnt + 1][r_cnt + 1]: self._clean(range1 + range2)})
            except:
                pass

        return 0

    def ncmparser(self, dot_bracket, int_b_idx=0, first=True):
        if first:
            self.dot_bracket = dot_bracket

        o_stack = 0 # open stack
        c_stack = 0 # close stack
        b_idx = 0 # helix beginning index
        e_idx = 0 # helix end index

        # Check for a first intersection
        # dot_bracket = self._check_intersection(dot_bracket, b_idx, len(dot_bracket) - 1)

        for x in dot_bracket:
            e_idx += 1
            if x == "(":
                o_stack += 1
            elif x == ")":
                c_stack += 1
                if o_stack == c_stack:
                    self._parse_helix(list(dot_bracket[b_idx:e_idx]), b_idx, e_idx, int_b_idx, first)
                    b_idx = e_idx

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(width=60)
    # parser = NCMParser()
    # parser.ncmparser(list("(.(...).....((.)))"))
    # pp.pprint(parser.ncms)
    parser = NCMParser()
    parser.ncmparser(list("(.(..((...).....((.)))).)"))
    pp.pprint(parser.ncms)
    # parser = NCMParser()
    # parser.ncmparser(list("(((.(.(...)).)))"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("..((((...)))).....(.(.(...)).).((((......)).....))."))
    # pp.pprint(parser.ncms)
    # parser = NCMParser(
    # parser.ncmparser(list("(((((.(((((.(((((((........)))))))..)).))).)))))"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("(.(...)..)"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("..((((..))))()"))
    # print parser.ncms
