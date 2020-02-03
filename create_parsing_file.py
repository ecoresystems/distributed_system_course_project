import os
import subprocess
import mysql.connector

cnx = mysql.connector.connect(host='13.231.178.152', username='dist-admin', password='dist-admin',
                              database='distributed_system_2019')

cursor = cnx.cursor()

cursor.execute('SELECT * FROM jp_wiki')
result = cursor.fetchall()

counter = 0
for row in result:
    with open('data/%s_text.txt' % row[0], 'w', encoding='utf-8') as text_file:
        text_file.write(row[1])
        counter += 1
    if counter % 100 == 0:
        print("Processing %d" % counter)

# title_file = open("title_freq", 'w+', encoding='utf-8', newline='')
# text_file = open("text_freq", 'w+', encoding='utf-8', newline='')

# for file in files:
#     if file.endswith("title.txt"):
#         freq_segment = os.system("perl wams/mkfreq.pl -f " + data_dir + "/" + file)
#         process = subprocess.Popen("perl wams/mkfreq.pl -f " + data_dir + "/" + file, stderr=subprocess.PIPE,
#                                    stdout=subprocess.PIPE, shell=True)
#         out, err = process.communicate()
#         print("Starting point of system print")
#         title_file.write(out.decode('utf-8'))
#     if file.endswith("text.txt"):
#         freq_segment = os.system("perl wams/mkfreq.pl -f " + data_dir + "/" + file)
#         process = subprocess.Popen("perl wams/mkfreq.pl -f " + data_dir + "/" + file, stderr=subprocess.PIPE,
#                                    stdout=subprocess.PIPE, shell=True)
#         out, err = process.communicate()
#         print("Starting point of system print")
#         text_file.write(out.decode('utf-8'))
#
# freq_segment = os.system("perl wams/mkfreq.pl -f sample_data/blogs_0000001_text.txt")
#
# print(freq_segment)
