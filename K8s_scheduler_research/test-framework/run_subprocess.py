import subprocess

def scrape_k8s(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    json_response, err = process.communicate()
    if process.returncode == 0:
        return json_response.decode('utf-8')
    else:
        print("Error:", err)
        return "Error: " + "err"
