from subprocess import run

pids = run(["lsof","-t","-i:8002"],capture_output=True).stdout.decode("utf-8",errors = "ignore").strip().split("\n")
[run(["kill",pid]) for pid in pids]
run(["python","api.py"])