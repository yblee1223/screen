import shutil
import sys
import os
sys.path.append(os.path.join("example", "file_test"))
print(sys.path)

# shutil.move("dummy/folder1", "dummy2")
# shutil.copytree("dummy/", "dummy2")
# shutil.copy("dummy/folder1", "dummy2")
shutil.rmtree(os.path.join('example', 'file_test', 'dummy'))
# print(os.listdir(os.path.join('example', 'file_test', 'dummy')))
# os.mkdir('dummy')