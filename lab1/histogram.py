import matplotlib.pyplot as plt
from collections import Counter

# Analyzed ciphertext
ciphertext = (
    "HEJJWIEEFHKGAOBMXHKYCMZGRENHAEEFKXFRKFLURJOYONWAEEFRMYKUGMVUGNKREUNMBMZWEXMZMQMQRMZGNHMGYMXMIHMZMGEQMEXMLJUAGKXOXYEXGLOYUEUGAKFAMNOXNEKYEQLUNMZIKONGGMYEXFGKXFNKCMGEBMZNHMMXNOZMOXTZKGNZUYNUZMRKFRMYKUGMOXNHMZMKJIEZJFKFMBOYMFEMGXNHKYCMBMZWNHOXAONKJIKWGMPLJEONGKGLMYOTOYLZENEYEJKFMGOAXTJKIEZKQOGYEXTOAUZMFFMBOYM"
)

# Counting letter occurrences
counter = Counter(ciphertext)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Preparing data for the chart (keeping alphabetical order)
labels = list(alphabet)
values = [counter[letter] for letter in labels]

# Creating the chart
plt.figure(figsize=(12, 6))
bars = plt.bar(labels, values, color='skyblue', edgecolor='black')

# Adding values above the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, int(yval), ha='center', va='bottom', fontsize=10)

# Appearance configuration
plt.title('Histogram of letter frequency in the ciphertext', fontsize=16, fontweight='bold')
plt.xlabel('Letters of the alphabet', fontsize=12)
plt.ylabel('Number of occurrences', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Displaying the chart
plt.tight_layout()
plt.show()