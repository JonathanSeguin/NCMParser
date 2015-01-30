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
        # print "ci : " + str(dot_bracket)
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
                            print self.NCM[2][left + 2][first_dangling + 2]
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
                print self.NCM[2][left + 2][first_dangling + 2]
                self.ncms.append(self.NCM[2][left + 2][first_dangling + 2])
            except:
                pass
            return dot_bracket[first_dangling + 1:][::-1]
        return dot_bracket

    def _parse_helix(self, dot_bracket, first=True):

        intersection = self._check_intersection(dot_bracket)
        orig_dot_bracket = dot_bracket

        if intersection != orig_dot_bracket:
            try:
                self.ncmparser(intersection)
                return 0
            except:
                pass

        if len(dot_bracket) > 1:
            left = dot_bracket.pop(0)
            right = dot_bracket.pop()
            right_count = 1
            left_count = 1
        elif len(dot_bracket) == 1:
            left = dot_bracket.pop(0)
            left_count = 0
        else:
            return 0

        while left == ".":
            left_count += 1
            try:
                left = dot_bracket.pop(0)
            except:
                try:
                    print self.NCM[1][left_count + 2]
                    self.ncms.append(self.NCM[1][left_count + 2])
                except:
                    pass
                return 0

        while right == ".":
            right_count += 1
            right = dot_bracket.pop()

        self._parse_helix(dot_bracket, False)

        if not first:
            try:
                print self.NCM[2][left_count + 1][right_count + 1]
                self.ncms.append(self.NCM[2][left_count + 1][right_count + 1])
            except:
                pass

        return 0

    def ncmparser(self, dot_bracket):
        o_stack = 0
        c_stack = 0
        start_index = 0
        end_index = 0

        # Check for a first intersection
        dot_bracket = self._check_intersection(dot_bracket)

        for x in dot_bracket:
            end_index += 1
            if x == "(":
                o_stack += 1
            elif x == ")":
                c_stack += 1
                if o_stack == c_stack:
                    # print start_index
                    self._parse_helix(list(dot_bracket[start_index:end_index]))
                    # print end_index
                    start_index = end_index
        # return self.ncms


if __name__ == "__main__":
    parser = NCMParser()
    parser.ncmparser(list("(.(...).....((.)))"))
    print parser.ncms
    parser = NCMParser()
    parser.ncmparser(list("(.(..((...).....((.)))).)"))
    print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("(((.(.(...)).)))"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("..((((...)))).....(.(.(...)).).((((......)).....))."))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("(((((.(((((.(((((((........)))))))..)).))).)))))"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("(.(...)..)"))
    # print parser.ncms
    # parser = NCMParser()
    # parser.ncmparser(list("..((((..))))()"))
    # print parser.ncms
