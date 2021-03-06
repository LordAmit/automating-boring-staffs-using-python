from typing import List

corestring = """Extracted Annotations (7/13/2018, 9:14:41 PM)
sample notes extracted from PDF
#g eita ek  
line g#
#b  asd asd
asd b#
#p asd asd asd p#
#i asd asd asd i#
#g asd asd asd g#
#b asd asd asd b#
#p point point
point p#

"""

tag_pairs = {"#b": "b#", "#g": "g#", "#p": "p#", "#c": "c#"}


def __count_tags(text: str, tag_start: str, tag_end: str) -> int:
    return text.count(tag_start) + text.count(tag_end)


def __count_all_tags(text: str) -> int:
    return __count_tags(text, "#g", "g#") + __count_tags(text, "#b", "b#") + \
        __count_tags(text, "#p", "p#") + __count_tags(text, "#c", "c#")


def __find_start_tag_in_line(text: str):
    if list(tag_pairs)[0] in text:
        return list(tag_pairs)[0]
    if list(tag_pairs)[1] in text:
        return list(tag_pairs)[1]
    if list(tag_pairs)[2] in text:
        return list(tag_pairs)[2]
    if list(tag_pairs)[3] in text:
        return list(tag_pairs)[3]


def __beautify_output_lines(lines: List[str], tag_type: str, start_tag: str,
                            markdown: bool = False) -> str:
    if len(lines) < 1:
        print("no lines found, exiting")
        return ""
    combined_line: str = tag_type.upper()
    if markdown:
        combined_line = "# " + combined_line
    combined_line += "\n"
    end_tag: str = tag_pairs[start_tag]
    for line in lines:

        is_end_tag_in_line: bool = line.find(end_tag) != -1
        is_start_tag_in_line: bool = line.find(start_tag) != -1

        # print(line + ": " + str(is_end_tag_in_line))
        if is_start_tag_in_line and markdown:
            combined_line += "-"
        # line = line.replace("\n", "")
        combined_line += " " + line.strip()
        if is_end_tag_in_line:
            combined_line += "\n"
        combined_line = combined_line.replace(start_tag, "")
        combined_line = combined_line.replace(end_tag, "")
        combined_line = combined_line.replace("  ", " ")
    return "\n"+combined_line


def __start_tag_in_line(line: str):
    global tag_pairs
    return list(tag_pairs)[0] in line or list(tag_pairs)[1] in line or \
        list(tag_pairs)[2] in line or list(tag_pairs)[3] in line


def process_content(value: str, markdown: bool=False) -> str:
    global tag_pairs
    tag_count = __count_all_tags(value)
    if tag_count % 2 is not 0:
        return("problem with tags. total tags: "+str(tag_count))

    all_lines: List[str] = value.splitlines()
    good_points: List[str] = []
    bad_points: List[str] = []
    comments: List[str] = []
    i_points: List[str] = []
    all_comments = {"b#": bad_points, "g#": good_points,
                    "c#": comments, "p#": i_points}
    is_looking_for_end_tag = False
    end_tag: str = ""
    for line in all_lines:
        # print("processing: "+line)
        if __start_tag_in_line(line):
            is_looking_for_end_tag = True
            end_tag = tag_pairs[__find_start_tag_in_line(line)]
        if is_looking_for_end_tag:
            # print("looking for end tag: " + line)
            all_comments[end_tag].append(line)
        if end_tag in line:
            # print("found end tag: " + line)
            is_looking_for_end_tag = False
    full_content: str = __beautify_output_lines(
        good_points, "Good Points", "#g", markdown)
    full_content += __beautify_output_lines(bad_points,
                                            "Bad Points",
                                            "#b", markdown)
    full_content += __beautify_output_lines(comments,
                                            "Comments", "#c", markdown)
    full_content += __beautify_output_lines(i_points,
                                            "Intersting Points",
                                            "#p", markdown)
    return full_content


if __name__ == "__main__":
    print(process_content(corestring, markdown=True))
