import inspect, os
curDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
rootdir = curDir + "/Templates"
print(f"Root dir: {rootdir}")

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(os.path.join(subdir, file))