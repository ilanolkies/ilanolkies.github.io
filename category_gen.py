import glob
import os

post_dir = '_posts/'
cat_dir = 'category/'

filenames = glob.glob(post_dir + '*md')

total_cats = []
for filename in filenames:
    f = open(filename, 'r')
    crawl = False
    for line in f:
        if crawl:
            current_category = line.strip().split()
            if current_category[0] == 'category:':
                total_cats.extend(current_category[1:])
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_cats = set(total_cats)

old_tags = glob.glob(cat_dir + '*.md')
for tag in old_tags:
    os.remove(tag)
    
if not os.path.exists(cat_dir):
    os.makedirs(cat_dir)

for cat in total_cats:
    cat_filename = cat_dir + cat + '.md'
    f = open(cat_filename, 'a')
    write_str = '---\nlayout: category\ntitle: \"Tag: ' + cat + '\"\ncategory: ' + cat + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()
print("Categories generated, count", total_cats.__len__())
