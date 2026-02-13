import os, sys, tempfile, shutil, logging, re, ftplib, ntpath, ConfigParser

# ---------------------------------------------------------------
# For language translation, recursively copies all property files
# from specified folder to a temporary folder, zips the files and
# sends zip file to configured ftp server
# ---------------------------------------------------------------
#  Author: Ranjith Karunakaran

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
log = logging.getLogger()

def get_usage(prog):
    "Get usage message"
    return """\nUsage: %s <path> [<languages>]\n
       <path> - directory that has the property files
       <language> - comma separated language codes like en,es,cn etc.""" % prog


def prop_file_matches(file, langs):
    "Is the property file name matching the required language (en, es etc.)"
    if not langs and (re.match('.*[^_]..\.properties', file) or file.endswith("_en.properties") or file == "en.json"):
        return True
    elif any(file.endswith("%s.properties" % lang) for lang in langs):
        return True
    elif any(file == "%s.json" % lang[1:] for lang in langs):
        return True
    elif re.match('.*[^_]..\.properties', file) and "_en" in langs:
        return True
    return False


def copy_if_prop_file(file, path, srcdir, targetdir, langs):
    "Copy property file if it matches required language"
    if prop_file_matches(file, langs):
        log.info("property file: %s" % file)
        newpath = targetdir + path[len(srcdir):]
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        shutil.copyfile("%s/%s" % (path, file), "%s/%s" % (newpath, file))


def copy_lang_files(srcdir, targetdir, langs):
    "Recursively copy all property files that match the required languages"
    for path, dirs, files in os.walk(srcdir):
        for file in files:
            copy_if_prop_file(file, path, srcdir, targetdir, langs)


def send_file_ftp(host, port, username, password, remote_dir, copy_file):
    "Send binary file through FTP"
    session = ftplib.FTP()
    session.connect(host, port)
    session.login(username, password)
    copied_file = open(copy_file, 'rb')
    session.cwd(remote_dir)
    session.storbinary('STOR %s' % ntpath.basename(copy_file), copied_file)
    copied_file.close()
    session.quit()
    log.info("Copied %s to FTP host %s" % (copy_file, host))


def archive_lang_files(srcpath, langs):
    "Compress all properties files matching required languages"
    tmpdir = tempfile.mkdtemp()
    tmpdir_files = "%s/files" % tmpdir
    log.info("Temp directory: %s" % tmpdir)
    copy_lang_files(srcpath, tmpdir_files, langs)
    filename = "English" if (not langs or (len(langs) == 1 and langs[0] == "en")) else "OtherLanguages"
    zip_file = "%s/%s" % (tmpdir, filename)
    shutil.make_archive(zip_file, "zip", tmpdir_files)
    shutil.rmtree(tmpdir_files)
    return zip_file

def main(argv):
    "Script entry point"
    cfg = ConfigParser.RawConfigParser()
    cfg.read('copy_translations.properties')
    srcpath = argv[1] if len(argv) > 1 else sys.exit(get_usage(argv[0]))
    langs = [] if len(argv) == 2 else [("_%s" % lang) for lang in argv[2].split(",")]
    zip_file = "%s.zip" % archive_lang_files(srcpath, langs)
    send_file_ftp(cfg.get('ftp','host'), cfg.get('ftp','port'), cfg.get('ftp','username'), \
                  cfg.get('ftp','password'), cfg.get('ftp','remotedir'), zip_file)


if __name__ == "__main__":
    main(sys.argv)
