import os, re
path = 'C:\Ranjith\Movies\Curious George Collection'
files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path)) for f in fn]
i = 1

for file in files:
    new_name = os.path.join(path, re.sub('^ ','',file))
    new_name = re.sub('[ ]+',' ',new_name)
    new_name = re.sub('\\\\([^\\\\]+)$',' \\1',new_name)
    os.rename(file, new_name)
    i = i + 1