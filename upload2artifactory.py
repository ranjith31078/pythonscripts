import os
import subprocess as proc
from os.path import expanduser

# Change below constant. List sub-folders in local repository that need to be uploaded (under C:\Users\<user>\.m2\repository)
# For eg. for C:\Users\<user>\.m2\repository\ar, just add "ar" to list

SUB_FOLDERS_TO_UPLOAD = ["avalon-framework"]

# -----------------------------------------------------------------------------------------------------------------------
# DO NOT CHANGE BELOW LINES
# -----------------------------------------------------------------------------------------------------------------------
MAVEN_REPO_PATH = expanduser("~") + "\\.m2\\repository\\"
# ARTIFACTORY_URL = "https://artifactory.uplandsoftware.net/artifactory/PowerSteering_MVN/"
ARTIFACTORY_URL = ""
USER_NAME = ""
PASSWORD = ""

CODEARTIFACT_AUTH_TOKEN = "eyJ2ZXIiOjEsImlzdSI6MTcyMzQ1Nzk1MywiZW5jIjoiQTEyOEdDTSIsInRhZyI6InFydkEyQWlzZXVqOHFvdDc4d2JEV3ciLCJleHAiOjE3MjM1MDExNTMsImFsZyI6IkExMjhHQ01LVyIsIml2IjoiNGZmenVYcWg2Nl8yWFhnQyJ9.YkvamOB271YGFkKj088Hiw.BBhm4E1bNrZnIWik.XDVUBKDjq22TUfBwqs2iYky7hvyG3fdVCpia1jYrNJJ7OAcwo9kLvYEjhV1WKnw-Hv-TXaU1SV4TzRIF97qeEra8nRocnypNQEe2yRUoSiekSMrCzZ5L2u9wLCVKXCwMtOOS5uP0XxfP4VG36a6RvBOawP3cXtEXQMVLMRqtYXFepHHT2bxgKwzdX7EGK2CqynUt1jFYhat36aRsVSZpQ2Q8IjmQi9g3d6oCQfQcRwfkgkR9dUxyHOAPqHFvy15yDMNUpA81hmUOx-j3CuYmhpSlKLzlwqIw44PYQPOyNdVb-W-ehEqFHz0QC5pSQxkDS64S70QJlBATQZzv44to7HYJ0Fd5t-7gRGhagdTT-e9Vbdequ8pKbJJuMdXnfU87zAMmdmJafLxbpiQMeV5jSltjv7kGE2EhOfMGp4vt67iA6khoC4T_CSSmUx4qbrlnlj7zSvqqhUrao5wuOFicKi9yL582TskEaml_snsONvmNFyYyO9x4CDAXG1HhEB01ZyaVZf34w7d3i-U9vYHnZjLZxmwtPCK2mXiOZ5wUay5uYSakcR0C1yWF_ObJqw1oOF5eqn8dn6u0D5-Kgd5K4R93H_cfYuIcrZWK46WveDdBFgecC9razlHJXZXYooT6zbw6MKCr0XvSa9fX2YezLEFKtgtloWcGROXBs8USVQ6pOOKgHGGF5IrpFN3M4uNCOIb2rK0gCrScPCvrb5VC-Oy9Ug1yuTEw4mIU8nOLEvqBsqXHE0iImrLF9YoGKnzgBxltGS05z749FIptdiJYV_B_isLT5dyxAb7bfgS_etuDW_dHd6Thz3VcOdoBu2mz8hzGUspa34mNk3M65xSngjO8qdz_n1zdyHIaptbqtZrOoXZSlfYt_hDboTema5h5QgNL-f8UM_FAxekiL8YVHRLE1Bv4LXTJDzEzgUplN9aqGXWztPxkIuCss_o-lcse7-J9YSIGHgMjEJ-qiKAt9lk2VRPnUQmkNvHWdTZk012j.Ci3-Jddx28HvjT1VeCtfgw"

ENABLE_UPLOAD = True # Set this to false to only see the actual files processed

def get_jar_files(lib_folder):
    for root, dirs, files in os.walk(lib_folder):
        path = root.split(os.sep)
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                yield file_path[len(lib_folder)+1:]

def process(sub_folders, full_path_provided = False):
    files_uploaded = 0
    upload_failures = 0
    for folder in sub_folders:
        if full_path_provided:
            folder_path = folder
        else:
            folder_path = MAVEN_REPO_PATH + folder
        os.chdir(folder_path)
        for file in get_jar_files(folder_path):
            target_url = ARTIFACTORY_URL + folder[folder.rfind('\\')+1:] + '/' + file.replace('\\','/')
            try:
                # command = ["curl", "-X", "PUT", "-u", "service_rdsystems_PSS@uplandsoftware.com:m<[-4RLnk'7gByfuQ1",
                #                "-T", folder_path + '\\' + file, target_url]

                os.chdir(folder_path + '\\' + file[:file.rfind('\\')+1])
                print(folder_path + '\\' + file[:file.rfind('\\')+1])

                command = ["curl","--request","PUT", target_url, "--user","'aws:" + CODEARTIFACT_AUTH_TOKEN + "'","--header",
                           "'Content-Type:application/octet-stream'","--data-binary","@" + file[file.rfind('\\')+1:]]

                print(command)
                if ENABLE_UPLOAD:
                    proc.call(command)
                files_uploaded += 1
            except RuntimeError as error:
                print("Unable to process " + target_url)
                print(error)
                upload_failures += 1
                pass
    print("\n\n\nUploaded " + str(files_uploaded) + " files. Failures " + str(upload_failures)) 


def get_all_sub_folders(top_folder):
    return [f.path for f in os.scandir(top_folder) if f.is_dir()]


if __name__ == '__main__':
    # process(SUB_FOLDERS_TO_UPLOAD) # Upload ony files under one folder in local repository to remote maven repository
    process(get_all_sub_folders(MAVEN_REPO_PATH), True) # Upload all files to remote maven repository
