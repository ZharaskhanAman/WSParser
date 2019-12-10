import re


def parse_lessons(line):
    line = line.replace('\n', ' ')
    line = line.replace("Круглый зал", "Круглый_зал")
    line = line.rstrip().split(" ")

    match = re.search("\(([0-9:]{5})-([0-9:]{5})\)", line[-1])

    return {
        "start_time": match.group(1),
        "end_time": match.group(2),
        "room": line[-2],
        "teacher": line[-5] + " " + line[-4],
        "subject": " ".join(line[:-5])
    }


#with open("../data/lessons.txt") as fp:
#    for line in fp:
#        print(parse_lessons(line))
