#!/usr/bin/python

import commands
import getopt
import os
import os.path
import sys

def main(argv):

    """Run import on existing SVN repositories.
    Use an 'svnadmin' binary from a release with the same schema version
    as you want your repository to have to load the dumpfile into a new
    repository:
    $ svnadmin create myrepos
    $ svnadmin load myrepos < dumpfile"""

    try:
        opts, args = getopt.getopt(sys.argv[1:],"h:s:d:",["help","sourcedir","destinationdir"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    source_dir = None
    destination_dir = None

    for x, a in opts:
     
        if x in ("-h","--help"):
            usage()
            sys.exit()
        elif x in ("-s", "--sourcedir"):
            source_dir = a
        elif x in("-d","--destinationdir"):
            destination_dir = a
        else:
            assert False, "unknown argument"
            usage()

    if source_dir == "" or destination_dir == "":
        usage()
        sys.exit(2)
    
     # watch those corners
    if not source_dir.endswith(os.path.sep):
        source_dir += os.path.sep
    if not destination_dir.endswith(os.path.sep):
        destination_dir += os.path.sep

    # get repository list
    repositories = []
    if os.path.exists(source_dir):
        for object in os.listdir(source_dir):
            if os.path.isdir(os.path.join(source_dir, object)):
                repositories.append(object)

    if len(repositories) > 0:
        repositories.sort()
        for dir in repositories:

            # TODO: Stop using 'old-'	    
            name = dir.replace ('old-', '')
            new_repos = os.path.join(destination_dir, name)

            # let us not overwrite anything important
            if not os.path.isdir(new_repos):
                create_cmd = "svnadmin create %s" % new_repos
                print create_cmd
                print commands.getoutput(create_cmd)
                
                restore = os.path.join(source_dir, new_repos)
                data = os.path.join(destination_dir, new_repos)

                load_cmd = "svnadmin load %s < %s-dumpfile" % (restore, data)
                print load_cmd
                print commands.getoutput(load_cmd)

		# TODO: You should clean up afterwards

    else:
        print "no repositories found in {0:>s} ".format(source_dir)

def usage():

    print "Usage: -s sourcedir -d destinationdir"
    print ""
    print "$ python load-repos.py -s /usr/local/svn/backup/ -d /usr/local/svn/repos/"
    print ""
    print "Specify full paths for --sourcedir and --destinationdir."
    print "Iterates repository backup dir(s), creates new repository dir(s), and loads svn data from dumpfile using \'svnadmin\' as a batch."
    print "Use an \'svnadmin\' binary from a release with the same schema version."

    sys.exit(0)

if __name__=="__main__":
    main( sys.argv )

