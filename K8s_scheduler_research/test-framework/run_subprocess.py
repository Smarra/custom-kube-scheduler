import subprocess


def run(cmd, wait=1):
    if wait != 1:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return ""
    else:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process.wait()
        json_response, err = process.communicate()
        if process.returncode == 0:
            return json_response.decode('utf-8')
        else:
            print("Error:", err)
            return "Error: " + "err"
