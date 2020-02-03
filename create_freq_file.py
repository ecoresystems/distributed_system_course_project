import os
import subprocess

text_file = open("text_freq_jp", 'w+', encoding='utf-8', newline='')
data_dir = 'data'

files = os.listdir(data_dir)
text_counter = 1
for file in files:
    uuid = file.split('_')[0]
    if file.endswith("text.txt"):
        process = subprocess.Popen(
            "perl wams/mkfreq_jp.pl -f " + data_dir + "/" + file + " -u " + uuid + " -i " + str(text_counter),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        text_file.write(out.decode('utf-8'))
        text_counter += 1
    if text_counter % 100 == 0:
        print("Parsing %d/250000" % text_counter)

text_file.close()
print("Process Finished")
