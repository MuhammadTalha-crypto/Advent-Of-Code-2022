
import re

DAY_NUM = 7
DAY_DESC = 'Day 7: No Space Left On Device'

def calc(log, values, mode):
    dirs = {}
    dir_name = [""]

    for row in values:
        m = re.search("^(?P<size>[0-9]+) (?P<fn>.*)$", row)
        if m is not None:
            size = int(m.group('size'))
            fn = m.group('fn')
            dirs["/".join(dir_name)].append([size, fn])
        
        m = re.search("^\\$ cd (?P<dn>.*)$", row)
        if m is not None:
            if m.group("dn") == "..":
                dir_name.pop(-1)
            else:
                dir_name.append(m.group("dn"))
                if "/".join(dir_name) not in dirs:
                    dirs["/".join(dir_name)] = []

        m = re.search("^dir (?P<dn>.*)$", row)
        if m is not None:
            dirs["/".join(dir_name)].append([-1, "/".join(dir_name + [m.group("dn")])])


    def get_size(dn):
        ret = 0
        for size, fn in dirs[dn]:
            if size == -1:
                ret += get_size(fn)
            else:
                ret += size
        return ret

    if mode == 2:
        free_space = 70000000 - get_size("//")
        best = None
        best_dir = ""
        for dn in dirs:
            test = get_size(dn)
            if test + free_space >= 30000000:
                if best is None or test <= best:
                    best = test
                    best_dir = dn
        return best

    if mode == 1:
        ret = 0
        for dn in dirs:
            size = get_size(dn)
            if size <= 100000:
                ret += size
        return ret

    return 0

def test(log):
    values = log.decode_values("""
        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        dir e
        29116 f
        2557 g
        62596 h.lst
        $ cd e
        $ ls
        584 i
        $ cd ..
        $ cd ..
        $ cd d
        $ ls
        4060174 j
        8033020 d.log
        5626152 d.ext
        7214296 k
    """)

    log.test(calc(log, values, 1), 95437)
    log.test(calc(log, values, 2), 24933642)

def run(log, values):
    log(calc(log, values, 1))
    log(calc(log, values, 2))

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["test.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!"); exit(1)
    with open(fn) as f: values = [x.strip() for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)