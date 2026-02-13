import os
import xml.etree.ElementTree as ET
import subprocess

def extract_pom_info(pom_path):
    # Parse the POM file
    tree = ET.parse(pom_path)
    root = tree.getroot()
    
    # Helper function to find elements ignoring namespaces
    def find_element(name):
        return root.find(f".//{name}") or root.find(f".//{{*}}{name}")
    
    # Extract groupId, artifactId, and version
    group_id = find_element('groupId')
    artifact_id = find_element('artifactId')
    version = find_element('version')

    return (group_id.text if group_id is not None else None,
            artifact_id.text if artifact_id is not None else None,
            version.text if version is not None else None)

def deploy_jar(jar_path, group_id, artifact_id, version):
    # Construct the mvn command
    
    file_name = jar_path[jar_path.rfind('\\')+1:]
    os.chdir(jar_path[:jar_path.rfind('\\')+1])

    cmd = [
        "mvn.cmd", "deploy:deploy-file","-e",
        f"-DgroupId={group_id}",
        f"-DartifactId={artifact_id}",
        f"-Dversion={version}",
        f"-Dfile={file_name}",
        "-Dpackaging=jar",
        "-DrepositoryId=codeartifact",
        "-Durl=<>"
    ]

    # Run the command
    subprocess.run(cmd, shell=True)

def traverse_and_deploy(repo_path):
    for root, dirs, files in os.walk(repo_path):
        # Check if a POM file and a JAR file exist in the current directory
        pom_files = [f for f in files if f.endswith(".pom")]
        jar_files = [f for f in files if f.endswith(".jar")]

        if pom_files and jar_files:
            pom_path = os.path.join(root, pom_files[0])
            jar_path = os.path.join(root, jar_files[0])
            
            group_id, artifact_id, version = extract_pom_info(pom_path)
            
            if group_id and artifact_id and version:
                deploy_jar(jar_path, group_id, artifact_id, version)
            else:
                print(f"Failed to extract info from POM: {pom_path}")

if __name__ == "__main__":
    # Set the path to your local Maven repository
    repo_path = "C:\\Users\\<user>\\.m2\\repository"
    
    traverse_and_deploy(repo_path)
