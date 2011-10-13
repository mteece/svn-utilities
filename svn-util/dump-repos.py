#!/usr/bin/python

import commands
import getopt
import os
import os.path
import sys

def main(argv):

    """Run export on existing SVN repositories.
    Use an 'svnadmin' binary from a release with the same schema version
    as your repository to create a dumpfile of your repository:
    $ mv myrepos old-repos
    $ svnadmin dump old-repos > dumpfile"""

    try:
        opts, args = getopt.getopt(sys.argv[1:],"h:p:b:",["help","parentdir","backupdir"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    parent_dir = None
    backup_dir = None

    for x, a in opts:
     
        if x in ("-h","--help"):
            usage()
            sys.exit()
        elif x in ("-p", "--parentdir"):
            parent_dir = a
        elif x in("-b","--backupdir"):
            backup_dir = a
        else:
            assert False, "unknown argument"
            usage()

    if parent_dir == "" or backup_dir == "":
        usage()
        sys.exit(2)

    # watch those corners
    if not backup_dir.endswith(os.path.sep):
        backup_dir += os.path.sep
    if not parent_dir.endswith(os.path.sep):
        parent_dir += os.path.sep
    
    # get repository list
    repositories = []
    if os.path.exists(parent_dir):
        for object in os.listdir(parent_dir):
            if os.path.isdir(os.path.join(parent_dir, object)):
                repositories.append(object)

    if len(repositories) > 0:
        repositories.sort()
        for dir in repositories:
            repos = os.path.join(parent_dir, dir)

            if os.path.isdir(repos):

                # TODO: tsk tsk handle dir copy without strings
                # import shutil http://docs.python.org/library/shutil.html
                #tmp = "%s%s" % (backup_dir, dir)
                #dest = os.path.normpath(tmp)
                
                # TODO: Stop using 'old-'
                copy_cmd = "mv %s %sold-%s" % (repos, backup_dir, dir)
                print copy_cmd
                print commands.getoutput(copy_cmd)
        
                admin_cmd = "svnadmin dump %sold-%s > %s%s-dumpfile" % (backup_dir, dir, backup_dir, dir)
                print admin_cmd
                print commands.getoutput(admin_cmd)

                # TODO: You should clean up afterwards
                # Leftover directories post svnadmin dump
                
            else:
                print "not a directory {0:>s}".format(repos)

    else:
        print "no repositories found in {0:>s} ".format(parent_dir)
        
def usage():

    print "Usage: -p parentdir -b backupdir"
    print ""
    print "$ python dump-repos.py -p /usr/local/svn/repos/ -b /usr/local/svn/backup/"
    print ""
    print "Specify full paths for --parentdir and --backupdir."
    print "Iterates repository dir(s) in parentdir, moves the dir(s) to backupdir, and creates a dumpfile from \'svnadmin\' as a batch."
    print "Use an \'svnadmin\' binary from a release with the same schema version."
    print "To revert repository changes and restore run load-repos.py."

    sys.exit(0)

if __name__=="__main__":
    main( sys.argv )
