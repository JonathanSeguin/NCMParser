NCM = {
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

def parse(dot_bracket, dangling=0):
    open_var = False
    unpaired_left = 0
    while dot_bracket:
        x = dot_bracket.pop(0)
        if x == "." and dangling > 0:
            unpaired_left += 1
        elif x == "(":
            open_var = True
            unpaired_right, end = parse(dot_bracket, dangling + 1)
            if not end:
                try:
                    print NCM[2][unpaired_left + 2][unpaired_right + 2]
                except:
                    pass
        elif x == ")":
            if not open_var:
                try:
                    print NCM[1][unpaired_left + 2]
                except:
                    pass
                return 0, False
            if dangling == 1:
                return 0, True
            return unpaired_left, False

if __name__ == "__main__":
    parse(list("..((((...)))).....(.(.(...)).).((((......)).....))."))
