
#!/usr/bin/python

import json
import os
import sys

fd = open("file_info_dict.json", "r")
content = fd.read()
fd.close()

file_info_dict = json.loads(content)
rep_strings = file_info_dict["replace"]

for i_file in file_info_dict.keys():
    if ".py" not in i_file:
        continue
    i_file_pr = i_file.split(".")[0]

    r_file = file_info_dict[i_file]["running"]
    r_file = r_file.split("/")[1]

    fd = open(r_file, "r")
    content = fd.read()
    fd.close()

    
    for rep_string in rep_strings:
        print(rep_string[1], rep_string[2])
        content = content.replace("from " + rep_string[1] + " import",
                                  "from " + rep_string[2] + " import")
    
    fd = open(r_file, "w")
    fd.write(content)
    fd.close()
    