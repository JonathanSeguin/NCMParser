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

def parse_helix(dot_bracket, first=True):
    left = dot_bracket.pop(0)
    right = dot_bracket.pop()
    left_count = 2
    right_count = 2

    while left == ".":
        left_count += 1
        try:
            left = dot_bracket.pop(0)
        except:
            try:
                print NCM[1][left_count + 1]
            except:
                pass
            return 0

    while right == ".":
        right_count += 1
        right = dot_bracket.pop()

    parse_helix(dot_bracket, False)

    if not first:
        try:
            print NCM[2][left_count][right_count]
        except:
            pass


def parse(dot_bracket):
    o_stack = 0
    c_stack = 0
    start_index = 0
    end_index = 0
    for x in dot_bracket:
        end_index += 1
        if x == "(":
            o_stack += 1
        elif x == ")":
            c_stack += 1
            if o_stack == c_stack:
                parse_helix(list(dot_bracket[start_index:end_index]))
                start_index = end_index


if __name__ == "__main__":
    parse(list("..((((...)))).....(.(.(...)).).((((......)).....))."))
    #parse(list("(((((.(((((.(((((((........)))))))..)).))).)))))"))
    #parse(list("(.(...)..)"))
    #parse(list("(((.(.(...)).)))"))
