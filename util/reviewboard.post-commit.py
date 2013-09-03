#WARNING: this script may not even work, I haven't tried it with newest modifications. Anyway you need svnlook and GNU diff (for post-review) in PATH 
#and this thing assumes windows (although it may work elsewhere)

import sys, subprocess, re, os, os.path

post_review = """c:\server\\app\python27\scripts\post-review"""
gnuwin = """c:\program files(x86)\gnuwin32"""
username = "admin"
password = "msnc500"
reviewboard = "http://reviewboard:8080"

svn_dir = sys.argv[1]
svn_name = os.path.basename(svn_dir)
svn_rev = int(sys.argv[2])
rev_range = "{0}:{1}".format(svn_rev-1, svn_rev)

def read_process_output(cmdline):
	process = subprocess.Popen(cmdline,stdout=subprocess.PIPE)
	return process.stdout.read().rstrip()

text=read_process_output("svnlook log -r {0} {1}".format(svn_rev, svn_dir))
author = read_process_output("svnlook author -r {0} {1}".format(svn_rev, svn_dir))
text_first_line=text.replace("\n"," ").replace("\r","");
if len(text_first_line)>64:
	text_first_line=text_first_line[0:64]+"..."

target_groups = ",".join(["tracticket{0}".format(x[1:]) for x in re.findall("""\#\d+""", text)])


args = [post_review, 
	"--repository-url=http://msncdata:81/svn/{0}".format(svn_name), 
	"--username={0}".format(username), 
	"--password={0}".format(password), 
	"--revision-range={0}".format(rev_range), 
	"--target-groups={0}".format(target_groups), 
	"--publish", 
	"--summary={0}".format(text_first_line), 
	"--description={0}".format(text),
	"--submit-as={0}".format(author),
	"--server={0}".format(reviewboard)]
print " ".join(args)
subprocess.call(args)

